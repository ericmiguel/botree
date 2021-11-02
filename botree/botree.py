"""Botree core functions."""
from typing import Optional

from boto3.session import Session
from botree.s3 import S3


class Botree:
    def __init__(
        self,
        region: str,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        profile: Optional[str] = None,
    ):
        """
        Botree wrapper.

        Parameters
        ----------
        bucket : str
            nome do bucket S3.
        region : str, optional
            região AWS do bucket
        profile : Optional[str], optional
            profile da AWS CLI, by default None.
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.region = region
        self.profile = profile
        self.session = Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            region_name=region,
            profile_name=profile,
        )

    @property
    def s3(self) -> S3:
        return S3(self.session)
