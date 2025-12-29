FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

ARG ENVIRONMENT

WORKDIR /app
COPY src src

COPY ${ENVIRONMENT}.env* .
COPY ${ENVIRONMENT}.fastmcp.json fastmcp.json
RUN mv ${ENVIRONMENT}.env .env | true

COPY README.md README.md
COPY logging.yaml logging.yaml
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY .python-version ./.python-version

RUN uv sync --frozen

FROM python:3.12-slim AS runner

COPY --from=builder /bin/ /bin/
COPY --from=builder /app /app

WORKDIR /app
RUN mkdir -p ./logs | true

RUN useradd -m -u 10001 runneruser
RUN chown -R runneruser:runneruser /app
USER 10001

ENV PORT=8000
EXPOSE ${PORT}
ENTRYPOINT ["uv", "run", "fastmcp", "run"]
CMD []
