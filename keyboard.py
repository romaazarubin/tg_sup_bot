from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_application = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Ответить', callback_data='answer')
            ]
        ]
    )


button_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Москва', callback_data='Moskva')
        ],
        [
            InlineKeyboardButton(text='СПБ', callback_data='spb')
        ],
        [
            InlineKeyboardButton(text='Иркутск', callback_data='Irkutsk')
        ]
    ]
)

menu_application_spb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Принять заявку', callback_data='support_spb')
        ]
    ]
)
menu_application_msk = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Принять заявку', callback_data='support_moskva')
        ]
    ]
)
menu_application_irkt = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Принять заявку', callback_data='support_irkutsk')
        ]
    ]
)

menu_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Общая статистика', callback_data='general_statistics')
        ],
        [
            InlineKeyboardButton(text='Статистика города Москва', callback_data='statistics_moscow')
        ],
        [
            InlineKeyboardButton(text='Статистика города Санкт-Петербург', callback_data='statistics_spb')
        ],
        [
            InlineKeyboardButton(text='Статистика города Иркутск', callback_data='statistics_irkutsk')
        ],
        [
            InlineKeyboardButton(text='Статистика менеджеров', callback_data='stats_manager')
        ],
        [
            InlineKeyboardButton(text='Редактировать список менеджеров', callback_data='edit_list_manager')
        ],
        [
            InlineKeyboardButton(text='Удалить все не принятые заявки', callback_data='delete_application')
        ]

    ]
)

back_main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='На главную', callback_data='back_main_menu')
        ]
    ]
)

list_city = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Москва', callback_data='msk')
        ],
        [
            InlineKeyboardButton(text='СПБ', callback_data='spb')
        ],
        [
            InlineKeyboardButton(text='Иркутск', callback_data='irk')
        ]
    ]
)