FROM python:3.13 AS builder
WORKDIR /app

# create and active environment (venv)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim AS runtime
WORKDIR /user/local/app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy in the source code
COPY . .
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


