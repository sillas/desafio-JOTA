import json
from typing import Dict, Any
from aws_lambda_powertools.utilities.typing import LambdaContext
from loggin_config import logger
from data_layer.handle_message import classify_message


def handler(event: Dict[str, Any], context: LambdaContext):

    logger.set_correlation_id(context.aws_request_id)

    logger.info("EVENT", extra={
        "#EVENT": event
    })

    if ("Records" in event):
        for record in event['Records']:
            classify_message(record['body'])

    return {
        'statusCode': 200,
        'body': json.dumps('sucesso!')
    }
