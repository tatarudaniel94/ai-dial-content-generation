import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-4o",
        api_key=API_KEY
    )

    base64_message = ContentedMessage(
        role=Role.USER,
        content=[
            TxtContent(text="What do you see in this image? Describe it in detail."),
            ImgContent(image_url=ImgUrl(url=f"data:image/png;base64,{base64_image}"))
        ]
    )
    response = client.get_completion(messages=[base64_message])
    print(f"\nAssistant: {response.content}\n")

    url_message = ContentedMessage(
        role=Role.USER,
        content=[
            TxtContent(text="What animal is shown in this image? Describe it."),
            ImgContent(image_url=ImgUrl(url="https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"))
        ]
    )
    response = client.get_completion(messages=[url_message])
    print(f"\nAssistant: {response.content}\n")


start()