from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # SECRET_KEY: str = os.environ["SECRET_KEY"]
    SECRET_KEY: str = os.environ.get("SECRET_KEY","eto_hack_i_mne_poh_na_kiberbez")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()
