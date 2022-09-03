from typing import Any
from io import BytesIO
from fastapi.responses import (
    Response, StreamingResponse, JSONResponse)

from .files import ImageServeCache

JSON, STREAM = "json", "stream"


class ResponseFactory:
    buffer: Any

    def __init__(self, maker):
        self.maker = maker
        self.target: ImageServeCache = ImageServeCache()


class JSONResponseFactory(ResponseFactory):
    def get_buffer(self):
        self.buffer = self.target.path
        return self.buffer

    def get_response(self) -> Response:
        return JSONResponse({
            "wcloud": str(self.target.url),
            "stopwords": self.maker._stopwords,
            "counter": self.maker._counter
        })


class StreamingResponseFactory(ResponseFactory):
    def get_buffer(self):
        self.buffer = BytesIO()
        return self.buffer

    def get_response(self) -> Response:
        self.buffer.seek(0)
        headers = {
            'Content-Disposition': f'attachment; filename="{self.target.filename}"'
        }
        return StreamingResponse(self.buffer, headers=headers)


class ResponseHelper:
    def __init__(self, maker: Any):
        self.maker = maker

    def __call__(self):
        reponse_factory = {
            JSON: JSONResponseFactory,
            STREAM: StreamingResponseFactory
        }.get(self.maker.params.response_type, JSONResponseFactory)(self.maker)
        return (reponse_factory.get_buffer(),
            reponse_factory.get_response
        )
