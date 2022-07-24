import os

CLIENT_ID = "f821b9f7-4cb5-479d-9084-a976d891e3df" # Application (client) ID of app registration

CLIENT_SECRET = "._p8Q~oS58hJ.mqW-lRFZepcMI_VjHBUhvgmPcsS" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

SQL_SERVER = os.environ.get('SQL_SERVER') or 'cms-test-eca.database.windows.net'
SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'test-cms-ed'
SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'ActuarialDevOps'
SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'Bungee1!'
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://' + SQL_USER_NAME + '@' + SQL_SERVER + ':' + SQL_PASSWORD + '@' + SQL_SERVER + ':1433/' + SQL_DATABASE + '?driver=ODBC+Driver+17+for+SQL+Server'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

UPLOAD_FOLDER = '/path/to/the/uploads'

BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'logstoragecms'
BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'R6LhDWC+thC9VQe4xTBk88FafjReBQ8INJQhHFvvEIq3tSyksNu4NYrwiCekNFqyFnCodRSYTRDK+AStp+Z00w=='
BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'testing-ed'
BLOB_URL='DefaultEndpointsProtocol=https;AccountName=logstoragecms;AccountKey=R6LhDWC+thC9VQe4xTBk88FafjReBQ8INJQhHFvvEIq3tSyksNu4NYrwiCekNFqyFnCodRSYTRDK+AStp+Z00w==;EndpointSuffix=core.windows.net'
