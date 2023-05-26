from dotenv import load_dotenv
import os
load_dotenv()

DEBUG = False
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# Configure Postgres database; the full username for PostgreSQL flexible server is
# username (not @sever-name).
DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'], #+ ".postgres.database.azure.com",
    dbname=os.environ['DBNAME']
)