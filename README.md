# Smart Meter with Raspberry Pi Zero

## Setup
### Install dependencies

As for the installation of Python dependencies, you can run the following [pip](https://pypi.org/project/pip/) command
```shell
python -m pip install -r requirements.txt
```

You can also obtain a stand-alone package, not requiring a compiler or external libraries, by installing the psycopg2-binary package from PyPI:
```shell
pip install psycopg2-binary
```

Install Postgres on the raspberry pi via
```shell
sudo apt update
sudo apt full-upgrade
sudo apt install postgresql
```

### Create .env file for credentials to connect to postgres database in the cloud

To set up a local .env file:

1) Copy `.env_example` and paste it as `.env` on the same directory level

```shell
cp ./.env_example ./.env
```

2) Replace empty strings in the new .env file with strings containing the secrets

```
DATABASE_NAME=""
DATABASE_USERNAME=""
DATABASE_PASSWORD=""
DATABASE_HOST=""
PAPERTRAIL_HOST=""
PAPERTRAIL_PORT=
```

## Run script
### Run measurement manually
```shell
python main.py
```

### Run with cronjob

Open the crontab editor with the following command:
```shell
crontab -e
```

Add a cronjob at the end of the file and save:
```
# m h dom mon dow   command
# */15 * * * * /usr/bin/python3 /home/willykaestner/PythonProgramms/energy_meter/main.py
```
More information about running cronjobs on a raspberry pi can be found [here](https://medium.com/analytics-vidhya/how-to-automate-run-your-python-script-in-your-raspberry-pi-b6fe652443db).
