import os
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from app import app
from dotenv import load_dotenv

async def main():
    env = os.getenv("APP_ENV", "development") # デフォルトはdevelopment 
    env_file = f".env.{env}" # 指定したファイルを読み込む 
    load_dotenv(dotenv_path=env_file)
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    config.reload = False  # 必要に応じて True に変更可能
    await serve(app, config)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🍄 CTRL+C を受け取りました。Hypercorn サーバーを終了します。")
