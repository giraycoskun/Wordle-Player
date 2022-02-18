"""

Player Class

Automated Wordle player based on Selenium

Returns:
    _type_: _description_
"""

import logging
import logging.config
import time

from os import getenv
from dotenv import load_dotenv

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class Player:
    """_summary_

    Returns:
        _type_: _description_
    """

    letter_dict = {
        'q': (1, 1),
        'w': (1, 2),
        'e': (1, 3),
        'r': (1, 4),
        't': (1, 5),
        'y': (1, 6),
        'u': (1, 7),
        'i': (1, 8),
        'o': (1, 9),
        'p': (1, 10),

        'a': (2, 2),
        's': (2, 3),
        'd': (2, 4),
        'f': (2, 5),
        'g': (2, 6),
        'h': (2, 7),
        'j': (2, 8),
        'k': (2, 9),
        'l': (2, 10),

        'enter': (3, 1),
        'z': (3, 2),
        'x': (3, 3),
        'c': (3, 4),
        'v': (3, 5),
        'b': (3, 6),
        'n': (3, 7),
        'm': (3, 8),
        'back': (3, 9)
    }

    def __init__(self) -> None:
        self.logger = logging.getLogger('Player')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.result = {}
        self.row = 1

    def play(self):
        """_summary_
        """

        self.driver.get(getenv('WORDLE_WEB_ADRESS'))
        self.__close_refrence_box()
        self.__write_letter('c')
        self.__write_letter('r')
        self.__write_letter('a')
        self.__write_letter('n')
        self.__write_letter('e')
        self.__write_letter('enter')

        line_result = self.__get_results()
        self.result.update(line_result)

        time.sleep(5)

        self.__write_letter('c')
        self.__write_letter('r')
        self.__write_letter('a')
        self.__write_letter('n')
        self.__write_letter('e')
        self.__write_letter('enter')

        line_result = self.__get_results()
        self.result.update(line_result)

        self.driver.implicitly_wait(10)  # seconds
        self.driver.quit()

    def __check_availability(self):
        # TODO
        self.__write_letter('t')
        js_path = f'return document.querySelector("body > game-app")\
            .shadowRoot.querySelector("#board > game-row:nth-child({self.row})")'

    def __close_refrence_box(self):
        js_path = 'return document.querySelector("body > game-app")\
            .shadowRoot.querySelector("#game > game-modal")\
            .shadowRoot.querySelector("div > div > div > game-icon")\
            .shadowRoot.querySelector("svg")'
        close_element = self.driver.execute_script(js_path)
        close_element.click()

    def __write_letter(self, letter):
        row, column = self.letter_dict[letter]
        js_path = f'return document.querySelector("body > game-app").shadowRoot\
            .querySelector("#game > game-keyboard").shadowRoot.querySelector\
            ("#keyboard > div:nth-child({row}) > button:nth-child({column})")'
        letter = self.driver.execute_script(js_path)
        letter.click()

    def __get_results(self):
        line_result = {}
        for letter_column in range(1, 6):
            letter, evaluation = self.__get_result(letter_column)
            line_result[letter] = (evaluation, letter_column)
        self.row += 1
        return line_result

    def __get_result(self, letter_column):
        js_path = f'return document.querySelector("body > game-app")\
            .shadowRoot.querySelector("#board > game-row:nth-child({self.row})")\
            .shadowRoot.querySelector("div > game-tile:nth-child({letter_column})")'
        tile_element = self.driver.execute_script(js_path)
        evaluation = tile_element.get_attribute('evaluation')
        letter = tile_element.get_attribute('letter')
        self.logger.debug("Line: %d -> Letter: %s - Evaluation: %s",
                          letter_column, letter, evaluation)
        return letter, evaluation


if __name__ == '__main__':
    load_dotenv()
    logging.config.fileConfig(getenv('LOG_CONF_FILE'))

    player = Player()
    player.play()
