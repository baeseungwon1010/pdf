#!/usr/bin/env bash
set -euo pipefail

gunicorn -b 127.0.0.1:5006 private.internal_processor_app:app \
  --workers 1 --threads 2 --timeout 120 &

exec gunicorn -b 0.0.0.0:5005 private.uploader_app:app \
  --workers 1 --threads 4 --timeout 120
