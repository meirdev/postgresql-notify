import asyncio
import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from psycopg_pool import AsyncConnectionPool


app = FastAPI()

pool = AsyncConnectionPool(os.environ["DB_URL"], open=False)


@app.on_event("startup")
async def startup():
    await pool.open()


@app.on_event("shutdown")
async def shutdown():
    await pool.close()


@app.get("/")
async def index():
    with open("index.html") as fp:
        return HTMLResponse(fp.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def listen():
        async with pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("LISTEN msgs")
                await connection.commit()

                async for notification in connection.notifies():
                    await websocket.send_text(notification.payload)

    task = asyncio.create_task(listen())

    try:
        await websocket.receive_text()
    except WebSocketDisconnect:
        task.cancel()
