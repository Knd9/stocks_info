import sys
sys.path.append("..")

import argparse
import datetime
import json
import logging
import logging.config
import requests
import time
from urllib.parse import urljoin

from stock.constants import (
    URL_BASE,
    STOCK_ENDPOINT_DATE,
)
from stock.core.config import settings


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def use_api(url='', method='GET', params=dict(), headers=dict(), **kwargs):
    """Send requests using Stock API."""
    request_url = urljoin(URL_BASE, url)

    if 'date' in kwargs:
        request_url = urljoin(request_url, kwargs.get('date'))

    logger.debug(
        "Hitting URL: %s (method %s)",
        request_url, method
    )

    response = {
        'error': False,
        'text': None,
    }

    try:
        start_time = time.time()

        resp = requests.request(
            method,
            request_url,
            headers=headers,
            params=params,
        )

        logger.debug(
            "Response from %s (took %s sec): %s",
            request_url,
            (time.time() - start_time),
            resp.text,
        )
        resp.raise_for_status()

    except requests.exceptions.HTTPError as e:
        logger.error("HTTP Error on request: %s", e)
        response['error'] = True
        response['text'] = e.response.text
        response['status_code'] = e.response.status_code
    except Exception as e:
        logger.error("Error: %s", e)
        response['error'] = True
        response['text'] = e.response.text
        response['status_code'] = e.response.status_code
    else:
        if resp is None:
            logger.error("API error, empty response: %s", response)

        logger.info("answered OK")
        response['text'] = resp.text

    return response

def store_in_file(data=None, filename=''):
    """
    Convert given data to json file and
    store in new file with given filename

    @param data: data to process
    @param filename: name of file to store
    """
    if data and filename:
        str_data = json.dumps(data, indent=2)
        json_file = open(f'./data/{filename}.json', 'w')
        json_file.write(str_data)
        json_file.close()

def get_stock_data_by_date(date=None):
    """
    Get API Token,
    call request to get stock data of given date
    and store compressed file of json format.

    @param date: date text in iso8601 format.
    """
    response = None
    token = settings.API_TOKEN

    if token:
        parsed_token = token.replace("'", "")
        params = {
            "token": parsed_token,
            "chartByDay": True
        }
    if date:
        parsed_date = date.replace("-", "")
        kwargs = {
            "date": parsed_date+'/'
        }

    response = use_api(
        url=STOCK_ENDPOINT_DATE, params=params, **kwargs
    )

    if response is not None and len(response.get('text')):
        data = json.loads((response.get('text')))
        store_in_file(data, date)

    return response

def validate_iso8601(date_text):
    """Validate date text format"""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

def add_argumments():
    parser = argparse.ArgumentParser(
                        prog = 'Stock Data',
                        description = 'Get Stock data by a given date and store'
            )

    parser.add_argument('date', type=str,
                        help='date text in ISO 8601 format (e.g. 2022-10-04)')

    args = parser.parse_args()

    return args

def handle(args):
    """Validate date and get stock data by date"""
    response = None
    date = args.date if args.date else None

    if date is None:
        logger.error("Please pass date argument")
        return

    try:
        validate_iso8601(date)
    except ValueError as e:
        logger.error(e)
        return

    response = get_stock_data_by_date(date)
    return response


if __name__ == '__main__':
    args = add_argumments()
    response = handle(args)
