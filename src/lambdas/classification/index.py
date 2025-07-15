import json
from loggin_config import logger


def handler(event, context):

    logger.set_correlation_id(context.aws_request_id)

    logger.info("EVENT", extra={
        "#EVENT": event
    })

    # Obtem a notícia da fila

    # Executa a classificação

    # Monta o payload de saída

    # salva no DynamoDB

    return {
        'statusCode': 200,
        'body': json.dumps('sucesso!')
    }
