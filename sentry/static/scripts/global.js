function varToggle(link, id) {
    $('#v' + id).toggle();
    var s = link.getElementsByTagName('span')[0];
    var uarr = String.fromCharCode(0x25b6);
    var darr = String.fromCharCode(0x25bc);
    s.innerHTML = s.innerHTML == uarr ? darr : uarr;
    return false;
}

function getQueryParams()
{
    var vars = {}, hash;
    var href = window.location.href;
    var hashes = href.slice(href.indexOf('?') + 1, (href.indexOf('#') !== -1 ? href.indexOf('#') : href.length)).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars[hash[0]] = hash[1];
    }
    return vars;
}

(function() {
  /**
   * @private
   */
  var prioritySortLow = function(a, b) {
    return b.priority - a.priority;
  };

  /**
   * @private
   */
  var prioritySortHigh = function(a, b) {
    return a.priority - b.priority;
  };

  /**
   * @constructor
   * @class Queue manages a queue of elements with priorities. Default
   * is highest priority first.
   *
   * @param [options] If low is set to true returns lowest first.
   */
  Queue = function(options) {
    var contents = [];

    var sorted = false;
    var sortStyle;
    if(options === undefined) {
        options = {};
    }

    if(options.low) {
      sortStyle = prioritySortLow;
    } else if(options.high) {
      sortStyle = prioritySortHigh;
    }

    /**
     * @private
     */
    var sort = function() {
      contents.sort(sortStyle);
      sorted = true;
    };

    var self = {
      /**
       * Removes and returns the next element in the queue.
       * @member Queue
       * @return The next element in the queue. If the queue is empty returns
       * undefined.
       *
       * @see PrioirtyQueue#top
       */
      pop: function() {
        if(!sorted && sortStyle) {
          sort();
        }

        var element = contents.pop();

        if(element) {
          return element.object;
        } else {
          return undefined;
        }
      },

      /**
       * Returns but does not remove the next element in the queue.
       * @member Queue
       * @return The next element in the queue. If the queue is empty returns
       * undefined.
       *
       * @see Queue#pop
       */
      top: function() {
        if(!sorted) {
          sort();
        }

        var element = contents[contents.length - 1];

        if(element) {
          return element.object;
        } else {
          return undefined;
        }
      },

      /**
       * @member Queue
       * @param object The object to check the queue for.
       * @returns true if the object is in the queue, false otherwise.
       */
      includes: function(object) {
        for(var i = contents.length - 1; i >= 0; i--) {
          if(contents[i].object === object) {
            return true;
          }
        }

        return false;
      },

      /**
       * @member Queue
       * @param object The object to check the queue for.
       * @returns true if the object was replaced, false if it was pushed.
       */
      replace: function(object, priority, key) {
        for(var i = contents.length - 1; i >= 0; i--) {
          if(contents[i].object[key] === object[key]) {
            contents[i] = {object: object, priority: priority};
            return true;
          }
        }
        self.push(object, priority);
        return false;
      },

      /**
       * @member Queue
       * @returns the current number of elements in the queue.
       */
      size: function() {
        return contents.length;
      },

      /**
       * @member Queue
       * @returns true if the queue is empty, false otherwise.
       */
      empty: function() {
        return contents.length === 0;
      },

      /**
       * @member Queue
       * @param object The object to be pushed onto the queue.
       * @param priority The priority of the object.
       */
      push: function(object, priority) {
        contents.push({object: object, priority: priority});
        sorted = false;
      }
    };

    return self;
  };
})();

/**
 * Date.parse with progressive enhancement for ISO 8601 <https://github.com/csnover/js-iso8601>
 * © 2011 Colin Snover <http://zetafleet.com>
 * Released under MIT license.
 */
