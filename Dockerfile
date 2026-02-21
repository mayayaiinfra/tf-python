# THUNDERFIRE Python SDK / MCP Server
FROM python:3.12-slim

LABEL org.opencontainers.image.title="THUNDERFIRE Python SDK"
LABEL org.opencontainers.image.description="Python SDK with MCP server for autonomous node management"
LABEL org.opencontainers.image.source="https://github.com/mayayaiinfra/tf-python"
LABEL org.opencontainers.image.vendor="MAYAYAI"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .[mcp]

# Create non-root user
RUN groupadd -g 1001 thunderfire && \
    useradd -u 1001 -g thunderfire -m thunderfire

USER thunderfire

# Environment
ENV THUNDERFIRE_API_URL=http://localhost:8080
ENV THUNDERFIRE_TIMEOUT=30000

ENTRYPOINT ["thunderfire-mcp"]
