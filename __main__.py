"""
Direct Line Group Technical test module.

Problem statement:

    Create a REST endpoint that return the sum of a list of numbers
    e.g. [1,2,3] => 1+2+3 = 6 You are free to use any Python 3
    framework, however, try and keep the usage of the third- party
    library to a minimum. The list of numbers is expected to arrive
    from a backend service and for this test you can hard code the
    list using the following line.

Solution:

    $ ~/__main__.py
    * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
    127.0.0.1 - - [01/Sep/2021 00:47:19] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [01/Sep/2021 00:47:31] "GET /total HTTP/1.1" 200 -
    127.0.0.1 - - [01/Sep/2021 00:47:49] "GET /?add=1,2,3,4.5 HTTP/1.1" 200 -

    $ ~/__main__.py --host 0.0.0.0
    * Running on http://0.0.0.0:5000 (Press CTRL+C to quit)
    0.0.0.0 - - [01/Sep/2021 00:48:12] "GET / HTTP/1.1" 200 -
"""

import argparse
import http
import http.server
import json
import socketserver
import urllib.parse as _urllib
from decimal import Decimal
from typing import List
from typing import Union

numbers_to_add: List[int] = list(range(10000001))


class WrapDecimal(json.JSONEncoder):
    """
    Extensible JSON encoder for Python data structures.

    To recognize other objects, we need to subclass and implement a
    :py:meth:`default` method with another method that returns a
    serializable object.

    ..seealso::

        To understand more about the below implementation, see this:
        https://docs.python.org/3/library/json.html?highlight=json%20jsonencoder#json.JSONEncoder
    """

    def default(self, o: Decimal) -> Union[int, float]:
        """Implementation to serialize ``o`` argument."""
        if isinstance(o, Decimal):
            # NOTE: The below is potentially a HUGE MISTAKE and an
            # unnecessary OVER ENGINEERING! but this works. This is
            # not required as such because we can get around this by
            # converting everything to float by default but it makes
            # more sense to return response of ints as int and float as
            # float.
            return int(o) if float(o).is_integer() else float(o)
        return super().default(o)


class Handler(http.server.SimpleHTTPRequestHandler):
    """
    This class is used to handle the HTTP requests that arrive at the
    server. By itself, it cannot respond to any actual HTTP requests;
    it must be subclassed to handle each request method (e.g. GET or
    POST).

    The handler will parse the request and the headers, then call a
    method specific to the request type. The method name is constructed
    from the request. Subclasses should not need to override or extend
    the __init__() method.

    .. note::

        This implementation doesn't cover all the necessary
        nitty-gritty stuff and just works with the bare bone
        essentials.

    .. warning::

        As per official Python documentation, http.server is not
        recommended for production. It only implements basic security
        checks.
    """

    def do_GET(self):
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if self.path == "/":
            response = (
                "Add /total for the default total or "
                "add /?add=<LIST OF NUMBERS SEPARATED BY COMMAS> to "
                "calculate sum of numbers."
            )
        # NOTE: Here, we're presuming that the list of numbers would be
        # coming from a backend service which may have already run
        # through the process thus generating it. So it is same to
        # assume and sum the numbers. Since the object to sum we're
        # dealing with is a list (mutable object), it will be passed
        # by reference so we can blindly pass the ``numbers_to_add``
        # list to the sum().
        if self.path == "/total":
            response = {"total": sum(numbers_to_add)}
        # NOTE: This is not required but this is how the service can
        # be extended in a way. Please note that this is a very crude
        # implementation and the optimizations can be done here.
        components = _urllib.parse_qs(_urllib.urlparse(self.path).query)
        add = components.get("add")
        if add:
            response = {"total": sum(map(Decimal, add[0].split(",")))}
        self.wfile.write(bytes(json.dumps(response, cls=WrapDecimal).encode()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", help="Service host")
    parser.add_argument("--port", default="5000", help="Service port")
    args = vars(parser.parse_args())
    HOST, PORT = args.values()
    with socketserver.TCPServer((HOST, int(PORT)), Handler) as httpd:
        print(f"* Running on http://{HOST}:{PORT} (Press CTRL+C to quit)")
        httpd.serve_forever()
