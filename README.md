# FamYoutube

An application which has following features:

* Fetches a videos of a specific domain in background, to populate the database. (Using celery and RabbitMQ)
* A GET API endpoint to get all the videos data in paginated format.
* GET API features include : sorting by specific field, searching a term in title/description.

## Setup

To set up this project follow below steps:

### Prequisites : 
* RabbitMQ-server : Install on [Windows](https://www.rabbitmq.com/install-windows-manual.html)|[Linux](https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-linux/)
* python3 
* virtualenv : Install using [pip/python](https://virtualenv.pypa.io/en/latest/installation.html)

### Steps :

1. Clone this repository with command `git clone https://github.com/BadduCoder/FamYoutube`
2. Change working directory to FamYoutube using `cd FamYoutube/`
3. Create virtual environment using command `virtualenv --python=python3 env`
4. Activate virtualenv using the command `source env/bin/activate`
5. Install requirements of the project using command `pip3 install -r requirements.txt`
6. Copy `env.example` as `.env` in root directory and put the values required.
7. Run all the migrations using commands `python3 manage.py migrate`
8. To run background task using celery, run following commands in sequence:
    * `celery -A FamYoutube worker`
    * `celery -A FamYoutube beat`
9. To run the server, run the command `python3 manage.py runserver`


## Documentation

### GET API : List API
`localhost:[PORT]/get-data/`
* Default PORT Value = 8000
This API endpoint if called without any arguments, returns all the videos present in database.
It can be called with following parameters:

1. page
    * Example `/get-data/?page=2`
2. q
    * Example `/get-data/?q=IPL`
    * Returns only those records, which contain q's value in title/description
3. sortby 
    * Example `/get-data/?sortby=title`
    * It takes only following arguments [`id`,`-id`,`publishedAt`,`-publishedAt`]
    * Invalid value is ignored and argument isn't considered



