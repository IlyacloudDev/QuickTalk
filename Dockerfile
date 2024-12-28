FROM python:3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "cd QuickTalk && daphne -b 0.0.0.0 -p 8000 config.asgi:application"]
