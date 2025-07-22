import os
import zipfile
import boto3
from botocore.exceptions import ClientError
from loggin_config import logger

s3_client = boto3.client('s3')


def load_from_s3(filename: str) -> bool:
    """Baixa um arquivo .zip do S3 para o diretório /tmp do Lambda e o extrai.

    :param filename: O nome do arquivo .zip no bucket.
    :return bool: Se o modelo foi baixado do S3 e descompactado com sucesso em /temp.
    """

    bucket_name = os.getenv('S3_BUCKET')
    zip_filepath = f"/tmp/{filename}"

    try:
        s3_client.download_file(
            bucket_name, f"spacy_model/{filename}", zip_filepath)

        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall("/tmp")

        os.remove(zip_filepath)

        return True

    except ClientError as e:

        if e.response['Error']['Code'] == 'NoSuchKey':
            logger.exception(
                f"ERROR'{filename}' not found on bucket '{bucket_name}'.", exc_info=e)

        else:
            logger.exception(
                f"ERROR: Boto3 error: {e}", exc_info=e)

    except Exception as e:
        logger.exception(
            f"ERROR: load_from_s3 exception: {e}", exc_info=e)

    return False
