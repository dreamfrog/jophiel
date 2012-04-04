

class LoadManager(Thread):
    def __init__(self, num_agents, interval, rampup, log_msgs, runtime_stats, error_queue, output_dir=None, test_name=None):
        Thread.__init__(self)
        
        socket.setdefaulttimeout(SOCKET_TIMEOUT)  # this affects all socket operations (including HTTP)
        
        self.running = True
        self.num_agents = num_agents
        self.interval = interval
        self.rampup = rampup
        self.log_msgs = log_msgs
        self.runtime_stats = runtime_stats
        self.error_queue = error_queue  # list used like a queue
        self.test_name = test_name

        if output_dir and test_name:
            self.output_dir = time.strftime(output_dir + '/' + test_name + '_' + 'results_%Y.%m.%d_%H.%M.%S', time.localtime())
        elif output_dir:
            self.output_dir = time.strftime(output_dir + '/' + 'results_%Y.%m.%d_%H.%M.%S', time.localtime())
        elif test_name:
            self.output_dir = time.strftime('results/' + test_name + '_' + 'results_%Y.%m.%d_%H.%M.%S', time.localtime())
        else:
            self.output_dir = time.strftime('results/results_%Y.%m.%d_%H.%M.%S', time.localtime()) 
        
        # initialize/reset stats
        for i in range(self.num_agents): 
            self.runtime_stats[i] = StatCollection(0, '', 0, 0, 0, 0, 0, 0)
            
        self.workload = {
            'num_agents': num_agents,
            'interval': interval * 1000, # convert to millisecs   
            'rampup': rampup,
            'start_epoch': time.mktime(time.localtime())
        }  
        
        self.results_queue = Queue.Queue()  # result stats get queued up by agent threads
        self.agent_refs = []
        self.msg_queue = []  # list of Request objects
        
    
    def run(self):
        self.running = True
        self.agents_started = False
        try:
            os.makedirs(self.output_dir, 0755)
        except OSError:
            self.output_dir = self.output_dir + time.strftime('/results_%Y.%m.%d_%H.%M.%S', time.localtime())
            try:
               os.makedirs(self.output_dir, 0755)
            except OSError:
                sys.stderr.write('ERROR: Can not create output directory\n')
                sys.exit(1)
        
        # start thread for reading and writing queued results
        self.results_writer = ResultWriter(self.results_queue, self.output_dir)
        self.results_writer.setDaemon(True)
        self.results_writer.start()
        
        for i in range(self.num_agents):
            spacing = float(self.rampup) / float(self.num_agents)
            if i > 0:  # first agent starts right away
                time.sleep(spacing)
            if self.running:  # in case stop() was called before all agents are started
                agent = LoadAgent(i, self.interval, self.log_msgs, self.output_dir, self.runtime_stats, self.error_queue, self.msg_queue, self.results_queue)
                agent.start()
                self.agent_refs.append(agent)
                agent_started_line = 'Started agent ' + str(i + 1) 
                if sys.platform.startswith('win'):
                    sys.stdout.write(chr(0x08) * len(agent_started_line))  # move cursor back so we update the same line again
                    sys.stdout.write(agent_started_line)
                else:
                    esc = chr(27) # escape key
                    sys.stdout.write(esc + '[G')
                    sys.stdout.write(esc + '[A')
                    sys.stdout.write(agent_started_line + '\n')
        if sys.platform.startswith('win'):
            sys.stdout.write('\n')
        print '\nAll agents running...\n\n'
        self.agents_started = True
        
    
    def stop(self):
        self.running = False
        for agent in self.agent_refs:
            agent.stop()
        
        if WAITFOR_AGENT_FINISH:
            keep_running = True
            while keep_running:
                keep_running = False
                for agent in self.agent_refs:
                    if agent.isAlive():
                        keep_running = True
                        time.sleep(0.1)

        self.results_writer.stop()
        
        if GENERATE_RESULTS:
            # pickle dictionaries to files for results post-processing        
            self.store_for_post_processing(self.output_dir, self.runtime_stats, self.workload)  
            
            # auto-generate results from a new thread when the test is stopped
            self.results_gen = results.ResultsGenerator(self.output_dir, self.test_name)
            self.results_gen.setDaemon(True)
            self.results_gen.start()


    def add_req(self, req):
        self.msg_queue.append(req)
