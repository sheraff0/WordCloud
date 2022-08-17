from dotenv import dotenv_values

config = dotenv_values(".env.local")

LOCAL = config.get("LOCAL")
APP_DIR = "" if LOCAL else "/app/"
STATIC_HOST = config.get("STATIC_HOST", "http://127.0.0.1:8000")
