#!/bin/bash

# Build Docker container
docker build -t keras_doctr_testing .

# Run the container
docker run -it --rm keras_doctr_testing

