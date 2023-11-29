FROM python:3.11

COPY . .

RUN pip install --upgrade -r requirements.txt

CMD ["sh", "-c", "python app.py --host 0.0.0.0 --port ${PORT:-${WEBSITES_PORT:-8080}}"]