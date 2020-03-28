#!/usr/bin/env python

"""

(c) 2020 Jonathan Angeles
jangelesg{at}gangsecurity{dot}com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

from tools.utils import make_requests
from colorama import Fore
from prettytable import PrettyTable
from pyfiglet import Figlet
from datetime import datetime
import argparse as arg

custom_fig = Figlet(font='graffiti')

# GLOBAL

URL = 'https://covid19.mathdro.id/api/'


def text_format(color: str, data: str):
    if color == 'Blue':
        print(Fore.LIGHTBLUE_EX + f'{data}')
    if color == 'Red':
        print(Fore.RED + f'{data}')
    if color == 'Green':
        print(Fore.GREEN + f'{data}')


class Covid19Records:
    def __init__(self, url_request: str, *args):  # Constructor Function
        self.url_call = url_request

        if url_request == 'global-summary':
            self.url = URL  # Global Summary
        if url_request == 'confirmed':
            self.url = URL + 'confirmed'  # global cases per region sorted by confirmed cases

        if url_request == 'recovered':  # global cases per region sorted by recovered cases
            self.url = URL + 'recovered'

        if url_request == 'deaths':  # global cases per region sorted by death toll
            self.url = URL + 'deaths'

        if url_request == 'daily':  # global cases per day
            self.url = URL + 'daily'

        if url_request == 'daily-date':  # detail of updates in a [date] (e.g. /api/daily/2-14-2020)
            self.date = args[0]
            self.url = URL + 'daily/'
            Covid19Records.match_date(self.date)
            self.url += self.date

        if url_request == 'countries':  # all countries and their ISO codes
            self.url = URL + 'countries'

        if url_request == 'country-summary':  # a [country] summary (e.g. /api/countries/Indonesia or /api/countries/USA or /api/countries/CN)
            country = args[0]
            text_format('Red', f'{country} Summary')
            self.url = URL + 'countries/' + f'{country}'  # >>

        if url_request == 'countries-confirmed':  # a [country] cases per region sorted by confirmed cases
            country = args[0]
            text_format('Red', f'{country} Confirmed')
            self.url = URL + 'countries/' + f'{country}/' + 'confirmed'  # >>

        if url_request == 'countries-recovered':  # a [country] cases per region sorted by recovered cases
            country = args[0]
            text_format('Red', f'{country} Recovered')
            self.url = URL + 'countries/' + f'{country}/' + 'recovered'  # >>

        if url_request == 'countries-deaths':  # a [country] cases per region sorted by death toll
            country = args[0]
            text_format('Red', f'{country} Deaths')
            self.url = URL + 'countries/' + f'{country}/' + 'deaths'

        if url_request == 'alabama_counties':  # A summary of Alabama information
            self.url = 'https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/COV19_Public_Dashboard_ReadOnly/FeatureServer/0/query?f=json&where=CONFIRMED%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=69'

    @staticmethod
    def match_date(date: str):
        try:
            datetime.strptime(date, "%m-%d-%Y")
        except ValueError as err:
            print(f'[-] {err}')
            exit(1)

    def caller(self):
        def create_table(response):  # Receives a list with dictionary objects
            t = PrettyTable()  # Create Table Object
            confirmed = 0
            died = 0

            if self.url_call == 'alabama_counties':
                t.field_names = ['CNTYNAME', 'CNTYFIPS', 'ADPHDistrict', 'CONFIRMED', 'DIED']  # Creates a Column
                for k, v in response.items():  # Iterates key and value over the json
                    if k == 'features':  # Extract a list that contains the dicts records from counties
                        assert type(v) is list, 'The type is incorrect, expected a list'
                        for i in v:  # Iterate over the list
                            assert type(i) is dict, 'The type is incorrect, expected a dict'
                            for v in i.values():  # Iterates over the dict values
                                entries = []
                                for k, v in v.items():
                                    if k == 'CNTYNAME':
                                        entries.append(v)
                                    if k == 'CNTYFIPS':
                                        entries.append(v)
                                    if k == 'ADPHDistrict':
                                        entries.append(v)
                                    if k == 'CONFIRMED':
                                        confirmed += v
                                        entries.append(v)
                                    if k == 'DIED':
                                        died += v
                                        entries.append(v)
                                t.add_row(entries)  # add a row per entry
                text_format('Blue', f'[*]  Alabama Summary CONFIRMED: {confirmed} DIED: {died}\n')
                text_format('Blue', 'Alabama County Summary')

                return t

            if self.url_call == 'countries':
                t.field_names = ['Columns']  # Creates a Column
                for k, v in response.items():  # Iterates key and value over the json
                    if k == 'countries':  # If key is equals Country entries
                        entries = [k + ' ' + v for k, v in v.items()]
                        for i in entries.__iter__():
                            line = [f'{i}']  # Get one element and create a list
                return t  # Return the table object

            elif self.url_call == 'global-summary':
                t.field_names = ['Confirmed', 'Recovered', 'Deaths', 'lastUpdate']
                e = [v.get('value') for k, v in response.items() if type(v) is dict]  # Extract row items
                entries = []
                for i, v in enumerate(e):
                    if v is not None:
                        entries.append(v)
                entries.append(response.get('lastUpdate'))
                t.add_row(entries)  # add a row per entry
                return t  # Return the table object
            else:
                columns = [col for col in response[0].keys()]  # # Receives a list with dictionary objects
                t.field_names = [col for col in response[0].keys()]  # # Receives a list with dictionary objects
                for case in response:  # Iterate over the cases
                    entry = [value for value in case.values()]  # Generates a list  of entries from the keys values
                    if len(entry) < len(columns):  # Check the length of the row vs columns
                        for x in range(len(columns) - len(entry)):  # add padding to the row, avoiding a raise exception
                            entry.append(None)
                    t.add_row(entry)  # add a row per entry
                return t  # Return the table object

        ###################################################
        #         Check response is not empty
        ###################################################
        res = make_requests(url=self.url, method='get')
        if len(res.get('content')) > 2:  # Check the length of the response
            response_covid19_cases_json = res.get('json')  # Grab the json response
            table = create_table(response_covid19_cases_json)  # Create the table
        else:
            text_format(color='Red', data='[x] API Error Empty Response,  try again later')
            exit(0)

        return text_format(color='Green', data=str(table))  # Return a formatted table with the whole records


def banner():
    """

    """
    print(custom_fig.renderText('Covid19 Tracker-cli'))
    text_format(color='Blue',
                data='[*] COVID19 Data Tracker via Johns Hopkins CSSE https://systems.jhu.edu/research/public-health/ncov/ \n')


def manage_args():
    _parser = arg.ArgumentParser(
        epilog='''Email: jangeles@gangsecurity.com\nCode: https://github.com/jangelesg/cov1d19-cli\nBetter Safe, than Sorry!!\nIt's Covit19 Virus not a Chinese Virus ''',
        formatter_class=arg.RawDescriptionHelpFormatter, description='''\
         COVID19 Tracker Tool
    --------------------------------
    Data Tracker via Johns Hopkins CSSE
    https://systems.jhu.edu/research/public-health/ncov/ ''')

    _parser.add_argument('--gs', action="store_true", help=' Show global Summary')
    _parser.add_argument('--gc', action="store_true", help=' Global cases per region sorted by confirmed cases')
    _parser.add_argument('--gr', action="store_true", help=' Global cases per region sorted by recovered cases')
    _parser.add_argument('--gd', action="store_true", help=' Global cases per region sorted by death toll')
    _parser.add_argument('--d', action="store_true", help=' Global cases per day')
    _parser.add_argument('--dt', help='Detail of updates in a (e.g. python3 c0v1d19-cli-tracker.py --dt 2-14-2020)')
    _parser.add_argument('--c', action="store_true", help='All countries and their ISO codes')
    _parser.add_argument('--cs', help='A [country] Summary (e.g. python3 c0v1d19-cli-tracker.py --sc JAPAN)')
    _parser.add_argument('--cc',
                         help='A [country] Cases per region sorted by confirmed cases (e.g. python3 c0v1d19-cli-tracker.py --cc JAPAN)')
    _parser.add_argument('--cr',
                         help='A cases per region sorted by recovered cases (e.g. python3 c0v1d19-cli-tracker.py --cr JAPAN)')
    _parser.add_argument('--cd',
                         help='A cases per region sorted by death toll (e.g. python3 c0v1d19-cli-tracker.py --cd JAPAN)')
    _parser.add_argument('--ac', action="store_true",
                         help='Alabama region sorted by counties, and Summary')
    args = _parser.parse_args()
    arguments = args.gs, args.gc, args.gr, args.gd, args.d, args.dt, args.c, args.cs, args.cc, args.cr, args.cd, args.ac

    return arguments


def built_call(arguments: tuple):
    """

    :param arguments:
    """
    global_summary, global_confirmed, global_recovered, global_death, daily, daily_date, countries, country_summary, countries_confirmed, countries_recovered, countries_deaths, alabama_counties = arguments

    if global_confirmed is True:
        Covid19Records(url_request='confirmed').caller()
    if global_recovered is True:
        Covid19Records(url_request='recovered').caller()
    if global_death is True:
        Covid19Records(url_request='deaths').caller()
    if daily is True:
        Covid19Records(url_request='daily').caller()
    if daily_date:
        Covid19Records('daily-date', daily_date).caller()
    if countries is True:
        Covid19Records(url_request='countries').caller()
    if country_summary:
        Covid19Records('country-summary', country_summary).caller()
    if countries_confirmed:
        Covid19Records('countries-confirmed', countries_confirmed).caller()
    if countries_recovered:
        Covid19Records('countries-recovered', countries_recovered).caller()
    if countries_deaths:
        Covid19Records('countries-deaths', countries_deaths).caller()
    if alabama_counties:
        Covid19Records(url_request='alabama_counties').caller()
    elif global_summary is True:
        Covid19Records(url_request='global-summary').caller()


def main():
    """

    """
    args = manage_args()
    built_call(arguments=args)


if __name__ == '__main__':
    main()
