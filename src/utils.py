""" Module containing utility / helper functions """
import logging


def setup_logging(loglevel=logging.INFO) -> None:
    """ Handles the logger setup / configuration

    :param loglevel: Level of logging, e.g. {logging.DEBUG, logging.INFO}
    :return: None
    """
    logging.basicConfig(level=loglevel,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S")
