FROM python:latest
COPY actOneStepOne.py .
COPY userAgent.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN python3 ./actOneStepOne.py
