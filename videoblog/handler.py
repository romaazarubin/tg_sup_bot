from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from main import dp, bot
from config import DATABASE,PG_USER,PG_PASSWORD, ip, \
    admin_id, id_group
import psycopg2
from keyboard import button_sity, menu_application_spb,menu_application_irkt,\
    menu_application_msk, menu_admin, back_main_keyboard


db_connection = psycopg2.connect(dbname=DATABASE, user=PG_USER, password=PG_PASSWORD, host=ip)
cursor = db_connection.cursor()

# admin handler
@dp.message_handler(Command('admin'))
async def admin(message: Message):
    if message.from_user.id == admin_id:
        await bot.send_message(chat_id=admin_id,text='Админ панель', reply_markup=menu_admin)

@dp.callback_query_handler(text_contains='general_statistics')
async def general_statistics(call: CallbackQuery):
    cursor.execute('SELECT count(*) FROM support_stats')
    db_connection.commit()
    count = cursor.fetchone()[0]
    await call.message.answer(text=f'всего заявок: {count}', reply_markup=back_main_keyboard)
    await call.message.delete()

@dp.callback_query_handler(text_contains='back_main_menu')
async def back(call: CallbackQuery):
    await call.message.answer(text='Меню администратора', reply_markup=menu_admin)
    await call.message.delete()

@dp.callback_query_handler(Text(equals=['statistics_moscow', 'statistics_spb', 'statistics_irkutsk']))
async def stats_sity(call: CallbackQuery):
    sity =''
    if call.data == 'statistics_moscow':
        sity = 'Москва'
    elif call.data == 'statistics_spb':
        sity = 'Санкт-Петербург'
    elif call.data == 'statistics_irkutsk':
        sity = 'Иркутск'
    cursor.execute(f"SELECT count(*) FROM support_stats WHERE sity='{sity}'")
    db_connection.commit()
    count = cursor.fetchone()[0]
    await call.message.answer(text=f'всего заявок по городу {sity}: {count}', reply_markup=back_main_keyboard)
    await call.message.delete()

@dp.callback_query_handler(text_contains='delete_application')
async def del_appl(call: CallbackQuery):
    cursor.execute(f"SELECT message_id FROM us_id")
    db_connection.commit()
    message_list = cursor.fetchall()
    if len(message_list) > 0:
        cursor.execute(f"DELETE FROM us_id")
        db_connection.commit()
        for i in range(len(message_list)):
            mes = str(int(str(int(message_list[i][0])+1)[2::]) - 13)
            await bot.delete_message(chat_id=id_group, message_id=mes)
        await call.message.answer(text='удален')
    else:
        await call.message.answer(text='Список пустой')

@dp.callback_query_handler(text_contains='edit_list_manager')
async def edit_list(call: CallbackQuery):
    await call.message.answer(text='Введите ваше действие, ник и город менеджера \nВ виде "ДЕЙСТВИЕ(удалить или добавить) НИК ГОРОД"')



@dp.callback_query_handler(text_contains='stats_manager')
async def stats(call: CallbackQuery):
    await call.message.answer(text='Введите запрос, ник менеджера \nВ виде "Статистика НИК"')





# client handler
@dp.message_handler(Command('start'))
async def start(message: Message):
    if message.chat.id != -763455375:  # and message.from_user.id not in support_id:
        await bot.send_message(chat_id=message.from_user.id, text='Выберите город для обращение к менеджеру', \
                               reply_markup=button_sity)




@dp.callback_query_handler(Text(equals=['Moskva', 'spb', 'Irkutsk']))
async def help(call: CallbackQuery):
    await call.message.delete()
    message_id = call.message.message_id
    user_id = call.from_user.id
    sity = str(call.data)
    cursor.execute(f"SELECT CASE WHEN EXISTS(SELECT user_id FROM us_id WHERE user_id = '{user_id}') THEN 1 ELSE 2 END;")
    row = (cursor.fetchone())[0]
    if row == 2:
        cursor.execute(f"INSERT INTO us_id(user_id,sity,message_id) VALUES ('{user_id}', '{sity}', '{message_id}');")
        db_connection.commit()
        if call.data == 'Moskva':
            await bot.send_message(chat_id=id_group, text=message_id, reply_markup=menu_application_msk)
        elif call.data == 'Irkutsk':
            await bot.send_message(chat_id=id_group, text='Запрос из Иркутска', reply_markup=menu_application_irkt)
        elif call.data == 'spb':
            await bot.send_message(chat_id=id_group, text='Запрос из Санкт-Петербурга', reply_markup=menu_application_spb)
        await call.answer(text='Заявка отправлена, ожидайте ответ от менеджера')
    else:
        await bot.send_message(chat_id=call.from_user.id, text=f'Вы уже отправили запрос, подождите,\
                                                                 в ближайшее время вам ответят')
        await call.answer(text='Заявка не отправлена, у вас есть старый запрос')


