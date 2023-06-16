import requests
import shutil
import time
import uuid

from generative_monster.settings import LEAP_API_TOKEN


class LeapGenerator:
	
    def __init__(self):
        # TODO Add more models
        self._model_id = "8b1b897c-d66d-45a6-b8d7-8e32421d02cf"
        self._api_url = f"https://api.tryleap.ai/api/v1/images/models/{self._model_id}/inferences"
        self._headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {LEAP_API_TOKEN}"
        }
        self._negative_prompt = (
            "out of frame, lowres, text, error, cropped, worst quality, low quality, "
            "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra "
            "fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, "
            "deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, "
            "cloned face, disfigured, gross proportions, malformed limbs, missing arms, "
            "missing legs, extra arms, extra legs, fused fingers, too many fingers, "
            "long neck, username, watermark, signature"
        )
        self._request_delay = 5
        self._max_requests = 10


    def _query(self, url, method="POST", **kwargs):
        if method == "POST":
            response = requests.post(url, headers=self._headers, **kwargs)
        elif method == "GET":
            response = requests.get(url, headers=self._headers, **kwargs)
        else:
            raise Exception(f"Method {method} not supported")
        return response.json()


    def _query_generation(self, prompt):
        payload = {
            "prompt": prompt,
            "negativePrompt": self._negative_prompt,
            "steps": 50,
            "width": 512,
            "height": 512,
            "numberOfImages": 1,
            "promptStrength": 7,
            # "seed": 31337,
            "enhancePrompt": False,
            "upscaleBy": "x1",
            "sampler": "ddim"
        } 
        response = self._query(self._api_url, json=payload)
        return response["id"]


    def _query_inference_job(self, inference_id):
        finished = False
        count_requests = 0
        while not finished:
            inference_url = f"{self._api_url}/{inference_id}"
            response = self._query(inference_url, method="GET")
            if "state" in response:
                inference_state = response["state"]
                finished = inference_state == "finished"
            if "images" in response:
                inference_images = response["images"]
                if len(inference_images) > 0:
                    image_url = response["images"][0]["uri"]
            time.sleep(self._request_delay)
            print("Still processing...")
            if count_requests > self._max_requests:
                print("Giving up...")
                return None
            count_requests += 1
        return image_url


    def _download_image(self, image_url):
        response = requests.get(image_url, stream=True)
        image_path = None
        if response.status_code == 200:
            response.raw.decode_content = True
            id = uuid.uuid4().hex
            image_path = f"/tmp/generated_{id}.jpg"
            with open(image_path,'wb') as f:
                shutil.copyfileobj(response.raw, f)
        else:
            raise Exception("Image couldn't be downloaded")
        return image_path


    def generate(self, prompt):
        inference_id = self._query_generation(prompt)
        image_url = self._query_inference_job(inference_id)
        if not image_url:
            return None
        image_path = self._download_image(image_url)
        return image_path