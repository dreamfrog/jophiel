# Description of the CrawlUri thrift structure

namespace py spyder.thrift.gen


/**
 * Some typedefs in order to make the code more readable.
 */
typedef i64 timestamp

typedef map<string,string> header

typedef map<string,string> key_value

/**
 * The main strcut for CrawlUris.
 * 
 * This contains some metadata and if possible the saved web page.
 */
struct CrawlUri {
    // readable version of the url to crawl
    1: string               url,

    // the effective url used for downloading the content (i.e.: IP instead of hostname)
    2: string               effective_url,

    // the host identifier used for queue selection
    3: i16                  current_priority,

    // when processing has been started
    4: timestamp            begin_processing,

    // when processing is finished
    5: timestamp            end_processing,

    // the http request headers
    6: header               req_header,

    // the http response headers
    7: header               rep_header

    // the saved content body
    8: string               content_body,

    // the servers status code
    9: i16                  status_code,

    // request time
    10: double              req_time,

    // queue time
    11: double              queue_time,

    // additional values from other processors
    12: key_value           optional_vars
}