(function (Date, undefined) {
    var origParse = Date.parse, numericKeys = [ 1, 4, 5, 6, 7, 10, 11 ];
    Date.parse = function (date) {
        var timestamp, struct, minutesOffset = 0;

        // ES5 §15.9.4.2 states that the string should attempt to be parsed as a Date Time String Format string
        // before falling back to any implementation-specific date parsing, so that's what we do, even if native
        // implementations could be faster
        //              1 YYYY                2 MM       3 DD           4 HH    5 mm       6 ss        7 msec        8 Z 9 ±    10 tzHH    11 tzmm
        if ((struct = /^(\d{4}|[+\-]\d{6})(?:-(\d{2})(?:-(\d{2}))?)?(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{3}))?)?(?:(Z)|([+\-])(\d{2})(?::(\d{2}))?)?)?$/.exec(date))) {
            // avoid NaN timestamps caused by "undefined" values being passed to Date.UTC
            for (var i = 0, k; (k = numericKeys[i]); ++i) {
                struct[k] = +struct[k] || 0;
            }

            // allow undefined days and months
            struct[2] = (+struct[2] || 1) - 1;
            struct[3] = +struct[3] || 1;

            if (struct[8] !== 'Z' && struct[9] !== undefined) {
                minutesOffset = struct[10] * 60 + struct[11];

                if (struct[9] === '+') {
                    minutesOffset = 0 - minutesOffset;
                }
            }

            timestamp = Date.UTC(struct[1], struct[2], struct[3], struct[4], struct[5] + minutesOffset, struct[6], struct[7]);
        }
        else {
            timestamp = origParse ? origParse(date) : NaN;
        }

        return timestamp;
    };
}(Date));

if (Sentry === undefined) {
    var Sentry = {};
}

