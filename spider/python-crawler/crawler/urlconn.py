import urllib2
import urllib
import cookielib
import socket
import lxml.html    # python-lxml # http://codespeak.net/lxml/lxmlhtml.html
import time
import mimetypes
import mimetools
import os
from urllib2 import HTTPError

SOCKET_DEFAULT_TIMEOUT = 30

class URLConn:

    def __init__(self, cookie = None, timeout = None):
        # cookie
        if cookie == None:
            self.cookie = cookielib.LWPCookieJar() 
        else:
            self.cookie = cookie
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler, urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        # socket timeout
        if timeout == None:
            timeout = SOCKET_DEFAULT_TIMEOUT
        socket.setdefaulttimeout(timeout)
                
    def clean_cookie(self):
        self.cookie = cookielib.LWPCookieJar() 
       
    ################################################
    # upload a file to a url link
    ################################################
    def upload(self, url, filename, key):
        if not os.path.isfile(filename):
            return (False,'file is not exist')
        file_pointer_to_upload = open(filename,'r')
        file_data = file_pointer_to_upload.read()
        #, due to use of multipart, need the , when the tuple is of size 1
        #constructed_http_data = (('ALLDATA', filename, file_data),)
        constructed_http_data = ((key, filename, file_data),)
        req = self.build_request(url, {}, constructed_http_data)
        try: 
            response = urllib2.urlopen(req)
        except HTTPError, e:
            print e.code
            err =  e.read()
            return err,None
        try:
            returncode = response.read()
            return None, returncode
        except:
            #print response.info
            return "response err", None
    
    ###############################################
    # submit (form) data to a url 
    ###############################################
    def submit(self, url, data):
        return self.download(url, data)

    ###############################################
    # download html page from a url
    ###############################################
    def download(self, url, data = None):  #download the html page from server. 

        redirected_url = None
        error_msg = None
        html = None
        # 1. URL Request Head
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        if data != None:
            req = urllib2.Request(url, urllib.urlencode(data), headers)
        else:
            req = urllib2.Request(url, data, headers)
        # 2. URL Request
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                #raise HtmlPageError('[fetch] failed to reach a server.' + \
                #            ' Reason: '+ str(e.reason) )
                error_msg = 'network-error'
            elif hasattr(e, 'code'):
                #raise HtmlPageError('[fetch] server couldn\'t fulfill the request.'+\
                #            ' Error code: '+ str(e.code) )
                error_msg = 'server-error'
            else:
                #raise HtmlPageError('[fetch] URLError, unknown reason.')
                error_msg = 'other-error'
        except KeyboardInterrupt:
            raise
        except:
            #raise HtmlPageError('[fetch] Unexpected urlopen() error: ' + 
            #            str(sys.exc_info()[0]) )
            error_msg = 'urlopen-error'
        
        # 3. Read Html 
        if error_msg != None:
            return error_msg, url, redirected_url, html
        try:
            print response.info().headers
            html = response.read()
        except KeyboardInterrupt:
            raise
        except:
            #raise HtmlPageError('[fetch] Unexpected response.read() error: ' + \
            #            str(sys.exc_info()[0]) )
            error_msg = 'reading-error'

        # 4. check if there is a redirect
        if error_msg != None:
            #f = open("undownloaded_urls.log", 'a')
            #f.write(time.strftime("%Y/%m/%d %H:%M:%S") + "\t" + error_msg + "\t" + url + "\n")
            #f.close()
            return error_msg, url, redirected_url, html

        nurl = response.geturl()
        if url != nurl:
            redirected_url = nurl
        else:
            redirected_url = None            
        
        # 5. generate lxml.html object for future processing
        #self.html = lxml.html.fromstring(the_page)
        return error_msg, url, redirected_url, html

    def encode_multipart_formdata(self, fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
        """ Encodes fields and files for uploading.
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        Return (content_type, body) ready for urllib2.Request instance
        You can optionally pass in a boundary string to use or we'll let mimetools provide one.
        """    
        CRLF = '\r\n'
        L = []
        if isinstance(fields, dict):
            fields = fields.items()
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
    #        if not filetype.startswith('text'):
    #            L.append('Content-Transfer-Encoding: binary')
            L.append('Content-Type: %s' % filetype)
    #        L.append('Content-Length: %s\r\n' % str(len(value)))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY        # XXX what if no files are encoded
        return content_type, body


    def build_request(self, theurl, fields, files, txheaders=None):
        """Given the fields to set and the files to encode it returns a fully formed urllib2.Request object.
        You can optionally pass in additional headers to encode into the opject. (Content-type and Content-length will be overridden if they are set).
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.    
        """
        content_type, body = self.encode_multipart_formdata(fields, files)
        if not txheaders: txheaders = {}
        txheaders['Content-type'] = content_type
        txheaders['Content-length'] = str(len(body))
        return urllib2.Request(theurl, body, txheaders)


if __name__ == "__main__":
    import sys
    url = "http://www.colorado.edu/GraduateSchool/academics/_docs/transfercredit.pdf"
    urlconn = URLConn()
    msg,url,reurl, data =urlconn.download(url)
    f = open("dd.dat",'w')
    f.write(data)
    f.close()
    #link = "http://"
    #print urlconn.upload(link, sys.argv[1],"WIFI" )

    
