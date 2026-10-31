FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir uv==0.13.6
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app ./app
COPY data ./data
CMD ["uv", "run", "--frozen", "--no-dev", "python", "-m", "app.cli", "demo"]
