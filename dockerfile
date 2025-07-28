FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN chmod +x /api/entrypoint.sh
RUN apk add --no-cache libffi-dev openssl-dev gcc musl-dev python3-dev
RUN uv sync --locked
EXPOSE 8000

CMD ["/api/entrypoint.sh"]
