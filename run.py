# @Ranigal-co
"""
    Запуск сервера
"""
from app import create_app
from config import DevelopmentConfig
import os

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)