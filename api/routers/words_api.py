from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from asyncio import get_running_loop
from schemas.words import CreateWord, Word, UpdateWord
from services.words import word_service
from api.depends.session_dep import SessionDep
from utils_backend.export_anki import export_anki
from utils_backend.remove_file import remove_file


router = APIRouter(prefix="/api/words", tags=['Words'])

@router.get('/')
async def get_all_words(session: SessionDep) -> list[Word]:
    words = await word_service.get_all_words(session)
    return [Word.model_validate(i) for i in words]

@router.get('/{id}')
async def get_by_id(session: SessionDep, id: int) -> list[Word]:
    words = await word_service.get_word_by_id(session, id)
    return [Word.model_validate(i) for i in words]

@router.post('/', response_model = Word)
async def create_words(session: SessionDep, word_scheme: CreateWord) -> Word:
    word = await word_service.create_word(session, word_scheme)
    return Word.model_validate(word)
    
@router.delete('/{id}')
async def delete_word(session: SessionDep, id: int):
    status = await word_service.delete_word(session, id)
    return status
    
@router.patch('/{id}')
async def update_word(session: SessionDep, id: int, update_scheme: UpdateWord) -> Word:
    updated_word = await word_service.update_word(session, id, update_scheme)
    return Word.model_validate(updated_word)
    
    
@router.post('/export_anki')
async def export_words(session: SessionDep, background_tasks: BackgroundTasks):
    words = await word_service.get_all_words(session)
    words_list = [
        Word.model_validate(w).model_dump() for w in words
    ]
    loop = get_running_loop()
    output_path = await loop.run_in_executor(None, export_anki, words_list)
    background_tasks.append(remove_file(str(output_path)))
    return FileResponse(
        output_path,
        filename="anki_cards.apkg", 
        media_type="application/octet-stream"
    )