FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-root \
    && pip uninstall -y poetry

COPY src ./src

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "src.main"]