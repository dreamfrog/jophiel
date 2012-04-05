from pprint import pformat
from celery.events.snapshot import Polaroid


class DumpCam(Polaroid):

    def on_shutter(self, state):
        if not state.event_count:
            # No new events since last snapshot.
            return
        print("Workers: %s" % (pformat(state.workers, indent=4), ))
        print("Tasks: %s" % (pformat(state.tasks, indent=4), ))
        print("Total: %s events, %s tasks" % (
            state.event_count, state.task_count))


from celery.events import EventReceiver
from celery.messaging import establish_connection
from celery.events.state import State

def main():
    state = State()
    with establish_connection() as connection:
        recv = EventReceiver(connection, handlers={"*": state.event})
        with DumpCam(state, freq=1.0):
            recv.capture(limit=None, timeout=None)

if __name__ == "__main__":
    main()
