FROM python:3.10-slim

USER root
RUN apt update && apt install git vim curl libgomp1 -y
RUN pip install --upgrade pip
RUN pip install pandas numpy lightgbm scikit-learn matplotlib jupyterlab

EXPOSE 8000