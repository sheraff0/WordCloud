import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

from .stopwords import STOPWORDS

MIN_XML_TEXT_RATIO = 0.3
MAX_WORD_LENGTH = 22


@dataclass
class TextProcessor:
    raw_utf8: str
    _text: str = None
    _words: list[str] = field(default_factory=lambda: [])

    def read_cleaned_text(self):
        if _text := TextIndex(self.hash, None).read():
            print("Read from INDEX")
            self._text = _text
            return self._text

    def save_cleaned_text(self):
        TextIndex(self.hash, self._text).save()

    def set_stopwords(self):
        self._stopwords = json.loads(self.stopwords)
        if (self._stopwords is None) and self.lang:
            print(f"{self.lang} - default STOPWORDS")
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
            r'\s{2,}', ' ', self._text)

    def clean_text(self):
        self.parse()
        self.remove_long_strings()
        self.clear_non_alpfa()
        self.deflate()
        self.save_cleaned_text()
        print("PARSED")

    def set_words_collection(self):
        self._words = self._text.split(' ')
        self._counter = Counter(self._words).most_common(MOST_COMMON_NUMBER)

    def clear_stopwords(self):
        if self._stopwords:
            re_options = "|".join(self._stopwords)
            pattern = re.compile(f"[{re_options}]'")
            self._text = re.sub(pattern, ' ', self._text)

    async def prepare_text(self):
        self.set_stopwords()
        try:
            if not self.read_cleaned_text():
                await self.read_file()
                self.clean_text()
            self.set_words_collection()
            self.clear_stopwords()
        except Exception as e:
            print(e)
