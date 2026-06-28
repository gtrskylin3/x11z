from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from asyncio import get_running_loop
from schemas.words import CreateWord, Word, UpdateWord
from services.words import word_service
from api.depends.session_dep import SessionDep
from utils_backend.export_anki import export_anki
from utils_backend.remove_file import remove_file
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False) 
templates = Jinja2Templates(directory="templates")

@router.get('/')
async def get_all_words(session: SessionDep, request: Request) -> HTMLResponse:
    words = await word_service.get_all_words(session)
    return templates.TemplateResponse(request, "index.html", {"words": words})


@router.get('/{id}')
async def get_by_id(session: SessionDep, id: int) -> list[Word]:
    words = await word_service.get_word_by_id(session, id)
    return [Word.model_validate(i) for i in words]

@router.post('/')
async def create_words(request: Request, session: SessionDep) -> RedirectResponse:
    form_data = await request.form()
    # Создаем схему
    word_scheme = CreateWord(
        word=form_data.get("word"),
        translate=form_data.get("translate"),
        context=form_data.get("context")
    )
    word = await word_service.create_word(session, word_scheme)
    return RedirectResponse(url="/", status_code=303)
    
@router.post('/delete')
async def delete_word(request: Request, session: SessionDep, id = Form(...)) -> RedirectResponse :
    status = await word_service.delete_word(session, id)
    return RedirectResponse(url="/", status_code=303)
    
@router.post('/update')
async def update_word(request: Request, session: SessionDep) -> RedirectResponse:
    form_data = await request.form()
    update_scheme = UpdateWord(
        word = form_data.get('word'),
        translate = form_data.get('translate', None),
        context = form_data.get('context', None)
    )
    updated_word = await word_service.update_word(session, form_data.get('id'), update_scheme)
    return RedirectResponse(url='/', status_code=303)
    
    
@router.post('/export-anki')
async def export_words(session: SessionDep, background_tasks: BackgroundTasks):
    words = await word_service.get_all_words(session)
    words_list = [
        Word.model_validate(w).model_dump() for w in words
    ]
    loop = get_running_loop()
    output_path = await loop.run_in_executor(None, export_anki, words_list)
    background_tasks.add_task(remove_file, str(output_path))
    return FileResponse(
        output_path,
        filename="anki_cards.apkg", 
        media_type="application/octet-stream"
    )