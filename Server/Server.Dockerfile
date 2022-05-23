FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r Server/requirements.txt

EXPOSE 50051

CMD ["python","Server/Server.py"]

