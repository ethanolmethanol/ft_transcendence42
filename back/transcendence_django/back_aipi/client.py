import asyncio
import json
import logging
import random
import ssl
import sys
from datetime import datetime
from typing import Any, Callable, Dict

import websockets
from back_game.game_settings.game_constants import (
    LEFT_SLOT,
    RIGHT_SLOT,
    TOP_SLOT,
    BOT_SLOT,
)
from transcendence_django.dict_keys import (
    HEIGHT,
    POSITION,
    WIDTH,
    BALL,
    PADDLE,
    PADDLES,
    ARENA,
    TYPE,
    JOIN,
    MESSAGE,
    UPDATE,
    ERROR,
    USER_ID,
    PLAYER,
    ARENA_ID,
    REMATCH,
    MOVE_PADDLE,
    START_TIMER,
    SLOT,
    GAME_OVER,
    DIRECTION,
    MAP,
    GAME_MESSAGE,
    GAME_ERROR,
    GAME_UPDATE,
    TIME,
    SCORES,
    COLLIDED_SLOT,
    PLAYERS,
)

now = datetime.now

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile="/etc/ssl/serv.crt", keyfile="/etc/ssl/serv.key")
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# ssl_context.load_verify_locations(cafile='/etc/ssl/serv.crt')

logger = logging.getLogger(__name__)


