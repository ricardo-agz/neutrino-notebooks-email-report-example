import os
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from ssl import CERT_NONE

load_dotenv()


def connect_db():
    config = {
        "DB_NAME": os.getenv("DB_NAME", "TestDB"),
        "DB_URL": os.getenv("DB_URL", None),
        "ENV": os.getenv("ENV", "prod")
    }

    db_name = config["DB_NAME"] if config["ENV"] == 'prod' else f'{config["DB_NAME"]}Testing'
    db_host = f'{config["DB_URL"]}/{db_name}?retryWrites=true&w=majority'

    try:
        disconnect()
        connect(
            host=db_host,
            tls=True,
            tlsAllowInvalidCertificates=True
        )

        print(f"Connected to {'production' if config['ENV'] == 'prod' else 'testing'} database at: {db_host}...")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")