FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

ARG ENVIRONMENT

WORKDIR /app
COPY src src

COPY ${ENVIRONMENT}.env ./.env
COPY ${ENVIRONMENT}.fastmcp.json fastmcp.json

COPY README.md README.md
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY .python-version ./.python-version

RUN uv sync --frozen

FROM python:3.12-slim AS runner

COPY --from=builder /bin/ /bin/
COPY --from=builder /app /home/runneruser

RUN groupadd -g 1001 runnergroup && \
    useradd -m -u 1001 -g 1001 runneruser

RUN mkdir -p ./logs

RUN chown -R 1001:1001 /home/runneruser

USER 1001:1001
ENTRYPOINT ["uv", "run", "fastmcp", "run"]
CMD []
