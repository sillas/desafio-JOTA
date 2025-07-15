import json
from os import environ
from typing import Any
import boto3
from botocore.exceptions import ClientError
from helpers import response_message
from loggin_config import logger

sqs = boto3.client('sqs')


def sqs_send_message(payload: dict[str, str], aws_request_id: str) -> dict[str, Any]:
    """
    Função que envia a mensagem para a fila SQS

    Args:
        payload: Os dados a serem enviados para a fila.
        aws_request_id (str): ID de execução do Lambda

    Returns:
        dict: Resposta com status da operação
    """

    try:
        queue_url = environ.get('QUEUE_URL')

        if not queue_url:
            error_message = 'SQS_QUEUE_URL não configurada nas variáveis de ambiente'
            logger.error(error_message)
            return response_message(400, {
                'error': error_message
            })

        message_body = {
            'request_id': aws_request_id,
            'data': payload
        }

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body),
            MessageAttributes={
                'RequestId': {
                    'StringValue': aws_request_id,
                    'DataType': 'String'
                },
                'Source': {
                    'StringValue': 'lambda',
                    'DataType': 'String'
                }
            }
        )

        return response_message(200, {
            'message': 'Mensagem enviada com sucesso',
            'messageId': response['MessageId'],
            'requestId': aws_request_id
        })

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']

        logger.exception("sqs_send_message - Erro AWS", exc_info=e)

        return response_message(500, {
            'error': f'Erro AWS: {error_code}',
            'message': error_message
        })

    except Exception as e:
        logger.exception("sqs_send_message - Erro geral", exc_info=e)
        return response_message(500, {
            'error': 'Erro interno do servidor',
            'message': str(e)
        })
