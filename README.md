# Stocks information app

This respository contains a few different functions based on stocks database. 
It integrates Python, PostgreSQL and Docker technologies.

## Setup

1. Create an Individual account at https://iexcloud.io/cloud-login/, a streaming data platform for finance. 
Select the free start plan and verify your email address in order to obtain your public API token which is used in .env file. 
Replace API_TOKEN value in that file by it.
[Here](https://iexcloud.io/docs/api/) you can find a IEX Cloud API’s documentation.

2. Install [Docker](https://docs.docker.com/engine/install/) in your system.

3. In local terminal go to path that contains this repository.

4. Create `img/` and `data` directories.

`$ mkdir img`
`$ mkdir data`

5. Run project with Docker Compose.

`$ docker-compose up --build`

## Functionalities

* **Functionality 1**

Script that receives an ISO8601 date (e.g. 2022-10-04) (parsed with [argparse](https://docs.python.org/3/library/argparse.html)) downloads data from the
`/stock/AAPL/chart` endpoint for that day and stores it in a json local file, inside `data/` directory, with the corresponding date in the file’s name.

Execute bash command with backend container.

`$ docker exec -it fastapi-app bash`

Execute a following script with a date.

`$ python get_data_and_store.py '2022-10-04'`

`$ exit`

View data of file generated.

`$ cat data/2022-10-04.json`

* **Functionality 2**

Script that stores a plot of the open and close prices for stocks of last **30 days**.

Execute bash command with backend container.

`$ docker exec -it fastapi-app bash`

Execute a following script.

`$ python plot_history_prices.py`

`$ exit`

Go to `img/` directory.

Open **stock/*.png** images generated.

* **Functionality 3**

A derivation of the Functionality 1, with choice to store the data getting in a table of the database.

Execute bash command with backend container.

`$ docker exec -it fastapi-app bash`

Execute a following script with a date and the `store` argument set to True.

`$ python insert_stock_by_date.py '2022-10-04' --store=True`

`$ exit`

Execute psql command in db container to view stocks inserted.

`$ docker exec -it db-stock psql -U root -W db`

(type the password that ask)

`\c db`

(type the password that ask)

`\dt`

`SELECT * FROM stocks;`

`\q`


## To stop and remove all containers, images and network of app
`$ docker-compose down --rmi all`
