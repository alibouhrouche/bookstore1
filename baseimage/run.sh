#!/bin/sh
python -m uvicorn main:app --root-path "$APP_ROOT" --proxy-headers --host 0.0.0.0 --port 80