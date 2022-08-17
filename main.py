from fastapi import (
    FastAPI, Request,
    File, Form, UploadFile
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from wcloud import WCMaker


app = FastAPI()

# Static
app.mount("/temp", StaticFiles(directory="temp"), name="temp")
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

templates = Jinja2Templates(directory="frontend/dist")


@app.post("/upload")
async def upload_files(
    text_file: UploadFile = File(description="Source text for word cloud"),
    lang: str = Form(),
    stopwords: str = Form(),
    # image_file: UploadFile = File(description="Image mask for word cloud"),
):
    wc = WCMaker(
        text_file=text_file,
        #image_file=images_file,
        lang=lang,
        stopwords=stopwords,
        response_type="json"
    )
    await wc()
    return wc.output


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
