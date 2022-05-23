FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r Client_Review/requirements.txt

CMD ["python","Client_Review/ClientReview.py"]