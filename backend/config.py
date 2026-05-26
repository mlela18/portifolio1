import os
from dotenv import load_dotenv

load_dotenv()

def _get_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in ('1', 'true', 'yes')

class Config:
    DB_FILE = os.getenv('DB_FILE', os.path.join(os.path.dirname(__file__), 'contacts.db'))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = _get_bool('FLASK_DEBUG', False)

    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587')) if os.getenv('SMTP_PORT') else None
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_USE_TLS = _get_bool('SMTP_USE_TLS', True)
    EMAIL_FROM = os.getenv('EMAIL_FROM')
