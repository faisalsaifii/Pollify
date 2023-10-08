FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV PATH="/root/.cargo/bin:${PATH}"
CMD ["gunicorn", "-b", ":5000", "app:app"]