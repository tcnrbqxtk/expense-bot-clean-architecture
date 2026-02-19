FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv
RUN uv sync

CMD ["uv", "run", "src/main.py"]
