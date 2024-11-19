from pGerrit.client import GerritClient
from requests.auth import HTTPBasicAuth

from gerrit import GerritClient
client = GerritClient(base_url="http://10.10.96.212:8081", username='zixiangliu', password='123123123')

project = client.projects.get("MyProjects")