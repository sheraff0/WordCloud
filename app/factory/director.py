from dataclasses import dataclass
from typing import Optional, List, Tuple
import re
import json
from collections import Counter

from fastapi import UploadFile
from fastapi.responses import JSONResponse

from .response import JSON, ResponseHelper
from .plot import Plotter
from .text import TextProcessor

MIN_WORDS_COLLECTION = 10


@dataclass
class WCMakerParams:
    text_file: Optional[UploadFile]
    hash: str
    stopwords: str = "[]"
    lang: str = None
    response_type: str = JSON


class WCMaker(
    TextProcessor,
    Plotter
):
    _text: str = ""
    _stopwords: List[str] = []
    _words: List[str] = []
    _counter: List[Tuple] = []

    def __init__(self, params: WCMakerParams):
        self.params = params

    def make_cloud(self, buffer):
        self.set_wcloud()
        self.generate_cloud()
        self.plot_cloud_to_buffer(buffer)

    async def __call__(self):
        await self.prepare_text()
        if not self._text:
            self.output = JSONResponse({"message": "No text file"})
            return
        if len(self._words) < MIN_WORDS_COLLECTION:
            self.output = JSONResponse({"message": "Non-imaginable text"})
            return
        # await self.make_image_mask()
        buffer, get_response = ResponseHelper(self)()
        self.make_cloud(buffer)
        self.output = get_response()
