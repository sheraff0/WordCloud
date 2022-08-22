from dataclasses import dataclass
import re
import json
from collections import Counter

from fastapi import UploadFile

MOST_COMMON_NUMBER = 100
MIN_WORDS_COLLECTION = 10


@dataclass
class WCMaker:
    text_file: UploadFile | None
    hash: str
    stopwords: str = "[]"
    lang: str = None

    async def __call__(self):
        await self.prepare_text()
        if not self._text:
            self.output = JSONResponse({"message": "No text file"})
            return
        if len(self._words) < MIN_WORDS_COLLECTION:
            self.output = JSONResponse({"message": "Non-imaginable text"})
            return
        # await self.make_image_mask()
        self.set_wcloud()
        self.generate_cloud()
        self.plot_cloud_to_buffer()
        self.make_output()
