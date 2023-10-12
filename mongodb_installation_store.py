import json
from typing import Optional
from slack_sdk.oauth.installation_store.installation_store import InstallationStore
from slack_sdk.oauth.installation_store.models.bot import Bot
from slack_sdk.oauth.installation_store.models.installation import Installation
from pymongo import MongoClient
import logging
from logging import Logger
from slack_sdk.errors import SlackClientConfigurationError
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)


class MongoDBInstallationStore(InstallationStore, AsyncInstallationStore):
    def __init__(
        self,
        client: MongoClient,
        database: str,
        client_id: str,
        historical_data_enabled: bool = True,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.client = client
        self.database = database
        self.collection = self.client[self.database]["installations"]
        self.client_id = client_id
        self._logger = logger
        self.historical_data_enabled = historical_data_enabled

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
        return self._logger

    async def async_save(self, installation: Installation):
        return self.save(installation)

    async def async_save_bot(self, bot: Bot):
        return self.save_bot(bot)

    def save(self, installation: Installation):
        none = "none"
        e_id = installation.enterprise_id or none
        t_id = installation.team_id or none
        workspace_path = f"{self.client_id}/{e_id}-{t_id}"

        self.save_bot(installation.to_bot())

        if self.historical_data_enabled:
            history_version: str = str(installation.installed_at)

            # per workspace
            data = installation.__dict__
            data["key"] = f"{workspace_path}/installer-latest"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-latest"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")
            data["key"] = f"{workspace_path}/installer-{history_version}"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-{history_version}"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

            # per workspace per user
            u_id = installation.user_id or none
            data = installation.__dict__
            data["key"] = f"{workspace_path}/installer-{u_id}-latest"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-{u_id}-latest"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")
            data["key"] = f"{workspace_path}/installer-{u_id}-{history_version}"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-{u_id}-{history_version}"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

        else:
            # per workspace
            data = installation.__dict__
            data["key"] = f"{workspace_path}/installer-latest"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-latest"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

            # per workspace per user
            u_id = installation.user_id or none
            data = installation.__dict__
            data["key"] = f"{workspace_path}/installer-{u_id}-latest"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/installer-{u_id}-latest"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

    def save_bot(self, bot: Bot):
        none = "none"
        e_id = bot.enterprise_id or none
        t_id = bot.team_id or none
        workspace_path = f"{self.client_id}/{e_id}-{t_id}"

        if self.historical_data_enabled:
            history_version: str = str(bot.installed_at)
            data = bot.__dict__
            data["key"] = f"{workspace_path}/bot-latest"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/bot-latest"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")
            data["key"] = f"{workspace_path}/bot-{history_version}"
            response = self.collection.replace_one(
                {"key": f"{workspace_path}/bot-{history_version}"},
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

        else:
            data = bot.__dict__
            data["key"] = f"{workspace_path}/bot-latest"
            response = self.collection.replace_one(
                data,
                upsert=True,
            )
            self.logger.debug(f"MongoDB Response: {response}")

    async def async_find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        return self.find_bot(
            enterprise_id=enterprise_id,
            team_id=team_id,
            is_enterprise_install=is_enterprise_install,
        )

    def find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        if is_enterprise_install:
            t_id = none
        workspace_path = f"{self.client_id}/{e_id}-{t_id}"
        try:
            document = self.collection.find_one({"key": f"{workspace_path}/bot-latest"})
            document.pop("_id")
            document.pop("key")
            self.logger.debug(f"MongoDB Response: {document}")
            return Bot(**document)
        except Exception as e:
            message = f"Failed to find bot installation data for enterprise: {e_id}, team: {t_id}: {e}"
            self.logger.warning(message)
            return None

    async def async_find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        return self.find_installation(
            enterprise_id=enterprise_id,
            team_id=team_id,
            user_id=user_id,
            is_enterprise_install=is_enterprise_install,
        )

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: Optional[str] = None,
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Installation]:
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        if is_enterprise_install:
            t_id = none
        workspace_path = f"{self.client_id}/{e_id}-{t_id}"
        try:
            key = (
                f"{workspace_path}/installer-{user_id}-latest"
                if user_id
                else f"{workspace_path}/installer-latest"
            )
            document = self.collection.find_one({"key": f"{workspace_path}/bot-latest"})
            document.pop("_id")
            document.pop("key")
            self.logger.debug(f"MongoDB Response: {document}")
            installation = Installation(**document)

            if installation is not None and user_id is not None:
                latest_bot_installation = self.find_installation(
                    enterprise_id=enterprise_id,
                    team_id=team_id,
                    is_enterprise_install=is_enterprise_install,
                )
                if (
                    latest_bot_installation is not None
                    and installation.bot_token != latest_bot_installation.bot_token
                ):
                    installation.bot_id = latest_bot_installation.bot_id
                    installation.bot_user_id = latest_bot_installation.bot_user_id
                    installation.bot_token = latest_bot_installation.bot_token
                    installation.bot_scopes = latest_bot_installation.bot_scopes
                    installation.bot_refresh_token = (
                        latest_bot_installation.bot_refresh_token
                    )
                    installation.bot_token_expires_at = (
                        latest_bot_installation.bot_token_expires_at
                    )
            return installation
        except Exception as e:  # skipcq: PYL-W0703
            message = f"Failed to find an installation data for enterprise: {e_id}, team: {t_id}: {e}"
            self.logger.warning(message)
            return None
