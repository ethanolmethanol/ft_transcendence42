import asyncio
from back_game.game_arena.arena import Arena
from back_game.game_settings.game_constants import *
import logging
import random
import string

logger = logging.getLogger(__name__)
class Monitor:

    def __init__(self):
        self.channels = {} # key: channelID, value: dict [key: arenaID, value: arena]
        self.userGameTable = {}

    def generateRandomID(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        return "".join(random.choice(letters_and_digits) for _ in range(length))

    async def getChannel(self, user_id, players_pecs):
        channel = self.get_channel_from_user_id(user_id)
        if channel is None:
            return await self.getNewChannel(user_id, players_pecs)
        return channel

    async def getNewChannel(self, user_id, players_pecs):
        newArena = Arena(players_pecs)
        channelID = self.generateRandomID(10)
        self.channels[channelID] = {newArena.id: newArena}
        asyncio.create_task(self.monitor_arenas_loop(channelID, self.channels[channelID]))
        asyncio.create_task(self.run_game_loop(self.channels[channelID].values()))
        self.userGameTable[user_id] = {"channelID": channelID, "arena": newArena.to_dict()}
        return self.userGameTable[user_id]

    def get_channel_from_user_id(self, user_id):
        channel = self.userGameTable.get(user_id)
        if channel is None:
            return None
        channelID = channel["channelID"]
        arenaID = channel["arena"]["id"]
        arena = self.channels[channelID][arenaID]
        channel = {"channelID": channelID, "arena": arena.to_dict()}
        return channel

    def deleteArena(self, arenas, arenaID):
        player_list = arenas[arenaID].players
        for player in player_list.values():
            self.deleteUser(player.user_id)
        arenas.pop(arenaID)

    def addUser(self, user_id, channelID, arenaID):
        self.userGameTable[user_id] = {"channelID": channelID, "arena": self.channels[channelID][arenaID].to_dict()}

    def deleteUser(self, user_id):
        try:
            self.userGameTable.pop(user_id)
            logger.info(f"User {user_id} deleted from userGameTable")
        except KeyError:
            pass

    def is_user_in_game(self, user_id, channelID, arenaID):
        return self.userGameTable.get(user_id) == {"channelID": channelID, "arena": arenaID}

    def deleteChannel(self, channelID):
        del self.channels[channelID]

    async def monitor_arenas_loop(self, channelID, arenas):
        while arenas:
            await self.update_game_states(arenas)
            await asyncio.sleep(MONITOR_LOOP_INTERVAL)
        self.deleteChannel(channelID)

    async def update_game_states(self, arenas):
        for arena in arenas.values():
            if arena.status == STARTED and arena.is_empty():
                arena.conclude_game()
            if arena.status == OVER:
                logger.info(f"Game over in arena {arena.id}")
                await self.gameOver(arenas, arena)
                break

    async def run_game_loop(self, arenas):
        while arenas:
            for arena in arenas:
                if arena.status == STARTED:
                    update_message = arena.update_game()
                    await arena.game_update_callback(update_message)
            await asyncio.sleep(RUN_LOOP_INTERVAL)

    async def gameOver(self, arenas, arena):
        arena.status = DYING
        time = TIMEOUT_GAME_OVER + 1
        while arena.status == DYING and time > 0:
            time -= TIMEOUT_INTERVAL
            await arena.game_over_callback("Game Over! Thank you for playing.", time)
            if time == 0:
                arena.status = DEAD
                self.deleteArena(arenas, arena.id)
            else:
                await asyncio.sleep(TIMEOUT_INTERVAL)

monitor = Monitor()
