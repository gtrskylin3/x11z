from config import settings, BASE_DIR
from pathlib import Path
from secrets import token_hex
import genanki
from random import randint


def export_anki(words_list: list[dict]) -> Path:
    output_filename = BASE_DIR / f'{token_hex(16)}.apkg'
    
    # 1. Создаем модель карточки (стиль и поля)
    my_model = genanki.Model(
        randint(10 ** 9, 10 ** 10), # Любое фиксированное уникальное число
        'Simple Word Model',
        fields=[
            {'name': 'Word'},
            {'name': 'Translate'},
            {'name': 'Context'},
        ],
        templates=[{
            'name': 'Card 1',
            'qfmt': '<div style="font-size: 24px; text-align: center;">{{Word}}</div>',
            'afmt': '''
                {{FrontSide}}
                <hr id="answer">
                <div style="font-size: 20px; text-align: center; color: green;"><b>{{Translate}}</b></div>
                <br>
                <div style="font-size: 16px; text-align: center; color: gray;"><i>{{Context}}</i></div>
            ''',
        }]
    )

    # 2. Создаем саму колоду
    my_deck = genanki.Deck(
        randint(10 ** 9, 10 ** 10), # Любое фиксированное уникальное число
        'Моя Колода Слов' # Название колоды внутри приложения Anki
    )

    # 3. Итерируемся по вашему списку и добавляем карточки
    for w in words_list:
        # Заменяем None на пустую строку, чтобы Anki не ругался на отсутствие контекста
        context_text = w['context'] if w['context'] is not None else ""
        
        note = genanki.Note(
            model=my_model,
            fields=[w['word'], w['translate'], context_text]
        )
        my_deck.add_note(note)

    # 4. Упаковываем в .apkg файл
    genanki.Package(my_deck).write_to_file(str(output_filename))
    
    return output_filename