import json
from datetime import datetime
from data_layer.classification import Classification
from access_layer.dynamo_db import DB
from loggin_config import logger
from access_layer.load_model import LoadSpacyModel

model = LoadSpacyModel("sm")
classify = Classification(model)
db = DB()


def classify_message(body: str) -> bool:
    """Classifica a notícia de acordo com os critérios estabelecidos.
    :param body: A mensagem JSON recebida da fila.
    :return bool: Indica se houve sucesso no processamento.
    """

    logger.info("classify_message", extra={
        "# DATA": body
    })

    message: dict = json.loads(body)
    category, tags = classify.process(message)
    formated_news = {
        "status": "waiting",  # Chave de partição (única).
        "category": category,
        "tags": [tags],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **message  # Title, Subtitle and Article
    }

    success: bool = db.store_processed_news(formated_news)
    return success
