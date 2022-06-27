from urllib.parse import urlparse
import os
import asyncio
import aiofiles
from tinydb import TinyDB
import aiohttp

db = TinyDB('db2.json')
db_data = db.all()


async def img_downloader(session: aiohttp.ClientSession, img_link: str) -> None:
    async with session.get(img_link) as response:
        img_file_name = urlparse(url=img_link).path.replace("/images/items/", "").replace("/", "_")

        response_content = await response.read()

        async with aiofiles.open(f"./product_images/{img_file_name}", 'wb') as img_file:
            await img_file.write(response_content)
            await img_file.close()


async def main() -> None:
    if not os.path.exists("product_images"):
        os.makedirs("product_images")
    else:
        pass

    async with aiohttp.ClientSession() as session:
        task = []
        print(db_data)
        for single_obj in db_data[:1]:
            for link in single_obj["Original_Image_Src"]:
                print(link)
                task.append(img_downloader(session=session, img_link=link))

        await asyncio.gather(*task)

asyncio.run(main())
