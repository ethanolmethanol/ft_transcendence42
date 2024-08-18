from back_game.app_settings.base_consumer import BaseConsumer
from back_game.app_settings.game_logic_interface import GameLogicInterface


class ClassicConsumer(BaseConsumer):

    def get_game_logic_interface(self):
        return GameLogicInterface(is_tournament=False)

class TournamentConsumer(BaseConsumer):

    def get_game_logic_interface(self):
        return GameLogicInterface(is_tournament=True)
