"""Botree Secrets Manager utilities."""

import json
import uuid

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

from boto3.session import Session


class SecretsManager:
    """AWS Secrets Manager wrapper."""

    def __init__(
        self,
        session: Session,
        client_kwargs: dict = dict(),
    ):
        self.session = session
        self.client = self.session.client(
            service_name="secretsmanager", **client_kwargs
        )

    def list_secrets(self, *args, **kwargs) -> dict:
        """
        Returns a list of all stored secrets.

        Acctually, this returns a list of all secrets within the Boto3 limit of 100.

        Parameters
        ----------
        shorten : bool, optional
            Exclude the response metadata. By default True.

        Returns
        -------
        dict
            List of secrets and, optionally, metadata.
        """
        secrets = self.client.list_secrets(*args, **kwargs)

        return secrets

    def generate_password(
        self,
        shorten: Optional[bool] = True,
        length: int = 32,
        exclude_characters: str = "",
        exclude_numbers: bool = False,
        exclude_punctuation: bool = False,
        exclude_uppercase: bool = False,
        exclude_lowercase: bool = False,
        exclude_space: bool = True,
        include_each_type: bool = True,
    ) -> dict:
        r"""
        Generates a strong random password.

        Parameters
        ----------
        shorten : bool, optional.
            Exclude the response metadata. By default True.
        length : int, optional
            The length of the password. If you don't include this parameter,
            by default 32
        exclude_characters : str, optional
            A string of the characters that you don't want in the password,
            by default ""
        exclude_numbers : bool, optional
            Specifies whether to exclude numbers from the password, by default False.
            If false, numbers will be included.
        exclude_punctuation : bool, optional
            Specifies whether to exclude the following punctuation characters from the
            password: ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~ .
            If False, the password can contain punctuation.
        exclude_uppercase : bool, optional
            Specifies whether to exclude uppercase letters from the password, by default
            False. If False, the password can contain uppercase letters.
        exclude_lowercase : bool, optional
            Specifies whether to exclude lowercase letters from the password,
            by default False. If False, the password can contain lowercase letters.
        exclude_space : bool, optional
            Specifies whether to include the space character, by default True.
            If False, the password can contain space characters.
        include_each_type : bool, optional
            Specifies whether to include at least one upper and lowercase letter,
            one number, and one punctuation, by default True. If True,
            the password contains at least one of every character type.

        Returns
        -------
        Mapping[Dict[str, str], Dict[str, models.ResponseMetadata]]
            Random password and, optionally, metadata.
        """
        random_password = self.client.get_random_password(
            PasswordLength=length,
            ExcludeCharacters=exclude_characters,
            ExcludeNumbers=exclude_numbers,
            ExcludePunctuation=exclude_punctuation,
            ExcludeUppercase=exclude_uppercase,
            ExcludeLowercase=exclude_lowercase,
            IncludeSpace=exclude_space,
            RequireEachIncludedType=include_each_type,
        )

        return random_password

    def delete_secret(
        self, name: str, recovery_window: int = 30, force_delete: bool = False
    ) -> dict:
        """
        Delete an existing secret.

        Parameters
        ----------
        name : str
            Secret name.
        recovery_window : int, optional
            The number of days that Secrets Manager waits before permanently
            deleting the secret, by default 30.
        force_delete : bool, optional
            Specifies whether to delete the secret without any recovery window.
            You can't use both this parameter and RecoveryWindowInDays in the same
            call. If you don't use either, then Secrets Manager defaults to a 30
            day recovery window, by default False.

        Returns
        -------
        Dict[str, Union[str, datetime, models.ResponseMetadata]]
            Metadata.
        """
        kwargs: Dict[str, Union[int, bool]] = dict()
        if force_delete:
            kwargs.update({"ForceDeleteWithoutRecovery": force_delete})
        else:
            kwargs.update({"RecoveryWindowInDays": recovery_window})

        response = self.client.delete_secret(SecretId=name, **kwargs)

        return response

    def get_secret(
        self, name: str, shorten: Optional[bool] = True, *args, **kwargs
    ) -> Dict[str, Union[str, Dict[str, str], List[str], int, datetime]]:
        """
        Get a secret from AWS Secrets Manager by name.

        Optionally, output can be shortened by selecting only the secret itself.

        Parameters
        ----------
        name : str
            Secret name as in AWS Secrets Manager.
        shorten : bool, optional
            Automatically filters the JSON and removes the response details,
            by default True

        Returns
        -------
        Dict[str, Union[str, Dict[str, str], List[str], int, datetime]]
            Chosen secret.
        """
        secret = self.client.get_secret_value(SecretId=name, *args, **kwargs)

        return secret

    def create_secret(
        self, name: str, secret: Dict[str, Any], description: str, *args, **kwargs
    ) -> Dict[str, Union[str, Dict[str, str], List[str], int, datetime]]:
        """
        Create a new secret.

        Parameters
        ----------
        name : str
            Secret name.
        secret : Dict[str, Any]
            Secret content.
        description : str
            Secret AWS description.

        Returns
        -------
        Dict[str, Union[str, Dict[str, str], List[str], int, datetime]]
            Chosen secret.
        """
        request_token = str(uuid.uuid4())
        self.client.create_secret(
            Name=name,
            ClientRequestToken=request_token,
            Description=description,
            SecretString=json.dumps(secret),
            *args,
            **kwargs,
        )

        return self.get_secret(name, shorten=True)
