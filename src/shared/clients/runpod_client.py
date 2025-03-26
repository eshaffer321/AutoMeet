import requests
from config.config import settings


class RunPodClient:
    def __init__(self, endpoint_id=None):
        self.endpoint_id = endpoint_id if endpoint_id else settings.runpod.endpoint_id 
        self.api_key = settings.runpod.api_key
        self.base_url = f"https://api.runpod.ai/v2/{self.endpoint_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def run(self, input_payload: dict) -> dict:
        """
        Trigger the RunPod endpoint with a payload and return the result (blocking).
        """
        response = requests.post(
            f"{self.base_url}/run",
            headers=self.headers,
            json={"input": input_payload},
            timeout=60
        )

        response.raise_for_status()
        return response.json()

    def run_async(self, input_payload: dict) -> str:
        """
        Trigger the RunPod endpoint asynchronously. Returns a job ID.
        """
        response = requests.post(
            f"{self.base_url}/run",
            headers=self.headers,
            json={"input": input_payload},
            timeout=10
        )
        response.raise_for_status()
        job = response.json()
        return job.get("id")

    def get_status(self, job_id: str) -> dict:
        """
        Check the status of an async job.
        """
        response = requests.get(
            f"{self.base_url}/status/{job_id}",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_output(self, job_id: str) -> dict:
        """
        Get the final output of a completed async job.
        """
        response = requests.get(
            f"{self.base_url}/output/{job_id}",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()