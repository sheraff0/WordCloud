from typing import Union
from fastapi import (
    FastAPI, Request,
    File, Form, UploadFile
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from .settings import *
from .wcloud import WCMaker, TextIndex


app = FastAPI()

# Static
app.mount("/temp", StaticFiles(directory=f"{APP_DIR}temp"), name="temp")
app.mount("/assets", StaticFiles(directory=f"{APP_DIR}frontend/dist/assets"), name="assets")

templates = Jinja2Templates(directory=f"{APP_DIR}frontend/dist")


# Views 
@app.post("/upload/")
async def upload_files(
    text_file: Union[UploadFile, None] = File(description="Source text for word cloud"),
    hash: str = Form(),
    lang: str = Form(),
    stopwords: str = Form(),
    # image_file: UploadFile = File(description="Image mask for word cloud"),
):
    wc = WCMaker(
        text_file=text_file,
        hash=hash,
        lang=lang,
        stopwords=stopwords,
        response_type="json"
    )
    await wc()
    return wc.output


class HashItem(BaseModel):
    hash: str


@app.post("/check-hash/")
async def check_hash(item: HashItem):
    exists = TextIndex(item.hash, None).exists()
    return {
        "textParsed": exists,
    }


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "static_host": STATIC_HOST
    })
