FROM python:3.11-buster

# Install Poetry and ensure it's on PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Install Google Cloud SDK
RUN curl -o /tmp/google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir -p /usr/local/gcloud && \
    tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz && \
    /usr/local/gcloud/google-cloud-sdk/install.sh

# Add gcloud to PATH
ENV PATH=$PATH:/usr/local/gcloud/google-cloud-sdk/bin

COPY . .

# Install dependencies using Poetry
RUN poetry install

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose the port Flask runs on
EXPOSE 5000

# Run Flask using Poetry
ENTRYPOINT ["poetry", "run", "python", "run.py"]
