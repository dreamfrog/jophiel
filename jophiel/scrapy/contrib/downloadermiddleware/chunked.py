from scrapy.utils.http import decode_chunked_transfer

from scrapy.middleware import BaseMiddleware

class ChunkedTransferMiddleware(BaseMiddleware):
    """This middleware adds support for chunked transfer encoding, as
    documented in: http://en.wikipedia.org/wiki/Chunked_transfer_encoding
    """

    def process_response(self, request, response, spider):
        if response.headers.get('Transfer-Encoding') == 'chunked':
            body = decode_chunked_transfer(response.body)
            return response.replace(body=body)
        return response