class AipiClient:
    def __init__(self, websocket_url: str, ai_user_id: int, arena_id: str) -> None:
        self.id: int = ai_user_id
        self.name: str = f"bot{self.id}"
        self.url: str = websocket_url
        self.arena_id: str = arena_id
        self.rematching: bool = False
        self.arena: Dict[str, Any] = {}
        self.slot: int = 0

    async def run(self):
        logger.info("%s: Start -- %s", self.id, now())
        retries: int = 0
        game_ongoing: bool = True
        has_joined: bool = False
        while game_ongoing:
            try:
                async with websockets.connect(
                    self.url, open_timeout=10, ssl=ssl_context
                ) as websocket:
                    logger.info(
                        "%s: %sConnected to WebSocket server %s",
                        self.id,
                        "Re-" if has_joined else "",
                        self.url,
                    )
                    retries = 0
                    if not has_joined:
                        await websocket.send(
                            json.dumps(
                                {
                                    TYPE: JOIN,
                                    MESSAGE: {
                                        USER_ID: self.id,
                                        PLAYER: self.name,
                                        ARENA_ID: self.arena_id,
                                    },
                                }
                            )
                        )
                        has_joined = True
                    while game_ongoing:
                        message = await websocket.recv()  # Await the coroutine
                        # logger.info(f"Received message: {message}")
                        response = self.handle_data(message)
                        if len(response) > 0:
                            # logger.info(f"Sending response: {response}")
                            await websocket.send(
                                response
                            )  # Send a response back to the server
            except websockets.ConnectionClosed as e:
                logger.warning(
                    "Connection lost! Reason: %s, code: %s. Retrying...",
                    e.reason,
                    e.code,
                )
                has_joined = False
            except asyncio.TimeoutError:
                logger.error("Connection attempt timed out. Retrying...")
            except asyncio.CancelledError:
                break
            # except Exception as e:
            #     logger.error(f"An unexpected error occurred: {e}")
            finally:
                backoff_time = 2 ** min(
                    retries, 5
                )  # Exponential backoff with a max wait time
                retries += 1
                if retries == 5:
                    logger.error(
                        "! connect failed; stopping after %s retries", retries
                    )
                    game_ongoing = False
                if backoff_time > 1:
                    logger.info(
                        "! connect failed; reconnecting in %s seconds", backoff_time
                    )
                    await asyncio.sleep(backoff_time)
        self.goodbye()

    def goodbye(self):
        logger.info("%s: Ended -- %s", self.id, now())
        sys.exit()

    def handle_data(self, message: str) -> str:
        def __content_from_msg_type(content: Any) -> str:
            return str({GAME_MESSAGE: MESSAGE, GAME_UPDATE: UPDATE, GAME_ERROR: ERROR}.get(
                content
            )) if not None else ""

        data: Dict[str, Any] = json.loads(message)
        return self.__unwrap_from_type(
            self.__unwrap_from_type(TYPE, {TYPE: __content_from_msg_type}, data),
            {
                MESSAGE: self.__h_message,
                UPDATE: self.__h_update,
                ERROR: self.__h_error,
            },
            data,
        )

    def __unwrap_from_type(
        self,
        cnt_type: str,
        handlers: dict[str, Callable[[Any | dict[str, Any]], str]],
        data: dict[str, Any],
        quit_if_none: bool = False,
    ) -> str:
        content: Any = data.get(cnt_type)
        if content is None:
            if quit_if_none:
                return ""
            logger.warning("%s: Received empty %s: %s", self.id, cnt_type, data)
        try:
            return handlers[cnt_type](content)
        except KeyError:
            return self.__h_error(
                {
                    ERROR: {
                        MESSAGE: f"No such key [{cnt_type}] within keys [{data.keys()}]",
                        "code": 42,
                    }
                }
            )

    def __h_message(self, content: dict[str, Any]) -> str:
        message: str = str(content)
        logger.info("%s: Received game message: %s", self.id, message)
        if REMATCH in message and not self.rematching:  # if rematch, respond rematch
            self.rematching = True
            return json.dumps({TYPE: REMATCH, MESSAGE: {}})
        return ""

    def __h_update(self, content: dict[str, Any]) -> str:
        def __do_nun(_) -> str:
            self.rematching = False
            return ""

        def __game_over(game_over: dict[str, Any]) -> str:
            timeout = game_over.get(TIME)
            if timeout is not None and not int(timeout):
                self.goodbye()
            return ""

        def __upd_scores(data: Any) -> str:
            if len(self.arena[PADDLES]) == 2:
                upd_arena = self.arena
                upd_arena[SCORES][int(data) - 1] += 1
                self.arena.update(upd_arena)
            else:
                raise NotImplementedError(
                    "implement when more than 2 players (subtract from score?)"
                )
            return ""

        def __upd_arena(arena: dict[str, Any]) -> str:
            self.arena.clear()
            self.arena.update(arena)
            self.slot = next(
                (
                    x + 1
                    for x, player in enumerate(self.arena[PLAYERS])
                    if player == self.name
                ),
                0,
            )
            if not self.slot:
                raise KeyError(
                    f"{self.id}: Cannot find myself within arena's given player list."
                )
            # logger.info(f"Received game arena: {self.arena}")
            return ""

        def __upd_paddle(paddle: dict[str, Any]) -> str:
            self.arena[PADDLES][paddle[SLOT] - 1][POSITION].update(paddle[POSITION])
            return ""

        def __upd_ball(ball: dict[str, Any]) -> str:
            brains: list[Callable[[dict[str, Any]], str]] = [
                self.__dumb_brain,
                self.__calc_brain,
            ]
            if len(self.arena[PLAYERS]) == 2:
                score_difference = (
                    self.arena[SCORES][self.slot - 1]
                    - self.arena[SCORES][0 if self.slot == 2 else 1]
                )
                brain = 1 if score_difference < 0 else 0
            else:
                raise NotImplementedError("Which brain when more than 2 players?")
            return brains[brain](ball)  # self.brain

        actions = {
            GAME_OVER: __game_over,
            START_TIMER: __do_nun,
            ARENA: __upd_arena,
            PADDLE: __upd_paddle,
            BALL: __upd_ball,
            COLLIDED_SLOT: __upd_scores,
        }
        res: str = ""
        for t in actions:
            res += self.__unwrap_from_type(t, actions, content, True)
        return res

    def __h_error(self, content: dict[str, Any]) -> str:
        logger.error(
            "%s: Received error: #%s -- %s",
            self.id,
            content.get('code'),
            content.get(MESSAGE),
        )
        return ""

    def __dumb_brain(self, ball: dict[str, Any]) -> str:
        paddle = self.arena[PADDLES][self.slot - 1]
        dx: float = ball[POSITION]["x"] - paddle[POSITION]["x"]
        dy: float = ball[POSITION]["y"] - paddle[POSITION]["y"]
        precision: float = 0.70 + random.random() / 2.0
        direction: int = 0
        if paddle[SLOT] == LEFT_SLOT or paddle[SLOT] == RIGHT_SLOT:
            direction = (
                -1
                if dy < -paddle[HEIGHT] * precision
                else 1 if dy > paddle[HEIGHT] * precision else 0
            )
        elif paddle[SLOT] == TOP_SLOT or paddle[SLOT] == BOT_SLOT:
            direction = (
                -1
                if dx < -paddle[WIDTH] * precision
                else 1 if dx > paddle[WIDTH] * precision else 0
            )
        if direction:
            return json.dumps(
                {TYPE: MOVE_PADDLE, MESSAGE: {PLAYER: self.name, DIRECTION: direction}}
            )
        return ""

    def __calc_brain(self, ball: dict[str, Any]) -> str:
        dx: float = ball[POSITION]["x"] - self.arena[BALL][POSITION]["x"]
        dy: float = ball[POSITION]["y"] - self.arena[BALL][POSITION]["y"]
        paddle: dict[str, Any] = self.arena[PADDLES][self.slot - 1]
        paddle_x = paddle[POSITION]["x"]
        paddle_y = paddle[POSITION]["y"]
        is_vertical = paddle[SLOT] in {LEFT_SLOT, RIGHT_SLOT}
        dp = dx if is_vertical else dy
        paddle_pos = paddle_x if is_vertical else paddle_y
        map_size = self.arena[MAP][HEIGHT] if is_vertical else self.arena[MAP][WIDTH]
        ball_pos = self.arena[BALL][POSITION]["y" if is_vertical else "x"]
        time_to_paddle = 0
        if dp != 0:
            time_to_paddle = abs(paddle_pos - self.arena[BALL][POSITION]
                                 ["x" if is_vertical else "y"]) / abs(dp)
        target_pos = ball_pos + time_to_paddle * (dy if is_vertical else dx)
        while target_pos < 0 or target_pos > map_size:
            if target_pos < 0:
                target_pos = -target_pos  # Reflect off the top/left
            elif target_pos > map_size:
                target_pos = 2 * map_size - target_pos  # Reflect off the bottom/right
        if self.__ball_moving_towards_me(is_vertical, paddle, dx, dy):
            paddle_delta = target_pos - (paddle_y if is_vertical else paddle_x)
        else:
            paddle_delta = (map_size / 2) - (paddle_y if is_vertical else paddle_x)
        self.arena[BALL][POSITION].update(ball[POSITION])
        return self.__direction_of_paddle(is_vertical, paddle, paddle_delta)

    def __direction_of_paddle(self,
            is_vertical: bool,
            paddle: dict[str, Any],
            paddle_delta,
        ) -> str:
        precision: float = 0.85
        paddle_size = paddle[HEIGHT] if is_vertical else paddle[WIDTH]
        direction: int = (
            -1 if paddle_delta < -paddle_size * precision
            else 1 if paddle_delta > paddle_size * precision else 0
        )
        if direction:
            return json.dumps(
                {TYPE: MOVE_PADDLE, MESSAGE: {PLAYER: self.name, DIRECTION: direction}}
            )
        return ""


    def __ball_moving_towards_me(self,
            is_vertical: bool,
            paddle: dict[str, Any],
            dx: float,
            dy: float
        ) -> bool:
        if is_vertical:
            return (paddle[SLOT] == LEFT_SLOT and dx < 0) \
                  or (paddle[SLOT] == RIGHT_SLOT and dx > 0)
        return (paddle[SLOT] == TOP_SLOT and dy < 0) \
              or (paddle[SLOT] == BOT_SLOT and dy > 0)
