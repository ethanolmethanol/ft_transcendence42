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
    retries = 0
    game_ongoing = True
    has_joined = False
    while game_ongoing:
        try:
            async with websockets.connect(
                websocket_url,
                open_timeout=10,
                ssl=ssl_context
            ) as websocket:
                logger.info(f"Connected to WebSocket server {websocket_url}")
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
                    logger.info(f"Received message: {message}")
                    response = handle_data(message, ai_user_id)
                    if len(response) > 0:
                        logger.info(f"Sending response: {response}")
                        await websocket.send(response)  # Send a response back to the server
        except websockets.ConnectionClosed as e:
            logger.warning(f"Connection lost! Reason: {e.reason}, code: {e.code}. Retrying...")
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
            else:
                logger.info(f"! connect failed; reconnecting in {backoff_time} seconds")
            await asyncio.sleep(backoff_time)

def handle_data(message: str, ai_user_id: int) -> str:
    data: Dict[str: Any] = json.loads(message)
    msg_type: str = data["type"]
    logger.info(f"Received message type: {msg_type}")
    match msg_type:
        case "game_message":
            logger.info(f"Received game message: {data['message']}")
        case "game_update":
            if data['update'].get('game_over') is not None:
                exit()
            # if data['update']['arena'] is not None:
            #     data['update']['arena']['ball']
            ball: Dict[str: Any] = data['update'].get('ball')
            if ball is None:
                return ""

            direction = 1 #isMovingUp ? -1 : isMovingDown ? 1 : 0;
            return json.dumps({'type': 'move_paddle',
                'message': {"player": f"bot{ai_user_id}", "direction": direction}})
        case "game_error":
            logger.warning(f"Received game error: {data['error']['message']}")
            if (int)(data['error']['code']) != 1:
                exit()
        case _:
            pass
    return ""
