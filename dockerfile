FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN chmod +x /api/entrypoint.sh
RUN uv sync --locked
EXPOSE 8000

CMD ["/api/entrypoint.sh"]
