import os
import sys


class LoadSpacyModel:

    def __init__(self, language_size: str['sm', 'lg']):
        # TODO: Remove before deploy!
        sys.path.append('../../layers/numpy')
        sys.path.append('../../layers/spacy_custom')
        self.nlp_model = self.load_model(language_size)

    def load_model(self, language_size: str['sm', 'lg']):

        try:
            if (language_size == 'sm' and self.load_file_module("pt_core_news_sm")):
                import temp.pt_core_news_sm as pt_core_news

            elif (language_size == 'lg' and self.load_file_module("pt_core_news_lg")):
                import temp.pt_core_news_lg as pt_core_news

            else:
                raise Exception(
                    f"Permitido apenas sm ou lg: fornecido: {language_size}")

            return pt_core_news.load()

        except Exception as e:
            raise Exception(f"ERRO ao carregar modelo: {str(e)}")

    def load_file_module(self, nome_arquivo: str) -> bool:
        caminho_destino = os.path.join("temp", nome_arquivo)

        if os.path.exists(caminho_destino):
            print("Exists")
            return True

        print("Load from S3")

        try:
            caminho_zip = os.path.join("../../../s3", f"{nome_arquivo}.zip")
            import zipfile
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall("temp")

            print("Extracted")
            return True
        except Exception:
            print("Model not found")
            return False

    def get_model(self):
        return self.nlp_model