import csv
import requests
from bs4 import BeautifulSoup
import re
import io
import tabula
import functools
import itertools
import pandas


def scrapeData():
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    tables = tabula.read_pdf('./jh_closed_end_fund.pdf', pages="all")
    tables = [t for t in tables if not t.empty and (re.search('(Bank)', ','.join(map(
        str, t.columns.values.tolist()))) or re.search('continued', ','.join(map(str, t.head(n=1).values.tolist()))))]
    headers = list(map(lambda table: filter(lambda col: not re.search(
        '(Unnamed)', col), table.columns.values.tolist()), tables))
    headers = [h for h in headers for h in h]
    headers = list(dict.fromkeys(headers))
    for table in tables:
        table.columns = headers
    holdings = pandas.concat(tables, ignore_index=True)
    pandas.set_option('display.max_columns', None)  # or 1000
    pandas.set_option('display.max_rows', None)  # or 1000
    # pandas.set_option('display.max_colwidth', -1)  # or 199
    print(holdings)
    holdings.to_csv('holdings.csv')


if __name__ == "__main__":
    scrapeData()
