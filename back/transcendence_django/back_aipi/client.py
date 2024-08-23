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
    BOTTOM_SLOT,
    LEFT_SLOT,
    RIGHT_SLOT,
    TOP_SLOT,
)
from transcendence_django.dict_keys import (
    ARENA,
    ARENA_ID,
    BALL,
    CODE,
    COLLIDED_SLOT,
    DIRECTION,
    ERROR,
    GAME_ERROR,
    GAME_MESSAGE,
    GAME_OVER,
    GAME_UPDATE,
    HEIGHT,
    JOIN,
    MAP,
    MESSAGE,
    MOVE_PADDLE,
    PADDLE,
    PADDLES,
    PLAYER,
    PLAYERS,
    POSITION,
    REMATCH,
    SCORES,
    SLOT,
    START_TIMER,
    TIME,
    TYPE,
    UPDATE,
    USER_ID,
    WIDTH,
)

from .constants import CALC_PRECISION, DUMB_PRECISION, MAX_CONNECT_ATTEMPTS

now = datetime.now

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile="/etc/ssl/public.crt", keyfile="/etc/ssl/private.key")
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# ssl_context.load_verify_locations(cafile='/etc/ssl/public.crt')

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
        await self.attempt_to_connect()
        self.goodbye()

    async def attempt_to_connect(self):
        retries: int = 0
        while retries < MAX_CONNECT_ATTEMPTS:
            try:
                await self.connect()
            except websockets.ConnectionClosed as e:
                logger.warning(
                    "%s: Connection lost! Reason: %s, code: %s. Retrying...",
                    self.id,
                    e.reason,
                    e.code,
                )
            except asyncio.TimeoutError:
                logger.error("%s: Connection attempt timed out. Retrying...", self.id)
            except asyncio.CancelledError:
                break
            finally:
                backoff_time = 2 ** min(retries, 5)
                retries += 1
                if backoff_time > 1 and retries < MAX_CONNECT_ATTEMPTS:
                    logger.info("%s: Reconnecting in %s seconds", self.id, backoff_time)
                    await asyncio.sleep(backoff_time)
        logger.error("%s: Stopping after %s retries", self.id, retries)

    async def connect(self):
        async with websockets.connect(
            self.url, open_timeout=10, ssl=ssl_context
        ) as websocket:
            logger.info(
                "%s: Connected to WebSocket server %s",
                self.id,
                self.url,
            )
            await self.join(websocket)
            await self.play(websocket)

    async def join(self, websocket):
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

    async def play(self, websocket):
        while True:
            message = await websocket.recv()
            # logger.info(f"Received message: {message}")
            response = self.answer_message(message)
            if len(response) > 0:
                # logger.info(f"Sending response: {response}")
                await websocket.send(response)

    def goodbye(self):
        logger.info("%s: Ended -- %s", self.id, now())
        sys.exit()

    def answer_message(self, message: str) -> str:
        def __content_from_msg_type(content: Any) -> str:
            return str(
                {GAME_MESSAGE: MESSAGE, GAME_UPDATE: UPDATE, GAME_ERROR: ERROR}.get(
                    str(content)
                )
                if not None
                else ""
            )

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
                        CODE: 42,
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
            timeout: int | None = game_over.get(TIME)
            if timeout is not None and timeout == 0:
                self.goodbye()
            return ""

        def __upd_scores(data: Any) -> str:
            if len(self.arena[PADDLES]) == 2:
                upd_arena = self.arena
                index: int = int(data) - 1
                upd_arena[SCORES][index] += 1
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
            logger.debug("%s: Received game arena: %s", self.id, self.arena)
            return ""

        def __upd_paddle(paddle: dict[str, Any]) -> str:
            self.arena[PADDLES][paddle[SLOT] - 1][POSITION].update(paddle[POSITION])
            return ""

        def __upd_ball(ball: dict[str, Any]) -> str:
            brains: list[Callable[[dict[str, Any]], str]] = [
                self.__dumb_brain,
                self.__calc_brain,
            ]
            if len(self.arena[PLAYERS]) == 2 and self.slot in (LEFT_SLOT, RIGHT_SLOT):
                score_difference = (
                    self.arena[SCORES][LEFT_SLOT - 1]
                    - self.arena[SCORES][RIGHT_SLOT - 1]
                ) * (-1 if self.slot == RIGHT_SLOT else 1)
                brain = 1 if score_difference < 0 else 0
            else:
                raise NotImplementedError("Which brain when more than 2 players?")
            return brains[brain](ball)

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
            content.get(CODE),
            content.get(MESSAGE),
        )
        return ""

    def __dumb_brain(self, ball: dict[str, Any]) -> str:
        paddle = self.arena[PADDLES][self.slot - 1]
        # Deltas between the ball and paddle
        dx: float = ball[POSITION]["x"] - paddle[POSITION]["x"]
        dy: float = ball[POSITION]["y"] - paddle[POSITION]["y"]
        is_vertical = paddle[SLOT] in {LEFT_SLOT, RIGHT_SLOT}
        # Basically, if ball is up go up, if down go down
        return self.__direction_of_paddle(
            is_vertical,
            paddle,
            dy if is_vertical else dx,
            DUMB_PRECISION + random.random() / 2.0,
        )

    def __calc_brain(self, ball: dict[str, Any]) -> str:
        # Rate of change of ball position dx and dy
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
        # Time to paddle aka how many times the rate of change till the ball and paddle meet
        # (if dp is 0, the ball is perpendicular to the paddle and will never meet it)
        time_to_paddle = 0
        if dp != 0:
            time_to_paddle = abs(
                paddle_pos - self.arena[BALL][POSITION]["x" if is_vertical else "y"]
            ) / abs(dp)
        # Find where the ball intersects with the paddle axis
        target_pos = ball_pos + time_to_paddle * (dy if is_vertical else dx)
        # If ball intersects with paddle axis outside range of map, wrap the value
        while target_pos < 0 or target_pos > map_size:
            if target_pos < 0:
                target_pos = -target_pos  # Reflect off the top/left
            elif target_pos > map_size:
                target_pos = 2 * map_size - target_pos  # Reflect off the bottom/right
        # If ball moves towards me, move towards its calculated target position
        if self.__ball_moving_towards_me(is_vertical, paddle, dx, dy):
            paddle_delta = target_pos - (paddle_y if is_vertical else paddle_x)
        # Otherwise return to the center of the axis segment
        else:
            paddle_delta = (map_size / 2) - (paddle_y if is_vertical else paddle_x)
        self.arena[BALL][POSITION].update(ball[POSITION])
        return self.__direction_of_paddle(
            is_vertical, paddle, paddle_delta, CALC_PRECISION
        )

    def __direction_of_paddle(
        self,
        is_vertical: bool,
        paddle: dict[str, Any],
        delta: float,
        precision: float,
    ) -> str:
        paddle_size = paddle[HEIGHT] if is_vertical else paddle[WIDTH]
        # If paddle delta isn't within the paddle, move the paddle accordingly
        direction: int = (
            -1
            if delta < -paddle_size * precision
            else 1 if delta > paddle_size * precision else 0
        )
        if direction:
            return json.dumps(
                {TYPE: MOVE_PADDLE, MESSAGE: {PLAYER: self.name, DIRECTION: direction}}
            )
        return ""

    def __ball_moving_towards_me(
        self, is_vertical: bool, paddle: dict[str, Any], dx: float, dy: float
    ) -> bool:
        if is_vertical:
            return (paddle[SLOT] == LEFT_SLOT and dx < 0) or (
                paddle[SLOT] == RIGHT_SLOT and dx > 0
            )
        return (paddle[SLOT] == TOP_SLOT and dy < 0) or (
            paddle[SLOT] == BOTTOM_SLOT and dy > 0
        )
