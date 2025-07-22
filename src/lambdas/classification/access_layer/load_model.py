from access_layer.s3_handler import load_from_s3


class LoadSpacyModel:

    def __init__(self, language_size: str['sm', 'lg']):
        # TODO: Remove before deploy!
        # sys.path.append('../../layers/numpy')
        # sys.path.append('../../layers/spacy_custom')
        # --------------------------
        self.nlp_model = self.load_model(language_size)

    def load_model(self, language_size: str['sm', 'lg']) -> None:
        """Carega o modelo de linguagem do S3 e retorna a instância.
        :param language_size: O tamanho da linguagem que desejo utilizar [sm | bg]
        """
        try:
            module_loaded = load_from_s3(
                "pt_core_news_sm.zip" if language_size == 'sm' else "pt_core_news_lg.zip")

            if (not module_loaded):
                raise Exception(
                    f"Module pt_core_news_{language_size} not load.")

            if (language_size == 'sm'):
                import temp.pt_core_news_sm as pt_core_news  # type: ignore

            elif (language_size == 'lg'):
                import temp.pt_core_news_lg as pt_core_news  # type: ignore

            else:
                raise Exception(
                    f"Size {language_size} not allowed. Use only sm or lg.")

            return pt_core_news.load()

        except Exception as e:
            raise Exception(f"ERROR ao carregar modelo: {str(e)}")

    def get_model(self):
        return self.nlp_model
