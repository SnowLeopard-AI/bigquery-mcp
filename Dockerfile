FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv pip compile pyproject.toml --output-file requirements.txt

COPY src/ src/
RUN uv build


FROM python:3.13-alpine

WORKDIR /app
COPY --from=builder /build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /build/dist/*.whl ./
RUN pip install --no-deps ./*.whl

ENTRYPOINT ["sl-bigquery-mcp"]
CMD ["--help"]