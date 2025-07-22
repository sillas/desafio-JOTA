import os
import zipfile
import boto3
from botocore.exceptions import ClientError
from loggin_config import logger

s3_client = boto3.client('s3')


def load_from_s3(object_key: str) -> bool:
    """Baixa um arquivo .zip do S3 para o diretório /tmp do Lambda e o extrai.

    :param object_key: O caminho completo (chave) para o arquivo .zip no bucket.
    :return bool: Se o modelo foi baixado do S3 e descompactado com sucesso em /temp.
    """

    extract_path = '/tmp'
    zip_filename = os.path.basename(object_key)
    zip_filepath = os.path.join(extract_path, zip_filename)

    bucket_name = os.getenv('S3_BUCKET')

    try:
        s3_client.download_file(bucket_name, object_key, zip_filepath)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        os.remove(zip_filepath)

        return True

    except ClientError as e:

        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.exception(
                f"Erro: O objeto '{object_key}' não foi encontrado no bucket '{bucket_name}'.", exc_info=e)

        else:
            logger.exception(
                f"Ocorreu um erro inesperado do Boto3: {e}", exc_info=e)

    except Exception as e:
        logger.exception(
            f"Ocorreu um erro durante a extração: {e}", exc_info=e)

    return False
