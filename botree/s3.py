"""Abstrações AWS."""

from pathlib import Path
from typing import Optional

from boto3.session import Session


class S3(object):
    """Classe de utilidades para operações com AWS S3."""

    def __init__(
        self, bucket: str, region: str, profile: Optional[str] = None
    ):
        """
        Init da classe S3.
        Parameters
        ----------
        bucket : str
            nome do bucket S3.
        region : str, optional
            região AWS do bucket
        profile : Optional[str], optional
            profile da AWS CLI, by default None. Para propósitos de desenvolvimento.
        """
        self.bucket = bucket
        self.region = region
        self.profile = profile
        self.session = Session(profile_name=profile)
        self.client = self.session.client(
            service_name="s3",
            region_name=region,
        )

    def download(self, destino: Path, fonte: str, **kwargs):
        """
        Download de arquivos do S3.
        Parameters
        ----------
        destino : Path
            local onde será salvo o arquivo escolhido.
        fonte : str
            local (chave) do objeto (arquivo) no S3.
        """
        if destino.is_file():
            destino.unlink()

        self.client.download_file(self.bucket, fonte, str(destino.resolve()), **kwargs)

    def upload(self, fonte: Path, destino: str):
        """
        Upload de arquivos para o S3.
        Parameters
        ----------
        destino : str
            local (chave) do objeto (arquivo) no S3.
        fonte : str
            local do arquivo a ser enviado.
        """
        self.client.upload_file(str(fonte.resolve()), self.bucket, destino)