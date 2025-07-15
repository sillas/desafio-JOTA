
from os import environ
from datetime import datetime
from typing import Any
import uuid
import boto3
from loggin_config import logger

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
news_table = dynamodb.Table(environ["TABLE_NAME"])


def put_profile(news_data: dict[str, Any]) -> None:
    """
    Cria o registro da notícia no DynamoDB para sincronia posterior com um banco relacional.

    Args:
        news_data (dict): The news
    """

    registry = {
        "status": "waiting",  # Chave de partição (única).
        "uuid": str(uuid.uuid4()),  # Chave de Classificação
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ** news_data
    }

    try:
        news_table.put_item(Item=registry)

    except Exception as e:
        logger.exception(
            "ERROR enquanto tentava executar -put_item-", exc_info=e)
