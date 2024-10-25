FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install Flask

EXPOSE 8090

ENV FLASK_APP=app.py

CMD ["python3", "app.py"]
