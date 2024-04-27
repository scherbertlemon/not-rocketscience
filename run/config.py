from not_rocketscience import config
import logging


def run():
    logger = logging.getLogger("config test")
    
    logger.info(config.background)
    logger.info(config.hex_to_rgb(config.background["space_color"]))


if __name__ == "__main__":
    config.init_logging()
    run()