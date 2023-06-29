import asyncio
import os

import psycopg


async def main():
    async with await psycopg.AsyncConnection.connect(os.environ["DB_URL"]) as connection:
        async with connection.cursor() as cursor:
            while True:
                msg = input("Enter message: ")

                if not msg:
                    continue

                if msg == "exit":
                    break

                await cursor.execute("SELECT pg_notify(%s, %s)", ("msgs", msg))
                await connection.commit()


if __name__ == "__main__":
    asyncio.run(main())
