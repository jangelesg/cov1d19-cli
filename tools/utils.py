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

from requests.exceptions import HTTPError, SSLError
import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def make_requests(url, method, **kwargs):
    """
    This provides a convenience function for making requests. This interfaces with requests  which in turn interfaces
    with urllib3 and provides the ability to make GET, POST, PUT, PATCH and DELETE requests.

    The return data from this function is headers, content, http status, and the timedelta from a successful request
    """

    # Checks to ensure that HTTP methods are valid  and header values and postdata are in the appropriate format

    METHODS = 'put', 'get', 'post', 'patch', 'delete'

    assert method in METHODS, f'HTTP Method is not valid in the function, Valid Methods {METHODS}'

    def manage_arguments():
        """This provides a convenience function to manage and select the necessary parameters for the request """

        parameters = {'url': url}  # Creating parameters starting with the url
        parameters.update({'verify': False})  # DEFAULT SSL VERIFICATION DISABLE
        for _ in kwargs.keys():  # Selecting and Adding parameters from arguments
            if _ == 'headers':
                parameters.update({'headers': kwargs['headers']})
            if _ == 'params':
                parameters.update({'params': kwargs['params']})
            if _ == 'data':
                parameters.update({'data': kwargs['data']})
            if _ == 'allow_redirects':
                parameters.update({'allow_redirects': kwargs['allow_redirects']})
            if _ == 'json':
                parameters.update({'json': kwargs['json']})
            if _ == 'proxies':
                # If proxies parameters is present "verify" Parameter is added equal to "False" to avoid
                # SSL Certs Error and disable warnings
                try:
                    from urllib3.exceptions import InsecureRequestWarning
                except ImportError as er:
                    print(f"Import Error Occurred. {er}")

                else:
                    # Suppress only the single warning from urllib3 needed.
                    # requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
                    parameters.update({'proxies': kwargs['proxies']})
                    parameters.update({'verify': False})

        return parameters

    try:
        _args = manage_arguments()

        req = {'post': requests.post,  # Selecting the appropriate HTTP Object method
               'patch': requests.patch,
               'put': requests.put,
               'get': requests.get,
               'delete': requests.delete
               }.get(method, lambda: None)

        start = datetime.datetime.now()

        response = req(**_args) # unpacking

        #  An HTTPError will be raised for certain status codes. If the status code indicates a successful request,
        #  the program will proceed without that exception being raised.

        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'{response.text}')
        exit(1)
    except Exception as err:
        print(f'Exception occurred: {err}')
        exit(1)
    except SSLError as sslerr:
        print(f'SSLError error occurred: {sslerr}')
        exit(1)
    else:
        end = datetime.datetime.now()
        time = end - start

        # Grab the HTTP Status Code, HTTP Headers, HTTP Content, JSON in case, Time, HTTP TEXT Content

        return {'headers': response.headers,
                'content': response.content,
                'code': response.status_code,
                'text': response.text,
                'json': response.json(),
                'time': f'Total in seconds: {time}',
                }


