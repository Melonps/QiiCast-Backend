FROM python:3.10-slim

USER root
RUN apt update && apt install git --yes && apt install curl --yes
RUN pip install --upgrade pip
RUN pip install pandas,  numpy
EXPOSE 8000