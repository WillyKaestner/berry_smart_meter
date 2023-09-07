FROM python:3.10
# COPY . .
# RUN pip install -r ./forecast/requirements.txt
# RUN pip install prophet
# RUN pip install pydantic[dotenv]
# CMD ["python", "./forecast_main.py"]

## Set the working directory in the docker container
WORKDIR /app

## Install dependencies
COPY ./forecast/requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install prophet

## Copy all the scripts to the working directory
COPY . /app

## Run the forecast script
CMD ["python", "./forecast_main.py"]