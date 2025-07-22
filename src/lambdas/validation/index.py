import uuid
from json import loads
from sqs import sqs_send_message
from helpers import response_message
from validation import validate_json
from loggin_config import logger


def handler(event, context):

    logger.set_correlation_id(context.aws_request_id)

    payload = loads(event["body"])

    error, message = validate_json(payload)
    if (error):
        return response_message(400, {'error': message})

    payload['uuid'] = str(uuid.uuid4())
    return sqs_send_message(payload, context.aws_request_id)
