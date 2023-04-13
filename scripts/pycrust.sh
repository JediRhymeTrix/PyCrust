#!/bin/bash

# Get the path to the input file from the command-line arguments
INPUT_FILE=$1

# Check if the input file exists
if [ ! -f $INPUT_FILE ]; then
  echo "Error: Input file $INPUT_FILE does not exist"
  exit 1
fi

# Check if the OpenAI API key is set
if [ -z $OPENAI_API_KEY ]; then
  echo "Error: OPENAI_API_KEY environment variable is not set"
  exit 1
fi

# Run the transpiler using Docker Compose
INPUT_FILE=$(realpath $INPUT_FILE)
export INPUT_FILE
export OPENAI_API_KEY
docker-compose run --rm pycrust