@dp.callback_query_handler(Text(equals=['support_spb', 'support_moskva', 'support_irkutsk']))
async def ans(call: CallbackQuery):
    message_id = call.message.message_id
    support_name_moscow = []
    support_name_spb = []
    support_name_irkutsk = []
    if call.data == 'support_moskva':
        support_name_moscow = st('Москва')
    elif call.data == 'support_spb':
        support_name_spb = st('Санкт-Петербург')
    elif call.data == 'support_irkutsk':
        support_name_irkutsk = st('Иркутск')
    if call.data =='support_moskva' and call.from_user.username.lower() in support_name_moscow:
        cursor.execute(f"SELECT user_id FROM us_id WHERE sity='Moskva' LIMIT 1")
        db_connection.commit()
        z = cursor.fetchall()

        for i in z:
            id = i[0]
        support_name = call.from_user.username
        sity = 'Москва'
        try:
            cursor.execute(f"INSERT INTO support_stats(support_name,user_name, sity) VALUES ('{support_name}', '{id}', '{sity}');")
            cursor.execute(f"DELETE FROM us_id WHERE user_id ='{id}'")
            db_connection.commit()
            await call.message.delete()
            await call.answer(text='Заявка принята')
            await bot.send_message(chat_id=id, text=message_id)
        except:
            await call.answer('Заявку уже приняли')

    elif call.data == 'support_spb' and call.from_user.username.lower() in support_name_spb:
        cursor.execute(f"SELECT user_id FROM us_id WHERE sity='spb' LIMIT 1")
        db_connection.commit()
        z = cursor.fetchall()

        for i in z:
            id = i[0]


        support_name = call.from_user.username
        sity = 'Санкт-Петербург'
        try:
            cursor.execute(f"INSERT INTO support_stats(support_name,user_name, sity) VALUES ('{support_name}', '{id}', '{sity}');")
            cursor.execute(f"DELETE FROM us_id WHERE user_id ='{id}'")
            db_connection.commit()
            await call.message.delete()
            await call.answer(text='Заявка принята')
            await bot.send_message(chat_id=id, text=f"Ссылка на менеджера: \n"
                                                    f"{'https://t.me/' + support_name}")
        except:
            await call.answer('Заявку уже приняли')


    elif call.data =='support_irkutsk' and call.from_user.username.lower() in support_name_irkutsk:
        cursor.execute(f"SELECT user_id FROM us_id WHERE sity='Irkutsk' LIMIT 1")
        db_connection.commit()
        z = cursor.fetchall()

        for i in z:
            id = i[0]


        support_name = call.from_user.username
        sity = 'Иркутск'
        try:
            cursor.execute(f"INSERT INTO support_stats(support_name,user_name, sity) VALUES ('{support_name}', '{id}', '{sity}');")
            cursor.execute(f"DELETE FROM us_id WHERE user_id ='{id}'")
            db_connection.commit()
            await call.message.delete()
            await call.answer(text='Заявка принята')
            await bot.send_message(chat_id=id, text=f"Ссылка на менеджера: \n"
                                                    f"{'https://t.me/' + support_name}")
        except:
            await call.answer('Заявку уже приняли')
    else:
        await call.answer('Это не ваш город')


@dp.message_handler(content_types=["text"])
async def word(message: Message):
    if message.from_user.id == admin_id:
        msg = message.text.split()
        if msg[0].lower() == 'добавить':
            try:
                cursor.execute(f"INSERT INTO support_list(sup_name,sup_sity) VALUES ('{msg[1]}','{msg[2]}');")
                db_connection.commit()
                step = 'Менеджер успешно добавлен'
            except:
                step = 'Такого пользователя нет'

        elif msg[0].lower() == 'удалить':
            try:
                cursor.execute(f"DELETE FROM support_list WHERE sup_name= '{msg[1]}' and sup_sity = '{msg[2]}'")
                db_connection.commit()
                step = 'Менеджер успешно удален'
            except:
                step = 'Такого пользователя нет'

        elif msg[0].lower() == 'статистика':
            cursor.execute(f"SELECT count(*) FROM support_stats WHERE support_name ='{msg[1]}'")
            db_connection.commit()
            count = cursor.fetchone()[0]
            step =f'Статистика {msg[1]} = {count} клиентов'


        else:
            step = 'НЕВЕРНЫЙ ЗАПРОС'
        await bot.send_message(chat_id=message.from_user.id, text=step)

def st(sity):
    sup_list = []
    cursor.execute(f"SELECT count(*) FROM support_list WHERE sup_sity ='{sity}'")
    db_connection.commit()
    count = int(cursor.fetchone()[0])
    cursor.execute(f"SELECT sup_name FROM support_list WHERE sup_sity='{sity}'")
    db_connection.commit()
    for i in range(count):
        name = cursor.fetchone()[0].lower()
        sup_list.append(name)
    return sup_list