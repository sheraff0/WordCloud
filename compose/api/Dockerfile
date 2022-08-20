FROM python:3.10-slim-buster

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN addgroup --system api \
    && adduser --system --ingroup api api

COPY --chown=api:api wcloud /app/wcloud
COPY --chown=api:api ./.env .env.local
COPY --chown=api:api ./frontend/dist /app/frontend/dist

COPY --chown=api:api ./compose/api/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN mkdir -p /app/temp /app/text_index
RUN chown api:api /app/temp /app/text_index

USER api
