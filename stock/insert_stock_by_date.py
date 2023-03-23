import sys
sys.path.append("..")

import argparse
import logging
import logging.config
import pandas as pd

from db.session import engine

from stock.get_data_and_store import (
    get_stock_data_by_date,
    validate_iso8601,
)


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def create_table(json_file=None):
    df = pd.read_json(json_file)
    df.to_sql('stocks', con=engine, if_exists="append")


def insert_stock_in_db(json_file=None):
    """
    Write in the database a list of stock items that will have to collect from a json file.

    :param json_file: json file with contains items
    """
    if json_file is None:
        msg = "Insert json file"
    else:
        msg = "Successfull insert stock items"

        with open(json_file, "r+") as file:
            try:
                create_table(json_file)
            except Exception as e:
                msg = f"Unsuccessfull insert stock: {e}"

        file.close()

    logger.info(msg)

def add_argumments():
    parser = argparse.ArgumentParser(
                        prog = 'Stock Data',
                        description = 'Get Stock data by a given date and store'
            )

    parser.add_argument('date', type=str,
                        help='date text in ISO 8601 format (e.g. 2022-10-04)')
    parser.add_argument('-s', '--store', type=bool,
                        help='If you want store the data in database, pass --store=True')

    args = parser.parse_args()

    return args

def handle(args):
    """Validate date and get stock data by date"""
    response = None
    date = args.date if args.date else None
    store = args.store if args.store else None

    if date is None:
        logger.error("Please pass date argument")
        return

    try:
        validate_iso8601(date)
    except ValueError as e:
        logger.error(e)
        return

    response = get_stock_data_by_date(date)
    if store:
        insert_stock_in_db(f'./data/{date}.json')

    return response


if __name__ == '__main__':
    args = add_argumments()
    response = handle(args)
