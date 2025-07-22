from typing import Any
from access_layer.s3_handler import load_from_s3
from loggin_config import logger


class LoadSpacyModel:

    def __init__(self):
        self.nlp_model = self.load_model()

    def direct_load(self):
        """Load lang model from temp folder."""
        try:
            import temp.pt_core_news_sm as pt_core_news  # type: ignore
            return pt_core_news.load()
        except:
            raise

    def load_model(self) -> Any:
        """Carega o modelo de linguagem do S3 e retorna a instância."""
        logger.info('Trying to load lang model.')

        try:
            return self.direct_load()
        except:
            logger.info('Not in /temp. Trying to load from local env.')

        try:
            import pt_core_news_sm
            return pt_core_news_sm.load()
        except:
            logger.info('Not in local env. Trying to load from S3')

        try:
            if (not load_from_s3("pt_core_news_sm.zip")):
                raise Exception(
                    f"Module pt_core_news_sm not load.")

            return self.direct_load()

        except Exception as e:
            raise Exception(f"Fail to load lang model: {str(e)}")

    def get_model(self):
        """Get nlp model"""
        return self.nlp_model
