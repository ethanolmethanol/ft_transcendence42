import asyncio
import logging
import websockets
import json
import ssl
from typing import Any, Dict

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile='/etc/ssl/serv.crt', keyfile='/etc/ssl/serv.key')
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# ssl_context.load_verify_locations(cafile='/etc/ssl/serv.crt')

logger = logging.getLogger(__name__)

async def client(websocket_url: str, ai_user_id: int, arena_id: str):
    logger.info(f"AIPI client joining {websocket_url}")
    retries: int = 0
    game_ongoing: bool = True
    has_joined: bool = False
    arena: Dict[str: Any] = {}
    while game_ongoing:
        try:
            async with websockets.connect( websocket_url, open_timeout=10,
                ssl=ssl_context ) as websocket:
                logger.info(f"{"Re-" if has_joined else ""}Connected to WebSocket server {websocket_url}")
                retries = 0
                if not has_joined:
                    await websocket.send(json.dumps(
                        {'type': 'join',
                         'message': {
                             'user_id': ai_user_id,
                             'player': f"bot{ai_user_id}",
                             'arena_id': arena_id
                         }}))
                    has_joined = True
                while game_ongoing:
                    message = await websocket.recv()  # Await the coroutine
                    # logger.info(f"Received message: {message}")
                    response = handle_data(message, ai_user_id, arena)
                    if len(response) > 0:
                        # logger.info(f"Sending response: {response}")
                        await websocket.send(response)  # Send a response back to the server
        except websockets.ConnectionClosed as e:
            logger.warning(f"Connection lost! Reason: {e.reason}, code: {e.code}. Retrying...")
            has_joined = False
        except asyncio.TimeoutError:
            logger.error("Connection attempt timed out. Retrying...")
        except asyncio.CancelledError as e:
            logger.error(f"Cancelled Error occurred: {e}. Stopping retries.")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        finally:
            backoff_time = 2 ** min(retries, 5)  # Exponential backoff with a max wait time
            retries += 1
            if retries == 5:
                logger.error(f"! connect failed; stopping after {retries} retries")
                break
            elif backoff_time > 1:
                logger.info(f"! connect failed; reconnecting in {backoff_time} seconds")
                await asyncio.sleep(backoff_time)

def handle_data(message: str, ai_user_id: int, arena: dict[str: Any]) -> str:
    data: Dict[str: Any] = json.loads(message)
    msg_type: str = data["type"]
    # logger.info(f"Received message type: {msg_type}")
    match msg_type:
        case "game_message": logger.info(f"Received game message: {data['message']}")
        case "game_update":
            update = data.get('update')
            if not update:
                logger.warning(f"Empty update? {message}")
                return ""
            if update.get('game_over') is not None: exit()
            if update.get('start_timer') is not None:
                logger.info(f"Received start timer: {update['start_timer']}")
                return ""
            if update.get('arena') is not None:
                arena.clear()
                arena.update(update['arena'])
                logger.info(f"Received game arena: {arena}")
                return ""
            if update.get('paddle') is not None:
                paddle = update['paddle']
                if paddle: arena["paddles"][paddle["slot"] - 1]["position"].update(paddle["position"])
                else: logger.warning(f"Empty paddle update? {message}")
                return ""
            ball: Dict[str: Any] = update.get('ball')
            if not arena:
                logger.warning(f"NO ARENA???? {message}")
                return ""
            if ball is None:
                logger.warning(f"Unknown update {message}")
                return ""
            paddle =  arena["paddles"][0]
            dx: int = ball["position"]["x"] - paddle["position"]["x"]
            dy: int = ball["position"]["y"] - paddle["position"]["y"]
            direction = -1 if dy < -paddle["height"] * 0.75 else 1 if dy > paddle["height"] * 0.75 else 0;
            if direction:
                return json.dumps({'type': 'move_paddle',
                'message': {"player": f"bot{ai_user_id}", "direction": direction}})
        case "game_error":
            logger.warning(f"Received game error: {data['error']['message']}")
            if (int)(data['error']['code']) != 1:
                exit()
        case _:
            pass
    return ""

# {"type": "game_update", "update": {
#     "arena": {"id": "140301557308336", "status": 2, "players": ["Player1", "Player2"],
#               "scores": [0, 0],
#               "ball": {"position": {"x": 500.0, "y": 300.0}, "speed": {"x": 7.58946638440411, "y": -2.5298221281347035, "absolute_velocity": 7.999999999999999}, "radius": 15},
#             "paddles": [{"slot": 1, "player_name": "Player1", "position": {"x": 10, "y": 300}, "speed": 0.025, "width": 20, "height": 100}, {"slot": 2, "player_name": "Player2", "position": {"x": 990, "y": 300}, "speed": 0.025, "width": 20, "height": 100}], "map": {"width": 1000, "height": 600}, "players_specs": {"nb_players": 2, "type": "local"}}}}