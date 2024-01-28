#!/bin/bash
# Run flake8 excluding the venv directory
echo "Running flake8..."
flake8 --exclude=.venv