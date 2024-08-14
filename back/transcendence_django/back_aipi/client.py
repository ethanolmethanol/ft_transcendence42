import asyncio
import logging
import websockets
import json
import random
import time
import ssl
from typing import Any, Callable, Dict

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile='/etc/ssl/serv.crt', keyfile='/etc/ssl/serv.key')
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# ssl_context.load_verify_locations(cafile='/etc/ssl/serv.crt')

logger = logging.getLogger(__name__)

class AipiClient:
    def __init__(self, websocket_url: str, ai_user_id: int, arena_id: str) -> None:
        self.id: int = ai_user_id
        self.url: str = websocket_url
        self.arena_id: str = arena_id
        self.retries: int = 0
        self.game_ongoing: bool = True
        self.has_joined: bool = False
        self.arena: Dict[str: Any] = {}

    async def run(self):
        logger.info(f"AIPI client joining {self.url}")
        while self.game_ongoing:
            try:
                async with websockets.connect( self.url, open_timeout=10,
                    ssl=ssl_context ) as websocket:
                    logger.info(f"{"Re-" if self.has_joined else ""}Connected to WebSocket server {self.url}")
                    self.retries = 0
                    if not self.has_joined:
                        await websocket.send(json.dumps(
                            {'type': 'join',
                            'message': {
                                'user_id': self.id,
                                'player': f"bot{self.id}",
                                'arena_id': self.arena_id
                            }}))
                        self.has_joined = True
                    while self.game_ongoing:
                        message = await websocket.recv()  # Await the coroutine
                        # logger.info(f"Received message: {message}")
                        response = self.handle_data(message)
                        if len(response) > 0:
                            # logger.info(f"Sending response: {response}")
                            await websocket.send(response)  # Send a response back to the server
            except websockets.ConnectionClosed as e:
                logger.warning(f"Connection lost! Reason: {e.reason}, code: {e.code}. Retrying...")
                self.has_joined = False
            except asyncio.TimeoutError:
                logger.error("Connection attempt timed out. Retrying...")
            except asyncio.CancelledError as e:
                logger.error(f"Cancelled Error occurred: {e}. Stopping retries.")
                break
            # except Exception as e:
            #     logger.error(f"An unexpected error occurred: {e}")
            finally:
                backoff_time = 2 ** min(self.retries, 5)  # Exponential backoff with a max wait time
                self.retries += 1
                if self.retries == 5:
                    logger.error(f"! connect failed; stopping after {self.retries} retries")
                    break
                elif backoff_time > 1:
                    logger.info(f"! connect failed; reconnecting in {backoff_time} seconds")
                    await asyncio.sleep(backoff_time)

    def handle_data(self, message: str) -> str:
        data: Dict[str: Any] = json.loads(message)
        # msg_type: str = data["type"]
        return self.__unwrap_from_type(
            self.__unwrap_from_type("type", {"type": lambda x: x.removeprefix("game_") if x is not None else ""}, data), {
            "message": self.__h_message,
            "update": self.__h_update,
            "error": self.__h_error,
        }, data)


    def __unwrap_from_type(self, cnt_type: str, handlers: dict[str: Callable[[dict[str, Any]], str]],
                      data: dict[str: Any], quit_if_none: bool = False) -> str:
        content = data.get(cnt_type)
        if content is None:
            if quit_if_none:
                return ""
            logger.warning(f"{self.id}: Received empty {cnt_type}: {data}")
        try:
            return handlers[cnt_type](content)
        except KeyError:
            return self.__h_error({"error": {"message": f"No such key [{cnt_type}] within keys [{data.keys()}]", "code": 42}})
    
    def __h_message(self, content: dict[str: Any]) -> str:
        # if rematch, respond rematch
        logger.info(f"{self.id}: Received game message: {content}")
        return ""

    def __h_update(self, content: dict[str: Any]) -> str:
        def __do_nun(_) -> str:
            return ""
        def __upd_arena(arena: dict[str: Any]) -> str:
            self.arena.clear()
            self.arena.update(arena)
            # logger.info(f"Received game arena: {self.arena}")
            return ""
        def __upd_paddle(paddle: dict[str: Any]) -> str:
            self.arena["paddles"][paddle["slot"] - 1]["position"].update(paddle["position"])
            return ""
        def __upd_ball(ball: dict[str: Any]) -> str:
            paddle = self.arena["paddles"][0]
            dx: int = ball["position"]["x"] - paddle["position"]["x"]
            dy: int = ball["position"]["y"] - paddle["position"]["y"]
            direction = -1 if dy < -paddle["height"] * 0.85 else 1 if dy > paddle["height"] * 0.85 else 0;
            if not random.randint(0, 20):
                time.sleep(0.025) # skill issue
            if direction:
                return json.dumps({'type': 'move_paddle',
                                'message': {"player": f"bot{self.id}", "direction": direction}})
            return ""
        actions = {
            "game_over": __do_nun,
            "start_timer": __do_nun,
            "arena": __upd_arena,
            "paddle": __upd_paddle,
            "ball": __upd_ball,
        }
        res: str = ""
        for t in actions.keys():
            res += self.__unwrap_from_type(t, actions, content, True)
        return res

    def __h_error(self, content: dict[str: Any]) -> str:
        logger.error(f"{self.id}: Received error: #{content.get('code')} -- {content.get('message')}")
        return ""

# {"type": "game_update", "update": {
#     "arena": {"id": "140301557308336", "status": 2, "players": ["Player1", "Player2"],
#               "scores": [0, 0],
#               "ball": {"position": {"x": 500.0, "y": 300.0}, "speed": {"x": 7.58946638440411, "y": -2.5298221281347035, "absolute_velocity": 7.999999999999999}, "radius": 15},
#             "paddles": [{"slot": 1, "player_name": "Player1", "position": {"x": 10, "y": 300}, "speed": 0.025, "width": 20, "height": 100}, {"slot": 2, "player_name": "Player2", "position": {"x": 990, "y": 300}, "speed": 0.025, "width": 20, "height": 100}], "map": {"width": 1000, "height": 600}, "players_specs": {"nb_players": 2, "type": "local"}}}}