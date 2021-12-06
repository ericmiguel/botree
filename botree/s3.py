"""Botree S3 utilities."""

from pathlib import Path
from typing import List
from typing import Optional

from boto3.session import Session


class Bucket:
    """AWS S3 Bucket level transactions."""

    def __init__(
        self,
        session: Session,
        name: str,
        client_kwargs: dict = dict(),
        resource_kwargs: dict = dict(),
    ):
        self.name = name
        self.session = session
        self.client = self.session.client(service_name="s3", **client_kwargs)
        self.resource = self.session.resource("s3", **resource_kwargs).Bucket(
            name=self.name
        )

    def download(self, source: Path, target: Path, **kwargs):
        """
        Downloads a file from S3.

        Parameters
        ----------
        source : Path
            remote file path.
        target : Path
            local file path.
        """
        self.resource.download_file(str(source), str(target), **kwargs)

    def upload(self, source: Path, target: Path, **kwargs):
        """
        Uploads a file to S3.

        Parameters
        ----------
        source : Path
            local file path.
        target : Path
            remote file path.
        """
        self.resource.upload_file(str(source), str(target), **kwargs)

    def copy(
        self,
        source: Path,
        target: Path,
        source_bucket: Optional[str] = None,
        *args,
        **kwargs
    ):
        """
        Copy an object stored in the bucket or from another bucket.

        If source_bucket is not specified, the object is copied from the current bucket.

        if target_key has no suffix, it assumes target_key is a folder and source_key
        file name is used.

        Parameters
        ----------
        source : Path
            source file path
        target : Path
            target file path. If target_key has no suffix, it assumes target_key
            is a folder.
        source_bucket : Optional[str], optional
            bucket from wich source file will be copied from, by default None
        """
        copy_source = {"Bucket": source_bucket, "Key": str(source)}

        if not source_bucket:
            copy_source.update({"Bucket": self.name})

        if not target.suffix:
            target = target / source.name

        self.client.copy(copy_source, self.name, str(target), **kwargs)

    def list_objects(
        self,
        prefix: str = "",
        only_folders: bool = False,
        *args, **kwargs
    ) -> List[str]:
        """Returns a list all objects in a bucket with specified prefix."""
        delimiter = "/" if only_folders else ""
        response_key = "CommonPrefixes" if only_folders else "Contents"
        response_item_key = "Prefix" if only_folders else "Key"

        if only_folders and not prefix.endswith("/"):
            prefix = prefix + "/"

        response = self.client.list_objects_v2(
            Bucket=self.name, Prefix=prefix, Delimiter=delimiter, *args, **kwargs
        )

        return [object[response_item_key] for object in response[response_key]]

    def delete(self, target: Path, **kwargs):
        """
        Delete a file from S3.

        Parameters
        ----------
        target : Path
            remote file path.
        """
        self.client.delete_object(Bucket=self.name, Key=str(target), **kwargs)


class S3:
    """AWS S3 operations."""

    def __init__(self, session: Session, **kwargs):
        """
        S3 class init.

        Parameters
        ----------
        region : str, optional
            região AWS do bucket
        profile : Optional[str], optional
            profile da AWS CLI, by default None.
        """
        self.session = session
        self.client = self.session.client(service_name="s3", **kwargs)

    def create_bucket(self, name: str, *args, **kwargs):
        """Creates a bucket."""
        self.client.create_bucket(Bucket=name, *args, **kwargs)

    def list_buckets(self) -> List[str]:
        """Returns a list of bucket names."""
        response = self.client.list_buckets()
        return [bucket["Name"] for bucket in response["Buckets"]]

    def bucket(
        self,
        name: str,
        client_kwargs: dict = dict(),
        resource_kwargs: dict = dict(),
    ) -> Bucket:
        """Get a bucket resource instance."""
        return Bucket(self.session, name, **client_kwargs, **resource_kwargs)
