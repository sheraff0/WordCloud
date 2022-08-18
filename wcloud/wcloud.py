from dataclasses import dataclass, field
from io import BytesIO
import re
import json
from datetime import datetime
from pathlib import Path
from collections import Counter

import PIL
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

import matplotlib.pyplot as plt
import numpy as np

from fastapi import File, UploadFile
from fastapi.responses import (
    Response, StreamingResponse, JSONResponse)
from wordcloud import WordCloud

from .settings import *
from .stopwords import STOPWORDS

JSON, STREAM = "json", "stream"

MIN_XML_TEXT_RATIO = 0.3
MIN_WORDS_COLLECTION = 10
MOST_COMMON_NUMBER = 100
MAX_WORD_LENGTH = 22


@dataclass
class ResponseMixin:
    response_type: str = JSON

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

    def get_filename(self, base="wcloud.png"):
        *name, ext = base.split(".")
        name = "_".join(name)
        timestamp = self.get_timestamp()
        return f"{name}_{timestamp}.{ext}"

    def set_output_path(self):
        p = Path(APP_DIR)
        self.filename = self.get_filename()
        self.output_url = Path("temp") / self.filename
        self.output_path = p / self.output_url

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


@dataclass
class TextProcessMixin:
    text_file: UploadFile
    stopwords: str = "[]"
    lang: str = None
    _text: str = None
    _words: list[str] = field(default_factory=lambda: [])

    def set_stopwords(self):
        self._stopwords = json.loads(self.stopwords)
        if (not self._stopwords) and self.lang:
            self._stopwords = STOPWORDS.get(self.lang, [])

    async def read_file(self):
        self.text = await self.text_file.read()

    def parse_xml(self):
        self._text = self.text.decode("utf-8").lower()
        soup = ""
        try:
            soup = BeautifulSoup(self._text, 'xml')
            soup = soup.text
        except Exception as e:
            print(e)
        if len(soup) / len(self.text) >= MIN_XML_TEXT_RATIO:
            self._text = soup

    def parse_pdf(self):
        self.reader = PdfReader(BytesIO(self.text))
        self._text = "".join([
            page.extract_text()
            for page in self.reader.pages
        ]).lower()

    def parse(self):
        if self.text_file.filename.endswith(".pdf"):
            self.parse_pdf()
        else:
            self.parse_xml()

    def remove_long_strings(self):
        # clean potential binary objects
        length = str(MAX_WORD_LENGTH + 1)
        pattern = re.compile(
            '\S{' + length + ',}')
        self._text = re.sub(pattern, ' ', self._text)

    def clear_non_alpfa(self):
        self._text = re.sub(
            r'[\n\d\/\W\_]', ' ', self._text)

    def deflate(self):
        self._text = re.sub(
            r'\s+', ' ', self._text)

    def extract_text(self):
        self.set_stopwords()
        self.parse()
        self.remove_long_strings()
        self.clear_non_alpfa()
        self.deflate()

    def set_words_collection(self):
        self._words = self._text.split(' ')
        self._counter = Counter(self._words).most_common(MOST_COMMON_NUMBER)

    def clear_stopwords(self):
        if self._stopwords:
            re_options = "|".join(self._stopwords)
            pattern = re.compile(f"[{re_options}]'")
            self._text = re.sub(pattern, ' ', self._text)

    async def prepare_text(self):
        try:
            await self.read_file()
            self.extract_text()
            self.set_words_collection()
            self.clear_stopwords()
        except Exception as e:
            print(e)

@dataclass
class ImageProcessMixin:
    """For future development: use `input_mask`
    """
    image_file: UploadFile

    def get_image_mask(self, file):
        return np.array(
            PIL.Image.open(file))

    async def prepare_image_mask(self):
        self.image_mask = self.get_image_mask(
            self.image_file.file)


@dataclass
class WCMaker(
    ResponseMixin,
    TextProcessMixin,
    # ImageProcessMixin,
):
    wc_base_params: dict = field(default_factory=lambda: dict(
        background_color="white",
        max_words=2000,
        contour_width=3,
        contour_color="steelblue"
    ))

    def set_wcloud(self):
        self.wc = WordCloud(**dict(
            **self.wc_base_params,
            stopwords=set(self._stopwords),
            # mask=self.image_mask,
        ))

    def generate_cloud(self):
        self.wc.generate(self._text)

    def plot_cloud(self, destination):
        plt.figure()
        plt.imshow(self.wc, interpolation="bilinear")
        # plt.figure()
        # plt.imshow(self.image_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(destination)

    def plot_cloud_to_buffer(self):
        self.set_output_path()
        self.set_output_buffer()
        self.plot_cloud(self.output_buffer)

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
