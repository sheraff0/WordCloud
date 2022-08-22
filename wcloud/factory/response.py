from io import BytesIO
from fastapi.responses import (
    Response, StreamingResponse, JSONResponse)

from .files import FileServeCache

JSON, STREAM = "json", "stream"


class ResponseWrapper(FileServeCache):
    response_type: str = JSON

    def set_output_buffer(self):
        self.output_buffer = {
            JSON: self.output_path,
            STREAM: BytesIO()
        }.get(self.response_type, self.output_path)

    def get_stream_response(self) -> Response:
        headers = {
            'Content-Disposition': f'attachment; filename="{self.filename}"'
        }
        return StreamingResponse(self.output_buffer, headers=headers)

    def make_stream_output(self):
        self.output_buffer.seek(0)
        self.output = self.get_stream_response()

    def get_json_response(self) -> Response:
        return JSONResponse({
            "stopwords": self._stopwords,
            "wcloud": str(self.output_url),
            "counter": self._counter
        })

    def make_json_output(self):
        self.output = self.get_json_response()

    def make_output(self):
        {
            JSON: self.make_json_output,
            STREAM: self.make_stream_output
        }.get(self.response_type, self.make_json_output)()
