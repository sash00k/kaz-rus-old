import os
from dotenv import load_dotenv, find_dotenv


class Parser:
    def __init__(self, _version=5.131):
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        self.__token: str = os.environ.get("TOKEN")
        self.__version: float = _version

    def get_token(self) -> str:
        return self.__token

    def get_version(self) -> float:
        return self.__version