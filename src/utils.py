""" Module containing utility / helper functions """
import logging


def setup_logging(loglevel=logging.INFO) -> None:
    """ Handles the logger setup / configuration

    :param loglevel: Level of logging, e.g. {logging.DEBUG, logging.INFO}
    :return: None
    """
    logging.basicConfig(level=loglevel, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def separate_input_string(x: str, sep: str) -> list[str]:
    """
    Separates string based on separator token sep and returns list of strings.
    E.g. "URL1$URL" --> ["URL1", "URL2"]

    :param x: str -- Input String
    :param sep: str -- Separator Token
    :return: list[str]
    """
    return x.split(sep)
