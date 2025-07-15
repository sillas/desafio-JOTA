from json import dumps
from typing import Any


def response_message(status_code: int, message: str | dict[str, Any]) -> dict[str, Any]:

    return {
        'statusCode': status_code,
        'body': dumps(message)
    }
