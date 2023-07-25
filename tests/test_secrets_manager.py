from moto import mock_secretsmanager


def test_list_secrets(botree_session):
    with mock_secretsmanager():
        secrets_names = ["botree-dev-1", "botree-dev-2"]

        for secret_name in secrets_names:
            botree_session.secrets_manager.create_secret(
                name=secret_name,
                secret={"user": "username", "pass": "areallystrongpassword"},
                description="it`s only a test",
            )

        existing_secrets = botree_session.secrets_manager.list_secrets()

        for existing_secret in existing_secrets["SecretList"]:
            assert existing_secret["Name"] in secrets_names


def test_create_a_secret(botree_session):
    with mock_secretsmanager():
        new_secret_name = "botree-dev"

        botree_session.secrets_manager.create_secret(
            name=new_secret_name,
            secret={"user": "username", "pass": "areallystrongpassword"},
            description="it`s only a test",
        )

        existing_secrets = botree_session.secrets_manager.list_secrets()

        assert existing_secrets["SecretList"][0]["Name"] == new_secret_name


def test_delete_a_secret(botree_session):
    with mock_secretsmanager():
        new_secret_name = "botree-dev"

        botree_session.secrets_manager.create_secret(
            name=new_secret_name,
            secret={"user": "username", "pass": "areallystrongpassword"},
            description="it`s only a test",
        )

        botree_session.secrets_manager.delete_secret(new_secret_name, force_delete=True)

        existing_secrets = botree_session.secrets_manager.list_secrets()

        assert len(existing_secrets["SecretList"]) == 0


def test_get_a_secret(botree_session):
    with mock_secretsmanager():
        new_secret_name = "botree-dev"

        botree_session.secrets_manager.create_secret(
            name=new_secret_name,
            secret={"user": "username", "pass": "areallystrongpassword"},
            description="it`s only a test",
        )

        existing_secrets = botree_session.secrets_manager.list_secrets()

        assert existing_secrets["SecretList"][0]["Name"] == new_secret_name
