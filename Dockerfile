# Use a base Python image with the required packages
FROM python:3.9-slim-buster

# Install any necessary dependencies
RUN apt-get update && apt-get install -y git

# Clone the OpenAI Python client library
RUN git clone https://github.com/openai/openai-python.git && cd openai-python && git checkout main && pip install .

# Set the working directory
WORKDIR /app

# copy files to working directory
COPY requirements.txt .
COPY src/pycrust.py src/
COPY scripts/download_dependencies.sh scripts/

# Install any required Python packages
RUN pip install -r requirements.txt

# Set the entry point for the container
ENTRYPOINT ["python3", "src/pycrust.py"]
