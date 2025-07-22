from typing import Any
from access_layer.s3_handler import load_from_s3
from loggin_config import logger


class LoadSpacyModel:

    def __init__(self):
        self.nlp_model = self.load_model()

    def load_model(self) -> Any:
        """Carega o modelo de linguagem do S3 e retorna a instância."""
        try:
            import pt_core_news_sm
            return pt_core_news_sm.load()
        except:
            logger.info('In production Env. Trying to load model from S3.')

        try:
            module_loaded = load_from_s3("pt_core_news_sm.zip")

            if (not module_loaded):
                raise Exception(
                    f"Module pt_core_news_sm not load.")

            import temp.pt_core_news_sm as pt_core_news  # type: ignore
            return pt_core_news.load()

        except Exception as e:
            raise Exception(f"ERROR ao carregar modelo: {str(e)}")

    def get_model(self):
        return self.nlp_model
