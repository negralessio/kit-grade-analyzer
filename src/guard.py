""" Module to clean and validate input url """
import src.constants as constants


class Guard:

    def __init__(self, url: str):
        self.url = url

    def check_input(self) -> bool:
        if self._check_if_url_starts_correctly():
            return True
        else:
            return False

    def _check_if_url_starts_correctly(self) -> bool:
        return self.url.startswith(constants.HOST)
