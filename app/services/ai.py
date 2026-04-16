import httpx

async def get_ai_rate_data(article_body: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.openai.com/gpt-4o-mini/", article_body)
        response.raise_for_status()
        return response.json()