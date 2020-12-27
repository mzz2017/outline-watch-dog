FROM python:3.8-alpine
ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python","outline_watch_dog.py"]