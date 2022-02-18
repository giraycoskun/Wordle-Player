"""
Wordle Solver
- Player automated by Selenium and a paralel subprocess solver based on information theory
"""

import logging
import logging.config
from os import getenv
from dotenv import load_dotenv

from player import Player

load_dotenv()
logging.config.fileConfig(getenv('LOG_CONF_FILE'))
logger = logging.getLogger()

if __name__ == '__main__':
    logger.debug("I AM HERE 1")
    player = Player()
    player.test()
