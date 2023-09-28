FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV SLACK_SIGNING_SECRET=a03a70d6a199de0eacba673064fe2947
ENV SLACK_BOT_TOKEN=xoxb-5649828779333-5718433923317-LYzQxfLcqAER14yqDwUwzaWE
CMD ["gunicorn", "-b", ":5000", "app:app"]