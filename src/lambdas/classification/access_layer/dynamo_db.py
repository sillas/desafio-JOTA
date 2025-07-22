from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError
from loggin_config import logger


class DB:

    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.processed_news_table = dynamodb.Table('processed_news')

    def store_processed_news(self, news: Dict[str, Any]) -> bool:
        """Armazena as notícias processadas na tabela do DynamoDB.
        :param news: Um dicionário representando a notícia a ser armazenada.
        :returns bool: True se a notícia foi armazenada com sucesso, False caso contrário.
        """

        try:
            self.processed_news_table.put_item(
                Item=news,
                ConditionExpression="attribute_not_exists(#uuid)",
                ExpressionAttributeNames={
                    "#uuid": 'uuid',
                }
            )
            return True

        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.info("Notícia já processada.")
                return True

            else:
                logger.exception(
                    "ERROR enquanto tentava executar -put_item-: ", exc_info=e)
                logger.info("Dados com erro", extra={
                            "uuid": news["uuid"]})
                return False
