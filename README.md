# Word Cloud

#### Build a word cloud from you favorite book, diary or web page in two clicks!

[`Sample web app`](https://wordcloud.7-gor.ru)

Features:
-
- easily manipulate non-representative "stop words"


Used libraries
-
- backend based on Python [`wordcloud`](https://github.com/amueller/word_cloud) and [`FastAPI`](https://fastapi.tiangolo.com)
- frontend based on [`Svelte`](https://svelte.dev)

Installation
-
### Local
- run project in a dedicated python environment, with pre-installed packages listed in `requirements.txt`:
`python bot.py`

### Production
- edit `.envs` file:

`DOMAIN_NAME=<your_domain>`

`STATIC_HOST=<your_domain>`

### Frontend
- source code and components are located in `frontend/src`
- to re-build frontend for FastAPI server, run:

`npm install`

`npm run build`

Buid frontend files will be served from `frontend/dist` folder.
