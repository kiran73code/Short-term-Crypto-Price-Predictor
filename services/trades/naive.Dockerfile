# Debian image for python
FROM python:3.12-slim-bookworm

# Install UV to python image 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# Run the python service
CMD ["uv", "run" ,"python", "run.py"]