(function(){
    Sentry.options = {
        urlPrefix: '',
        mediaUrl: '/media/',
        defaultImage: '/media/images/sentry.png'
    };

    Sentry.config = function(data){
        $.each(data, function(k, v){
            Sentry.options[k] = v;
        });
    };

    Sentry.prettyDate = function(date_str) {
        // we need to zero out at CST
        var time = Date.parse(date_str);
        var now = new Date();
        var now_utc = Date.UTC(
            now.getUTCFullYear(),
            now.getUTCMonth(),
            now.getUTCDate(),
            now.getUTCHours(),
            now.getUTCMinutes(),
            now.getUTCSeconds()
        );

        var seconds = (now_utc - time) / 1000;
        // var offset = (new Date().getTimezoneOffset() - 300) * 60;
        // seconds = seconds + offset;
        var token = 'ago';
        var time_formats = [
          [60, 'just now', 'just now'], // 60
          [120, '1 minute ago', '1 minute from now'], // 60*2
          [3600, 'minutes', 60], // 60*60, 60
          [7200, '1 hour ago', '1 hour from now'], // 60*60*2
          [86400, 'hours', 3600], // 60*60*24, 60*60
          [172800, 'yesterday', 'tomorrow'], // 60*60*24*2
          [604800, 'days', 86400], // 60*60*24*7, 60*60*24
          [1209600, 'last week', 'next week'], // 60*60*24*7*4*2
          [2419200, 'weeks', 604800], // 60*60*24*7*4, 60*60*24*7
          [4838400, 'last month', 'next month'], // 60*60*24*7*4*2
          [29030400, 'months', 2419200], // 60*60*24*7*4*12, 60*60*24*7*4
          [58060800, 'last year', 'next year'], // 60*60*24*7*4*12*2
          [2903040000, 'years', 29030400], // 60*60*24*7*4*12*100, 60*60*24*7*4*12
          [5806080000, 'last century', 'next century'], // 60*60*24*7*4*12*100*2
          [58060800000, 'centuries', 2903040000] // 60*60*24*7*4*12*100*20, 60*60*24*7*4*12*100
        ];
        var list_choice = 1;

        if (seconds < 0)
        {
            seconds = Math.abs(seconds);
            token = 'from now';
            list_choice = 2;
        }

        for (var i=0, format; (format = time_formats[i]); i++) {
            if (seconds < format[0])
            {
                if (typeof format[2] == 'string')
                    return format[list_choice];
                else
                    return Math.floor(seconds / format[2]) + ' ' + format[1] + ' ' + token;
            }
        }
        return time;
    };

    Sentry.prettyDates = function() {
        $('.pretty-date').each(function(_, el){
            var $el = $(el);
            var title = $el.attr('title');
            if (title) {
                var date = Sentry.prettyDate(title);
                if (date) {
                    $el.text(date);
                }
            }
        });
    };

    $(document).ready(function(){
        $('.filter-list').each(function(_, el){
            var $el = $(el);
            if ($el.find('li').length > 6) {
                // rebuild this widget as a dropdown select
                var select = $('<select></select>');
                var parent = $('<div class="filter-select sidebar-module">').appendTo($el.parent());

                $el.find('li a').each(function(_, a){
                    a = $(a);
                    var opt = $('<option value="' + a.attr('href') + '">' + a.text() + '</option>').appendTo(select);
                    if (a.parent().hasClass('active')) {
                        opt.attr('selected', 'selected');
                    }
                });
                $el.remove();
                select.appendTo(parent).change(function(){
                    window.location.href = $(this).val();
                });
            }
        });

        // Update date strings periodically
        setInterval(Sentry.prettyDates, 5000);
        Sentry.prettyDates();
    });

    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $(document).ready(function(){
        $('.client-platform-list a').click(function(){
            var $modal = $('#modal');
            var $this = $(this);
            var title = $this.attr('title') || $this.text();
            var href = $this.attr('href');

            $.ajax({
                dataType: 'html',
                url: href,
                success: function(data){
                    $('.modal-header h3', $modal).html(title + ' <small><a href="' + href + '">expand</a></small>');
                    $('.modal-body', $modal).html(data);
                    $modal.modal({
                        keyboard:true,
                        backdrop:false
                    });
                }
            });

            return false;
        });
    });

    $('.popup').live('click', function(){
        var $this = $(this);
        var $window = $(window);
        var $container = $($this.attr('data-container'));
        var title = $this.attr('data-title') || 'Untitled';
        var content = $container.html();
        var height = Math.min($window.height() - 100, $container.height() + 40);
        var width = Math.min($window.width() - 100, $container.width() + 40);
        var w = window.open("about:blank", "dsqApiExpand", "toolbar=0,status=0,location=0,menubar=0,height=" + height + ",width=" + width);
        w.document.write("<!DOCTYPE html><html>" +
            "<head>" +
                "<title>" + title + "</title>" +
                "<link href=\"" + Sentry.options.popupCss + "\" rel=\"stylesheet\" type=\"text/css\"/>" +
            "</head><body>" +
                "<div id=\"popup\">" + content + "</div></body>" +
            "</html>");
    });

}());
if (Sentry === undefined) {
    var Sentry = {};
}
(function(){
    function getRankedPosition(list, value, idx) {
        for (var i=0, item; (item = list[i]); i++) {
            if (value > item[idx]) {
                return i;
            }
        }
        return -1;
    }
    function getPosition(list, value, idx) {
        for (var i=0, item; (item = list[i]); i++) {
            if (value == item[idx]) {
                return i;
            }
        }
        return -1;
    }
    Sentry.realtime = {};
    Sentry.realtime.options = {
        viewId: null,
        projectId: null
    };
    Sentry.realtime.status = false;
    Sentry.realtime.queue = Queue({high: true});

    Sentry.realtime.init = function(){
        var sorted = [];
        $('#event_list .event').each(function(i, el){
            var $el = $(el);
            sorted.push([$el.attr('data-score'), $el.attr('id')]);
        });
        Sentry.realtime.events = sorted;

        $('#sentry-realtime').click(function(){
            if (Sentry.realtime.status) {
                Sentry.realtime.disable();
            } else {
                Sentry.realtime.enable();
            }
        });
        Sentry.realtime.poll();
        setInterval(Sentry.realtime.tick, 300);
    };

    Sentry.realtime.config = function(data){
        $.each(data, function(k, v){
            Sentry.realtime.options[k] = v;
        });
    };

    Sentry.realtime.toggle = function(){
        if (Sentry.realtime.status) {
            Sentry.realtime.enable();
        } else {
            Sentry.realtime.disable();
        }
    };

    Sentry.realtime.enable = function(){
        var $el = $('#sentry-realtime');
        $el.removeClass('realtime-play');
        $el.addClass('realtime-pause');
        $el.text('Pause Feed');
        Sentry.realtime.status = true;
    };

    Sentry.realtime.disable = function(){
        var $el = $('#sentry-realtime');
        $el.addClass('realtime-play');
        $el.removeClass('realtime-pause');
        $el.text('Go Live');
        Sentry.realtime.status = false;
    };

    Sentry.realtime.tick = function(){
        if (Sentry.realtime.queue.empty()) {
            return;
        }
        var data = Sentry.realtime.queue.pop();
        var id = 'group_' + data.id;
        var $row = $('#' + id);
        var is_new = ($row.length === 0);

        // ensure "no messages" is cleaned up
        $('#no_messages').remove();

        // resort because we suck at javascript
        Sentry.realtime.events.sort(function(a, b){
            return b[0] - a[0];
        });

        // if the row already was present, let's make sure
        // the count changed
        if (!is_new) {
            if ($row.attr('data-count') == data.count) {
                return;
            }
        }

        // get the ranked position based on data.score
        pos = getRankedPosition(Sentry.realtime.events, data.score, 0);

        // check to see if the row already exists in the sort,
        // and get the current position
        old_pos = getPosition(Sentry.realtime.events, id, 1);

        // if the row was already present, adjust its score
        if (old_pos !== -1) {
            Sentry.realtime.events[old_pos][0] = data.score;
            if (old_pos == pos) {
                return;
            }
            $row.remove();
        } else if (!is_new) {
            $row.remove();
        }

        $row = $(data.html);

        // if the row doesnt outrank any existing elements
        if (pos === -1) {
            $('#event_list').append($row);
        } else {
            $('#' + Sentry.realtime.events[pos][1]).before($row);
        }

        // insert it into the events list at the current position
        if (is_new) {
            Sentry.realtime.events.splice(pos, 0, [data.score, id]);
        }

        // shiny fx
        $row.css('background-color', '#ddd').animate({backgroundColor: '#fff'}, 1200);
    };

    Sentry.realtime.poll = function(){
        if (!Sentry.realtime.status) {
            setTimeout(Sentry.realtime.poll, 1000);
            return;
        }
        data = getQueryParams();
        data.view_id = Sentry.realtime.options.viewId || undefined;
        data.cursor = Sentry.realtime.cursor || undefined;
        $.ajax({
            url: Sentry.options.urlPrefix + '/api/' + Sentry.realtime.options.projectId + '/poll/',
            type: 'get',
            dataType: 'json',
            data: data,
            success: function(groups){
                if (!groups.length) {
                    setTimeout(Sentry.realtime.poll, 5000);
                    return;
                }
                Sentry.realtime.cursor = groups[groups.length - 1].score || undefined;
                $(groups).each(function(i, data){
                    Sentry.realtime.queue.replace(data, data.score, 'id');
                });
                setTimeout(Sentry.realtime.poll, 1000);
            },
            error: function(){
                // if an error happened lets give the server a bit of time before we poll again
                setTimeout(Sentry.realtime.poll, 10000);
            }
        });

        // make sure we limit the number shown
        while (Sentry.realtime.events.length > 50) {
            var item = Sentry.realtime.events.pop();
            $("#" + item[1]).remove();
        }
    };

    $(document).ready(function(){
        Sentry.realtime.init();
    });

}());if (Sentry === undefined) {
    var Sentry = {};
}
(function(){
    Sentry.charts = {};
    Sentry.charts.render = function(el, project_id, group_id, grid){
        var $sparkline = $(el);

        if ($sparkline.length < 1) {
            return; // Supress an empty chart
        }

        $.ajax({
            url: Sentry.options.urlPrefix + '/api/' + project_id + '/chart/',
            type: 'get',
            dataType: 'json',
            data: {
                days: 1,
                gid: group_id || undefined
            },
            success: function(data){
                var start = new Date().getTime() - data.length * 3600000;
                var pairs = [];
                // for (var i=0; i<1000; i++) {
                //     pairs.push([start + (3600 * 1000) * i, Math.random()*1000]);
                // }
                for (var i=0; i<data.length; i++) {
                    pairs.push([start + (3600 * 1000) * i, data[i]]);
                }
                $sparkline.height($sparkline.parent().height());
                $.plot($sparkline, [
                    {
                        data: pairs,
                        color: '#3079d0',
                        shadowSize: 0,
                        lines: {
                            lineWidth: 1,
                            show: true,
                            fill: true
                        }
                    }
                ], {
                    xaxis: {
                       mode: "time"
                    },
                    grid: {
                        show: grid || false,
                        borderColor: '#dddddd',
                        borderWidth: 1,
                        backgroundColor: '#F5F5F5'
                    },
                    lines: { show: false }

                });
            }
        });
    };
}());if (Sentry === undefined) {
    var Sentry = {};
}
(function(){
    Sentry.notifications = {};
    Sentry.notifications.status = false;

    Sentry.notifications.enable = function(){
        // if (window.webkitNotifications.checkPermission()) {
        //     Sentry.notifications.status = true;
        //     $('#sentry_notify').text('Disable Notifications');
        // } else {
        window.webkitNotifications.requestPermission(function(){
            Sentry.notifications.status = true;
            Sentry.notifications.show({'type': 'simple', 'title': 'Sentry', 'body': 'Notifications have been enabled.'});
            $('#sentry_notify').text('Disable Notifications');
        });
        // }
    };

    Sentry.notifications.disable = function(){
        Sentry.notifications.status = false;
        $('#sentry_notify').text('Enable Notifications');
    };

    Sentry.notifications.show = function(options){
        if (!Sentry.notifications.status) return;

        var note;

        if (options.type == 'html') {
            note = window.webkitNotifications.createHTMLNotification(options.url);
        } else {
            note = window.webkitNotifications.createNotification(options.image || Sentry.options.defaultImage, options.title, options.body);
        }
        note.ondisplay = function() {
            setTimeout(function(){ note.cancel(); }, 10000);
        };
        note.show();
    };

    $(document).ready(function(){
        if (window.webkitNotifications){
            Sentry.notifications.status = (window.webkitNotifications.checkPermission() > 0);
            $('<li><a id="sentry_notify" href="javascript:void()">' + (Sentry.notifications.status ? 'Disable Notifications' : 'Enable Notifications') + '</a></li>').click(function(){
                if (Sentry.notifications.status) {
                    Sentry.notifications.disable();
                } else {
                    Sentry.notifications.enable();
                }
            }).prependTo('#account');
        }
    });
}());if (Sentry === undefined) {
    var Sentry = {};
}
(function(){
    Sentry.stream = {};
    Sentry.stream.clear = function(project_id) {
        if (confirm("Are you sure you want to mark all your stream as resolved?")) {
            $.ajax({
                url: Sentry.options.urlPrefix + '/api/' + project_id + '/clear/',
                type: 'post',
                dataType: 'json',
                success: function(groups){
                    window.location.reload();
                }
            });
        }
    };
    Sentry.stream.resolve = function(project_id, gid, remove){
        if (typeof(remove) == 'undefined') {
            remove = true;
        }
        $.ajax({
            url: Sentry.options.urlPrefix + '/api/' + project_id + '/resolve/',
            type: 'post',
            dataType: 'json',
            data: {
                gid: gid
            },
            success: function(groups){
                for (var i=groups.length-1, el, row; (el=groups[i]); i--) {
                    var id = el[0];
                    var data = el[1];
                    $('#group_' + id).remove();
                    if (!remove) {
                        $('#event_list').prepend(data.html);
                        $('#group_' + id).addClass('fresh');
                    }
                }
            }
        });
    };
    Sentry.stream.bookmark = function(project_id, gid, el){
        $.ajax({
            url: Sentry.options.urlPrefix + '/api/' + project_id + '/bookmark/',
            type: 'post',
            dataType: 'json',
            data: {
                gid: gid
            },
            success: function(data){
                if (!el) {
                    return;
                }
                var $el = $(el);
                if (data.bookmarked) {
                    $el.addClass('checked');
                } else {
                    $el.removeClass('checked');
                }
            }
        });
    };
}());