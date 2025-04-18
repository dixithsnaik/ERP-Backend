FROM python:3.11-buster

COPY google-cloud-sdk google-cloud-sdk 

# Add gcloud to PATH
ENV PATH=$PATH:/google-cloud-sdk/bin

# adding poetry
RUN pip install poetry==2.1.1

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
