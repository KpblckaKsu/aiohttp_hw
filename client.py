import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        # --- add adv ---

        response = await session.post(
            "http://127.0.0.1:8080/adv/",
            json={
                "title": "Ugly cat for sale",
                "description": "cheap little annoying bastard for sale",
                "owner": "Doggo",
            },
        )
        json_data = await response.json()
        print(json_data)

        # --- get adv by ID ---

        # response = await session.get(
        #     "http://127.0.0.1:8080/adv/1",)
        # json_data = await response.json()
        # print(json_data)

        # --- change adv ---

        # response = await session.patch(
        #     "http://127.0.0.1:8080/adv/1",
        #     json={
        #         "title": "mr.Cat for sale",
        #         "description": "So cute little kitty",
        #         "owner": "mr.Doggo",
        #     },
        # )
        # json_data = await response.json()
        # print(json_data)

        # --- get changed adv ---

        # response = await session.get(
        #     "http://127.0.0.1:8080/adv/1",)
        # json_data = await response.json()
        # print(json_data)

        # --- delete adv by ID ---

        # response = await session.delete(
        #     "http://127.0.0.1:8080/adv/1", )
        # json_data = await response.json()
        # print(json_data)


asyncio.run(main())
