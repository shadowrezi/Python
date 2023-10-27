#!/usr/bin/env python3
'''usd to uash and oppsote convertor using PrivatBank API'''
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import json
import datetime
import requests


def get_rates():
    '''Download rates from API'''
    cache = "/tmp/currency_rates.cache"

    if os.path.isfile(cache):
        dt = os.path.getmtime(cache)

    if os.path.isfile(cache) and (datetime.datetime.utcfromtimestamp(dt) > datetime.datetime.utcnow() - datetime.timedelta(minutes=10)):
        with open(cache, 'r') as file:
            data = json.load(file)
    else:
        try:
            resp = requests.get(
                "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
            data = resp.json()
            with open(cache, 'w') as file:
                json.dump(data, file)
        except:
            if os.path.isfile(cache):
                with open(cache, 'r') as file:
                    print(
                        "Attention! PrivatBank API is not available, using cached values.")
                    data = json.load(file)
            else:
                sys.exit(
                    "PrivatBank API is not available and no cache found. Exiting...")
    return (data)


def autoconvert():
    '''Parse arguments'''
    parser = argparse.ArgumentParser(
        description='UAH<>USD converter using PrivatBank API. Can be used either in interactive mode (without arguments) or in automatic mode (exactly two arguments required).')
    parser.add_argument('amount', metavar='N', type=float,
                        help='amount of currency to convert')
    parser.add_argument('curr', metavar='C', type=str,
                        help='currency to convert from')

    args = parser.parse_args()
    # Get rates
    data = get_rates()
    # Convert
    if args.curr in ("usd", "USD"):
        print("%.2f UAH" % (args.amount*float(data[0]["buy"])))
    elif args.curr in ("uah", "UAH"):
        print("%.2f UAD" % (args.amount/float(data[0]["sale"])))
    else:
        print("Allowed currencies: UAH|USD")


def interactive():
    '''Get and print rates'''
    data = get_rates()
    course = round(float(data[0]["buy"]), 2)
    print("USD buying rate for ", datetime.date.today(), ":", course, ' UAH')

    # Start interactive mode
    def _is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    print("1. USD --> UAH")
    print("2. UAH --> USD")

    response = None
    while response not in ('1', '2'):
        response = input('Choose direction: ')

    sum_value = ''
    while _is_number(sum_value) == False:
        sum_value = input('Enter the sum to exchange: ')

    # print sum_value
    if response == '1':
        print("%.2f UAH" % (float(sum_value) * course))
    elif response == '2':
        print("%.2f USD" % (float(sum_value) / course))


print(data := get_rates()[1]['sale'][0:-3])
# import os
# os.system('echo 1 > /dev/pts/1 2> /dev/pts/0')
