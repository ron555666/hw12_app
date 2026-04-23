import httpx
import os
from dotenv import load_dotenv
load_dotenv()

class AIClient():
    def __init__(self, api_key: str, base_url: str = 'https://api.openai.com/v1') -> None:
        self.api_key = api_key
        self.base_url = base_url

    async def summarize_content(self, content: str) -> str:
        print('content', content)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-5-nano",
                    "input": f"summarize the following content in 10 words: {content}",
                    "store": True
                }
            )

            result = response.json()
            print('result', result)
            return result['output'][1]['content'][0]['text']
    
OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")
api_key = os.getenv("OPENAI_SECRET_KEY")
if not api_key:
    raise RuntimeError("OPENAI_SECRET_KEY not set")

ai_client = AIClient(api_key=api_key)
