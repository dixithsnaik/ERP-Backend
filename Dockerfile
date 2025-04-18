FROM python:3.11-buster

# Install Poetry via curl (latest version)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set Poetry's binary path to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Install Google Cloud SDK
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh

# Add gcloud to PATH
ENV PATH=$PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Copy the rest of the project files after installing dependencies (avoids re-installing if code changes)
COPY . .

# Install dependencies using Poetry (Poetry installs in the working directory)
RUN poetry install

# Set environment variables for Flask (optional fallback)
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose the port Flask runs on
EXPOSE 5000

# Run Flask using Poetry
ENTRYPOINT ["poetry", "run", "python", "run.py"]