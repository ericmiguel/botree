"""Botree S3 utilities."""

from pathlib import Path
from typing import List
from typing import Optional

from boto3.session import Session


class S3:
    """AWS S3 operations."""

    def __init__(self, session: Session, **kwargs):
        """
        S3 class init.

        Parameters
        ----------
        bucket : str
            nome do bucket S3.
        region : str, optional
            região AWS do bucket
        profile : Optional[str], optional
            profile da AWS CLI, by default None.
        """
        self.session = session
        self.client = self.session.client(service_name="s3", **kwargs)

    def download(self, bucket: str, source: Path, output: Path, **kwargs):
        """
        Downloads a file from S3.

        Parameters
        ----------
        output : Path
            local onde será salvo o arquivo escolhido.
        source : str
            local (chave) do objeto (arquivo) no S3.
        """
        self.client.download_file(bucket, str(source), str(output), **kwargs)

    def upload(self, bucket: str, source: Path, output: Path, **kwargs):
        """
        Uploads a file to S3.

        Parameters
        ----------
        output : str
            local (chave) do objeto (arquivo) no S3.
        source : str
            local do arquivo a ser enviado.
        """
        self.client.upload_file(str(source), bucket, str(output), **kwargs)

    def create_bucket(self, name: str, **kwargs):
        """Creates a bucket."""
        self.client.create_bucket(Bucket=name, **kwargs)

    def list_buckets(self) -> List[str]:
        """Returns a list of bucket names."""
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]

    def list_objects(self, bucket, prefix: Optional[str] = "", **kwargs) -> List[str]:
        """Returns a list all objects in a bucket with specified prefix."""
        response = self.client.list_objects(Bucket=bucket, Prefix=prefix, **kwargs)
        return [object["Key"] for object in response["Contents"]]
