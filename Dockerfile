FROM python:3.7

RUN pip install "PyGithub>=1.55,<2.0"

COPY ./app /app

CMD ["python3", "/app/main.py"]
