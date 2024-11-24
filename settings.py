
# Scrape settings
HTTP_PROXY_URL = "http://username:password@host:port"
MAX_RETRY_COUNT = 5
HTTP_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

# DB settings for mysql, postgresql and...
# DB_TYPE = "mysql"
# DB_HOST = "127.0.0.1"
# DB_PORT = "3306"
# DB_USERNAME = "root"
# DB_PASSWORD = "PUT YOUR DB PASSWORD"
# DB_NAME = "insta_fastapi_db"
# SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DB settings
SQLALCHEMY_DATABASE_URL = f"sqlite:///insta_fastapi_db.db"

