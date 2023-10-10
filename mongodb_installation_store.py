from slack_sdk.oauth.installation_store.installation_store import InstallationStore
from pymongo import MongoClient


class MongoDBInstallationStore(InstallationStore):
    def __init__(self, client: MongoClient, database: str):
        self.client = client
        self.database = database
        self.collection = self.client[self.database]["installations"]

    def save(self, installation):
        data = vars(installation)
        if data["is_enterprise_install"] and data["enterprise"]:
            return self.collection.replace_one(
                {"enterprise_id": data["enterprise_id"]},
                data,
                upsert=True,
            )
        if data["team_id"]:
            return self.collection.replace_one(
                {"team_id": data["team_id"]},
                data,
                upsert=True,
            )
        return "Failed saving installation data to installationStore"

    def find_installation(self, enterprise_id, team_id, is_enterprise_install):
        if is_enterprise_install and enterprise_id:
            document = self.collection.find_one({"enterprise_id": enterprise_id})
            if not document:
                return document
            else:
                document.pop("_id")
                document.pop("installed_at")
                return document
        if team_id:
            document = self.collection.find_one({"team_id": team_id})
            if not document:
                return document
            else:
                document.pop("_id")
                document.pop("installed_at")
                return document
        return "Failed fetching installation"
