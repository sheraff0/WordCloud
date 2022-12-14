from pathlib import Path
from datetime import datetime

FILES_ROOT = "/temp"
BASE_URL = "temp"
TEXT_INDEX_ROOT = "text_index"


class FileResource:
    root = Path(FILES_ROOT)
    path: Path = None
    data: str | bytes = None
    bytes: str = ""  # "b" if bytes

    def exists(self):
        if self.path:
            return self.path.exists()

    def read(self):
        if self.exists():
            b = self.bytes
            with open(self.path, f'r{b}') as f:
                self.data = f.read()
            return self.data

    def save(self):
        if self.path and self.data:
            b = self.bytes
            with open(self.path, f'w{b}') as f:
                f.write(self.data)


class TextIndex(FileResource):
    def __init__(self, hash: str, text: str = ""):
        self.path = self.root / TEXT_INDEX_ROOT / hash
        self.data = text


class FileServeCache(FileResource):
    filename: str
    url: str
    path: Path
    filename_base: str = "file.ext"

    def __init__(self):
        self.set()

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

    def set_filename(self):
        base = self.filename_base
        *name, ext = base.split(".")
        name = "_".join(name)
        timestamp = self.get_timestamp()
        self.filename = f"{name}_{timestamp}.{ext}"

    def set_url(self):
        self.url = Path(BASE_URL) / self.filename

    def set_path(self):
        self.path = self.root / self.filename

    def set(self):
        self.set_filename()
        self.set_url()
        self.set_path()


class ImageServeCache(FileServeCache):
    filename_base = "image.png"
