import asyncio
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as client:
        for i, attachment in enumerate(attachments):
            if attachment.url:
                image_bytes = await client.get_file(attachment.url)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}_{i}.png"
                with open(filename, 'wb') as f:
                    f.write(image_bytes)
                print(f"Image saved: {filename}")


def start() -> None:
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="dall-e-3",
        api_key=API_KEY
    )

    message = Message(
        role=Role.USER,
        content="Sunny day on Bali"
    )

    custom_fields = {
        "size": Size.square,
        "style": Style.vivid,
        "quality": Quality.hd
    }

    response = client.get_completion(messages=[message], custom_fields=custom_fields)
    print(f"\n{response.content}")

    if response.custom_content and response.custom_content.attachments:
        asyncio.run(_save_images(response.custom_content.attachments))


start()
