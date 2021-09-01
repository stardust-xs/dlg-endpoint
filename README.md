<!-- markdownlint-disable MD033 MD041 -->
# DLG - RESTful Endpoint

## Prelude

As per given requirement, a RESTful endpoint is implemented. This is the first time I'm trying a REST API so it may not be correct or I may have certainly mistaken in understanding the requirement. Later might be true. Whatever be the case, the so-called *"implementation"* seems to work. As per the requirement, an endpoint is created which sums a list of arbitrary numbers. The requirement presumes the list of numbers would be already present as a result of backend service so it is safe to assume the list already exists. This followed with the fact that the lists are mutable, we can use this list to pass to the python's sum function to calculate the sum of the numbers. For the sake of extensibility, the implementation also supports addition via the query strings.

To keep the use of 3rd party libraries to minimum, this service is implemented using the Python's builtin [socketserver](https://docs.python.org/3/library/socketserver.html) and [http.server](https://docs.python.org/3/library/http.server.html) module. The same can be replaced either with [Flask](https://flask.palletsprojects.com/en/2.0.x/) or [Django](https://www.djangoproject.com/) and implemented in much better and graceful way. But I don't know either of those, hence I thought of implementing this with pure Python.

The implementation supports type hints and is statically typed, linted using pylint and formatted using black.

## Running the code

To run the code, simply clone the repo and call the script like below:
```bash
$ python __main__.py
```
This will run start the webserver. The default host is `127.0.0.1` and runs on port `5000`. You can override this by providing `--host` and `--port` arguments like below:
```bash
$ python __main__.py --host 0.0.0.0 --port 8080
```

## Endpoints

As per the requirements, there is a default `/total` path OR endpoint. By visiting the server at `/total` path, you'll get the default sum of the `range(10000001)`. This behavior is also aided with query string parameters. You can add `/?add=1,2,3...` and provide a list of numbers. This will sum all the numbers and return response as:

```json
{
	"total": 6
}
```

## Tests

The service is tested for status code, headers and the responses using pytest. Tests are present under `test_main.py`.


## License

Copyright (c) 2021 XAMES3. All rights reserved.
Licensed under the [MIT](https://github.com/xames3/dlg-endpoint/blob/main/LICENSE) License
