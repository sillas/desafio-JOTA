import json
from datetime import datetime
from data_layer.classification import Classification
from access_layer.dynamo_db import DB
from loggin_config import logger

classify = Classification()
db = DB()


def classify_message(body: str) -> bool:

    logger.info("classify_message", extra={
        "# DATA": message
    })

    message: dict = json.loads(body)
    category: str = classify.process(message)
    formated_news = {
        "status": "waiting",  # Chave de partição (única).
        "category": category,
        "tags": [],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **message
    }

    success: bool = db.store_processed_news(formated_news)
    return success
