from jophiel.crawler.w3lib.url import file_uri_to_path
from jophiel.crawler.responsetypes import responsetypes

class FileDownloadHandler(object):
    
    def download_request(self, request):
        filepath = file_uri_to_path(request.url)
        body = open(filepath, 'rb').read()
        respcls = responsetypes.from_args(filename=filepath, body=body)
        return respcls(url=request.url, body=body)
