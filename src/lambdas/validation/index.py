from json import loads
from sqs import sqs_send_message
from helpers import response_message
from validation import validate_json
from loggin_config import logger


def handler(event, context):

    logger.set_correlation_id(context.aws_request_id)

    body = loads(event["body"])

    error, message = validate_json(body)
    if (error):
        return response_message(400, {'error': message})

    return sqs_send_message(body, context.aws_request_id)
