FROM python:3.10-slim

WORKDIR /app
COPY honey-rui.py /app

CMD ["python3", "honey-rui.py"]
