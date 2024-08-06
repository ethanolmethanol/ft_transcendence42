# import asyncio
import logging
import websockets

logger = logging.getLogger(__name__)

async def client(websocket_url: str):
    async for websocket in websockets.connect(websocket_url):
        logger.info(f"Connected to Websocket server {websocket_url}")
        try:
            async for message in websocket:
            # Process message received on the connection.
                logger.info(message)
        except websockets.ConnectionClosed:
            logger.info("Connection lost! Retrying..")
            continue #continue will retry websocket connection by exponential back off 
