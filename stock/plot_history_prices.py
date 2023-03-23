import sys
sys.path.append("..")

import datetime
import logging
import logging.config

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np

from stock.get_data_and_store import get_stock_data_by_date


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def plot_prices_and_save(df):
    """Create and save some plots"""
    sns.histplot(df.open.dropna())
    plt.xlabel("Open Price", size=14, fontweight='bold')
    plt.savefig('img/open_price.png', dpi=100, bbox_inches="tight")
    plt.close()
    
    sns.histplot(df.close.dropna())
    plt.xlabel("Close Price", size=14, fontweight='bold')
    plt.savefig('img/close_price.png', dpi=100, bbox_inches="tight")
    plt.close()

    # Open by Date
    sns.lineplot(data=df.sort_values('date'), x='date', y='open')
    plt.xticks(rotation=20);
    plt.title('Open Price by Date', loc='center', color='black',
                fontsize=18, fontweight='bold')
    plt.xlabel("Date", size=14, fontweight='bold')
    plt.ylabel("Open Price", size=14, fontweight='bold')
    plt.savefig('img/open_price_by_date.png', dpi=100, bbox_inches="tight")
    plt.close()

    # Close by Date
    sns.lineplot(data=df.sort_values('date'), x='date', y='close')
    plt.xticks(rotation=20);
    plt.title('Close Price by Date', loc='center', color='black',
                fontsize=18, fontweight='bold')
    plt.xlabel("Date", size=14, fontweight='bold')
    plt.ylabel("Close Price", size=14, fontweight='bold')
    plt.savefig('img/close_price_by_date.png', dpi=100, bbox_inches="tight")
    plt.close()


def collect_data_in_dataframe():
    """create and process dataframe to work with it"""
    df_to_plot = None
    dfs = []
    date_without_file = []

    for date in n_dates:
        try:
            dfs.append(pd.read_json(f'data/{date}.json'))
        except FileNotFoundError:
            date_without_file.append(date)
            # some dates can have empty response
            continue

    data = pd.concat(dfs, ignore_index=True)

    # insert dates with empty response
    for date in date_without_file:
        rest_df = pd.DataFrame([[
            np.NaN, np.NaN, np.NaN, np.NaN, f"{date}", "AAPL",
            np.NaN, "HISTORICAL_PRICES", "AAPL", "",
            f"{date}", np.NaN, np.NaN, np.NaN, np.NaN,
            np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,
            np.NaN, np.NaN, np.NaN, "", np.NaN, np.NaN
        ]], columns=data.columns)
        data = pd.concat([data, rest_df])

    # create dataframe to work and format date
    interesting_cols = [ 'open', 'close', 'priceDate' ]
    df = data[interesting_cols]

    copy_df = df.copy()
    copy_df.loc[:, 'date'] = pd.to_datetime(
        copy_df.priceDate, format='%Y-%m-%d')

    df_to_plot = copy_df.copy()
    df_to_plot.loc[:, 'date'] = copy_df.date.dropna().reset_index(drop=True)

    return df_to_plot


if __name__ == '__main__':
    # create dates of last 30 days
    range_datetimes = pd.date_range(
        end = datetime.datetime.today(), periods = 30
        ).to_pydatetime().tolist()

    n_dates = [ d.date().__str__() for d in range_datetimes ]

    for date in n_dates:
        get_stock_data_by_date(date)

    df = collect_data_in_dataframe()

    plot_prices_and_save(df)