import requests
import io
import uuid

from PIL import Image

from generative_monster.settings import HUGGINGFACE_API_TOKEN


class OpenJourneyGenerator:
	
    def __init__(self):
        self._api_url = "https://api-inference.huggingface.co/models/prompthero/openjourney"
        self._headers = {
             "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
        }


    def _query(self, payload):
        response = requests.post(
            self._api_url,
            headers=self._headers,
            json=payload)
        return response.content


    def generate(self, prompt):
        image_bytes = self._query({
            "inputs": prompt,
        })
        image = Image.open(io.BytesIO(image_bytes))
        id = uuid.uuid4().hex
        image_path = f"/tmp/generated_{id}.jpg"
        image.save(image_path)
        return image_path