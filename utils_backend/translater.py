from config import settings
from aiohttp import ClientSession
from fastapi import HTTPException

async def translate(text: str, from_lang='en', to_lang='ru'):
    url = settings.API_URL
    params = {
        "q": text,
        "langpair": f"{from_lang}|{to_lang}",
        "de": settings.EMAIL
    }
    async with ClientSession() as session:
        response = await session.get(url, params=params, timeout = 10)
        if response.status !=  200:
            raise HTTPException(status_code=400, detail='MyMemory API ERROR')
        data = await response.json()
        if data.get('responseStatus') != 200: 
            error_msg = data.get("responseDetails", "Unknown error")
            raise HTTPException(status_code=400, detail=f"MyMemory Error: {error_msg}")
        translated_word =  data["responseData"]["translatedText"]   
        if translated_word.lower() == text.lower():
            raise HTTPException(status_code=400, detail=f"Can't translate automaticly")
        return translated_word