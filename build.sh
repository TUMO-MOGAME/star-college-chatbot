#!/bin/bash
# Install Python dependencies
pip install --upgrade pip
pip install -r requirements-server.txt

# Verify gunicorn is installed
which gunicorn || pip install gunicorn

# Print installed packages for debugging
pip list
