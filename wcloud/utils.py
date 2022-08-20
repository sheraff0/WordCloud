from typing import Union
from io import BytesIO

from fastapi import File, UploadFile

CHUNK_SIZE = 1024


async def read_by_chunks(file: UploadFile) -> Union[BytesIO, None]:
    if file:
        buffer = BytesIO()
        while content := await file.read(CHUNK_SIZE):
            buffer.write(content)
        return buffer.getbuffer()
