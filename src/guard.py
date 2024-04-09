""" Module to clean and validate input url """
import logging
import src.constants as constants

logger = logging.getLogger(__name__)


class Guard:

    def __init__(self, url: str):
        self.url = url

    def check_input(self) -> bool:
        logger.debug("Checking user input via Guard Class ...")
        if self._check_if_url_starts_correctly():
            return True
        else:
            return False

    def _check_if_url_starts_correctly(self) -> bool:
        logger.debug("Checking if URL starts correctly of Guard with URL: %s", self.url)
        return self.url.startswith(constants.HOST)
