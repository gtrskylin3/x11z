from repository.words import WordsRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.words import CreateWord, UpdateWord
from fastapi import HTTPException
from models.words import Words
from utils_backend.translater import translate

class WordsService:
    @staticmethod
    async def create_word(session: AsyncSession, create_data: CreateWord) -> Words:
        try:
            if not create_data.translate :
                create_data.translate = await translate(create_data.word)
            new_word = await WordsRepository.create(session, create_data)
            return new_word
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create word: {e}")
    @staticmethod      
    async def get_word_by_id(session: AsyncSession, word_id: int) -> Words:
        word = await WordsRepository.get_by_id(session, word_id)
        if not word:
            raise HTTPException(status_code=404, detail=f"Word with id {word_id} not found")
        return word
    @staticmethod    
    async def get_all_words(session: AsyncSession) -> list[Words]:
        return await WordsRepository.get_all(session)
    @staticmethod   
    async def update_word(session: AsyncSession, word_id: int, update_data: UpdateWord) -> Words:
        if update_data.word:
            update_data.translate = await translate(update_data.word)
        updated_word = await WordsRepository.update(session, word_id, update_data)
        if not updated_word:
            raise HTTPException(status_code=404, detail=f"Word with id {word_id} not found, cannot update")
        return updated_word
    @staticmethod
    async def delete_word(session: AsyncSession, word_id: int) -> dict:
        deleted = await WordsRepository.remove(session, word_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Word with id {word_id} not found, cannot delete")
        return {"message": f"Word with id {word_id} was successfully deleted."}

word_service = WordsService()

