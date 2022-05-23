FROM python:3-stretch

WORKDIR /app

COPY Web_Server/output_logs.py Web_Server/requirements.txt /app/

COPY Web_Server/templates /app/templates

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080:5000

CMD ["python","output_logs.py"]