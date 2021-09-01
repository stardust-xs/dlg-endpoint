import json
from typing import Union

import pytest
import requests  # type: ignore


@pytest.mark.parametrize(
    ("path", "attr", "response"),
    (
        ("/", "status_code", 200),
        ("/", "headers", "application/json"),
        (
            "/",
            "text",
            json.dumps(
                "Add /total for the default total or "
                "add /?add=<LIST OF NUMBERS SEPARATED BY COMMAS> to "
                "calculate sum of numbers."
            ),
        ),
        ("/total", "text", json.dumps({"total": 50000005000000})),
        ("/?add=1,2,3", "text", json.dumps({"total": 6})),
        ("/?add=10,2.7,31.856,41.345", "text", json.dumps({"total": 85.901})),
    ),
)
def test_service(path: str, attr: str, response: Union[int, str]) -> None:
    _response = requests.get(f"http://0.0.0.0:5000{path}")
    if attr == "headers":
        assert getattr(_response, attr)["Content-Type"] == response
        return
    assert getattr(_response, attr) == response
