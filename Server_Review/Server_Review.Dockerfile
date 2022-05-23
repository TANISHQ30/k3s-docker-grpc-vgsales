FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r Server_Review/requirements.txt

EXPOSE 50061

CMD ["python","Server_Review/ServerReview.py"]

