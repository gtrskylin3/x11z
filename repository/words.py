from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Words
from schemas.words import CreateWord, UpdateWord

class WordsRepository:
    @staticmethod
    async def create(session: AsyncSession, data: CreateWord) -> Words:
        new_word = Words(**data.model_dump())
        session.add(new_word)
        await session.commit()
        await session.refresh(new_word)
        return new_word
    @staticmethod
    async def get_by_id(session: AsyncSession, word_id: int) -> Words | None:
        return await session.get(Words, word_id)
    @staticmethod
    async def get_all(session: AsyncSession) -> list[Words]:
        stmt = select(Words).order_by(Words.id)
        result = await session.execute(stmt)
        return list(result.scalars().all())
    @staticmethod
    async def remove(session: AsyncSession, word_id: int) -> bool:
        word = await session.get(Words, word_id)
        if word:
            await session.delete(word)
            await session.commit()
            return True
        return False
    @staticmethod
    async def update(session: AsyncSession, word_id: int, data: UpdateWord) -> Words | None:
        word = await session.get(Words, word_id)
        if word:
            print(data)
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(word, key, value)
            await session.commit()
            await session.refresh(word)
        return word
        
    
words_repository = WordsRepository()
    
    