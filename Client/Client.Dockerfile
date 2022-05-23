FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r Client/requirements.txt

CMD ["python","Client/Client.py"]