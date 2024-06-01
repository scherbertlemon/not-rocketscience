"""
Test script for configuration object
"""
import logging
from not_rocketscience import config


def run():
    """
    accesses some config properties
    """
    logger = logging.getLogger("config test")

    logger.info(config.background_number_of_layers)
    logger.info(config.screen_size)
    logger.info(config)
    logger.info(config.colors)
    logger.debug(config.colors.ship_green)



if __name__ == "__main__":
    config.init_logging()
    run()
