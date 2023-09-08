FROM python:3.10

## Set the working directory in the docker container
WORKDIR /app

## Install dependencies
COPY ./forecast/requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install prophet

## Copy all the scripts to the working directory
COPY . /app

## Run the forecast script
CMD ["python", "./forecast_main.py"]