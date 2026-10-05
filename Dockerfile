# ==========================================
# DataLens AI - Backend Dockerfile
# ==========================================

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies
RUN uv sync --frozen --no-dev

# Copy backend source code
COPY src ./src

# Create runtime directories
RUN mkdir -p data/uploads reports/generated reports/eda

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]