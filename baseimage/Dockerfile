FROM python:alpine
LABEL authors="ali"

RUN python -m pip install fastapi uvicorn sqlalchemy requests

WORKDIR /app
COPY main.py /app/
COPY run.sh /app/

CMD ["./run.sh"]
