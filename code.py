import telebot
from telebot import types
import ast
import random  # чтобы отправлять случайную картинку из списка
import datetime
from time import sleep, time
from functools import wraps

TOKEN = '1768268284:AAEmnrx9HHxjZgd6eDmmjgfKptnPAsHY6e0'

bot = telebot.TeleBot(TOKEN)

chat_id = 0
old_desc_rem_ind = 0
old_time_rem = 0
curr_reminder = ""
reminders = {}
reminders_time_list = []
thereminder = ""
curr_day = datetime.datetime.today() #чтобы автоматически определялось, какой сейчас год
new = ''
deadlines_to_print = {} #при выводе формат гггг-дд-мм, что неудобно, а пофиксить на самом выводе не получается, поэтому таким путем делаем
look_tasks = {}
data_list = []  # можно и словарь типа {"описание": данные, "дедлайн": данные, "важность": данные} сделать, но нужно ли?
image_list = [
    'https://images.unsplash.com/photo-1511044568932-338cba0ad803?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/photo-1494256997604-768d1f608cac?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1101&q=80']
# пока в списке две произвольных картинки с котами
# я думаю, стоит загрузить все нужные нам картинки в отдельную папку на гитхабе + давать ссылки туда, чтобы точно ничего не сломалось
thing = ''  # стоит назвать эти переменные как-то нормально... это для редактирования
thing2 = ''
thing3 = ''


def mult_threading(func):
    """Декоратор для запуска функции в отдельном потоке"""

    @wraps(func)
    def wrapper(*args_, **kwargs_):
        import threading
        func_thread = threading.Thread(target=func, args=tuple(args_), kwargs=kwargs_)
        func_thread.start()
        return func_thread

    return wrapper

@mult_threading
def send_rem():
    while True:
        for time_rem in reminders_time_list:
            curr_time = datetime.datetime.today()
            curr_time_str = "{}.{}.{} {}:{}".format(curr_time.day, curr_time.month, curr_time.year, curr_time.hour, curr_time.minute)
            print(curr_time_str, "-----", reminders[time_rem][1])
            if curr_time_str == reminders[time_rem][1]:
                for i in range(len(reminders[time_rem][0])):
                    to_print = "Напоминание: {}".format(reminders[time_rem][0][i])
                    bot.send_message(chat_id, text=to_print)
                    reminders[time_rem][0].remove(reminders[time_rem][0][i])
                    if len(reminders[time_rem][0]) == 0:
                        del reminders[time_rem]
                        reminders_time_list.remove(time_rem)

send_rem()

@bot.message_handler(commands=['start'])
def what_to_do(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Записать новое дело', 'Посмотреть записанные дела', 'Создать напоминание', 'Посмотреть напоминания')
    bot.send_message(message.from_user.id, 'Что Вы хотите сделать?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def new(message, f=None):
    if message.text == 'Посмотреть записанные дела':
        keyboard2 = types.ReplyKeyboardMarkup(True, True)
        keyboard2.row('Сортировать дела', 'Не сортировать')
        sort = bot.send_message(message.from_user.id, "Сортировать дела?", reply_markup=keyboard2)
        bot.register_next_step_handler(sort, qstn)

    elif message.text == 'Записать новое дело':
        msg = bot.send_message(message.from_user.id, 'Напишите, как называется ваше дело')
        bot.register_next_step_handler(msg, get_new)

    elif message.text == 'Создать напоминание':
        msg = bot.send_message(message.from_user.id, 'О чем мне нужно Вам напомнить?')
        global chat_id
        chat_id = message.from_user.id
        bot.register_next_step_handler(msg, add_reminder)

    elif message.text == 'Посмотреть напоминания':
        if len(reminders_time_list) == 0:
            bot.send_message(message.from_user.id, "Пока нет никаких напоминаний")
        else:
            for time in reminders_time_list:
                for i in reminders[time][0]:
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    key_delete_rem = types.InlineKeyboardButton(text='Удалить', callback_data=i + "del_rem")
                    key_edit_desc = types.InlineKeyboardButton(text='Править описание', callback_data=i + "ed_desc_rem")
                    key_edit_time = types.InlineKeyboardButton(text='Править время', callback_data=i + "ed_time_rem")
                    keyboard.add(key_delete_rem, key_edit_desc, key_edit_time)
                    to_print = '''📌 "{}"
Время, когда напомнить: {}'''.format(i, reminders[time][1])
                    bot.send_message(message.from_user.id, text=to_print, reply_markup=keyboard)


def qstn(message, f=None):
    if len(look_tasks) == 0:
        bot.send_message(message.from_user.id, "Список дел пуст\nВы можете отдыхать или добавить новое дело :)")
    if message.text == 'Не сортировать':
        for i in look_tasks.keys():
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            key_done_task = types.InlineKeyboardButton(text='Сделано', callback_data=i + 'done')
            key_delete_tasks = types.InlineKeyboardButton(text='Удалить', callback_data=i + 'delete')
            key_show_desc = types.InlineKeyboardButton(text='Посмотреть описание', callback_data=i + 'desc')
            keyboard.add(key_done_task, key_delete_tasks, key_show_desc)
            key_edit_desc = types.InlineKeyboardButton(text='Править описание', callback_data=i + 'edit_desc')
            key_edit_dl = types.InlineKeyboardButton(text='Править дедлайн', callback_data=i + 'dl')
            key_edit_imp = types.InlineKeyboardButton(text='Править важность', callback_data=i + 'imp')
            keyboard.row(key_edit_desc, key_edit_dl, key_edit_imp)
            global deadlines_to_print
            to_print = '''📌 "{}"
Описание: {}
Дедлайн: {}
Важность: {}'''.format(i, look_tasks[i][0], deadlines_to_print[i], look_tasks[i][2])
            bot.send_message(message.from_user.id, text=to_print, reply_markup=keyboard)
    elif message.text == 'Сортировать дела':
        keyboard3 = types.ReplyKeyboardMarkup(True, True)
        keyboard3.row('По дедлайну', 'По важности')
        sort_type = bot.send_message(message.from_user.id, "Как сортировать?", reply_markup=keyboard3)
        bot.register_next_step_handler(sort_type, sort_things)


def sort_things(message, f=None):
    if message.text == 'По дедлайну':
        bot.send_message(message.from_user.id, "Пока не умею сортировать по дедлайну :(")
    elif message.text == 'По важности':
        new_list = []
        for key in look_tasks.keys():
            imp = int(look_tasks[key][2])
            task_desc = (key, imp)
            new_list.append(task_desc)
        for i in sorted(new_list, key=lambda x: x[1],
                        reverse=True):  # когда разберёмся с дедлайнами, будет многоуровневая: сначала по важности, потом по дл
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            key_done_task = types.InlineKeyboardButton(text='Сделано', callback_data=i[0] + 'done')
            key_delete_tasks = types.InlineKeyboardButton(text='Удалить', callback_data=i[0] + 'delete')
            key_show_desc = types.InlineKeyboardButton(text='Посмотреть описание', callback_data=i[0] + 'desc')
            keyboard.add(key_done_task, key_delete_tasks, key_show_desc)
            key_edit_desc = types.InlineKeyboardButton(text='Править описание', callback_data=i[0] + 'edit_desc')
            key_edit_dl = types.InlineKeyboardButton(text='Править дедлайн', callback_data=i[0] + 'dl')
            key_edit_imp = types.InlineKeyboardButton(text='Править важность', callback_data=i[0] + 'imp')
            keyboard.row(key_edit_desc, key_edit_dl, key_edit_imp)
            bot.send_message(message.from_user.id, text=i[0], reply_markup=keyboard)


def get_new(message):
    global new
    new = message.text
    look_tasks[new] = []
    data = bot.send_message(message.from_user.id, 'Введите описание вашего дела')
    bot.register_next_step_handler(data, add_data)


def add_data(message):
    data = message.text
    global data_list
    data_list.append(data)
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('Без дедлайна')
    data2 = bot.send_message(message.from_user.id, '''Укажите дедлайн. Если не хотите, нажмите кнопку "Без дедлайна" ниже.
Указывайте дедлайн в формате *дд.мм.гггг чч:мм*.
Вы можете не указывать время, а также год - тогда по умолчанию будет ставиться текущий год, а время - 23:59.
То есть, если Вы укажете 25.05, то программа будет считать дедлайном 25.05.{} 23.59.'''.format(curr_day.year), reply_markup=keyboard)
    bot.register_next_step_handler(data2, add_data2)


def add_data2(message):
    date_s = message.text
    global data_list
    global new
    global deadlines_to_print
    if date_s == "Без дедлайна":
        data_list.append(None) #не знаю что сюда положить
        deadlines_to_print[new] = "Нет"
    else:
        is_year = 0
        for i in date_s:
            if i == ".":
                is_year += 1
        thedate = 0
        if ":" in date_s:
            if is_year == 2:
                thedate = datetime.datetime.strptime(date_s, '%d.%m.%Y %H:%S')
            else:
                thedate = datetime.datetime.strptime(date_s, '%d.%m %H:%S')
                thedate = thedate.replace(year=curr_day.year)
        else:
            if is_year == 2:
                thedate = datetime.datetime.strptime(date_s, '%d.%m.%Y')
                thedate = thedate.replace(hour=23, minute=59)
            else:
                thedate = datetime.datetime.strptime(date_s, '%d.%m')
                thedate = thedate.replace(year=curr_day.year)
                thedate = thedate.replace(hour=23, minute=59)
        data_list.append(thedate)
        deadlines_to_print[new] = "{}.{}.{} {}:{}".format(thedate.day, thedate.month, thedate.year, thedate.hour, thedate.minute)
    keyboard = types.ReplyKeyboardRemove(True)
    data3 = bot.send_message(message.from_user.id, 'Укажите важность по шкале 1-5, где 5 - наиболее важное дело.', reply_markup=keyboard)
    bot.register_next_step_handler(data3, add_data3)


def add_data3(message):
    data = message.text
    global data_list
    data_list.append(data)
    global new
    look_tasks.update({new: data_list})
    # я пока делала словарь "задача": [описание, дедлайн, важность]
    # но несложно сделать и словарь "задача": {"описание": данные, "дедлайн": данные, "важность": данные}
    # просто не знаю, как лучше
    data_list = []
    curr_task = {}
    bot.send_message(message.from_user.id, 'Добавил :)')


def desc_edit(message):
    global look_tasks
    global thing
    help_list = look_tasks[thing]
    help_list.pop(0)
    help_list.insert(0, message.text)
    look_tasks[thing] = help_list
    thing = ''
    bot.send_message(message.from_user.id, "Описание отредактировано!")


def dl_edit(message):
    global look_tasks
    global thing2
    help_list = look_tasks[thing2]
    help_list.pop(1)
    help_list.insert(1, message.text)
    look_tasks[thing2] = help_list
    thing2 = ''
    bot.send_message(message.from_user.id, "Дедлайн отредактирован!")


def imp_edit(message):
    global look_tasks
    global thing3
    help_list = look_tasks[thing3]
    help_list.pop(2)
    help_list.insert(2, message.text)
    look_tasks[thing3] = help_list
    thing3 = ''
    bot.send_message(message.from_user.id, "Важность отредактирована!")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    for i in list(look_tasks):
        if call.data == i + 'done':
            del look_tasks[i]
            bot.send_message(call.message.chat.id, 'Вы молодец! Поздравляю с успешно выполненным делом :)')
            bot.send_photo(call.message.chat.id, random.choice(image_list))
        elif call.data == i + 'delete':
            del look_tasks[i]
            bot.send_message(call.message.chat.id, 'Дело удалено')
        elif call.data == i + 'desc':
            desc = "Описание: "
            desc += look_tasks[i][0] + "\n" + "Дедлайн: " + look_tasks[i][1] + "\n" + 'Важность: ' + look_tasks[i][2]
            bot.send_message(call.message.chat.id, desc)
        elif call.data == i + 'edit_desc':
            global thing
            thing = i
            new_desc = bot.send_message(call.message.chat.id, 'Введите новое описание')
            bot.register_next_step_handler(new_desc, desc_edit)
        elif call.data == i + 'dl':
            global thing2
            thing2 = i
            new_dl = bot.send_message(call.message.chat.id, 'Введите новый дедлайн')
            bot.register_next_step_handler(new_dl, dl_edit)
        elif call.data == i + 'imp':
            global thing3
            thing3 = i
            new_imp = bot.send_message(call.message.chat.id, 'Введите новое значение важности (0-10)')
            bot.register_next_step_handler(new_imp, imp_edit)
    for time in reminders_time_list:
        for i in range(len(reminders[time][0])):
            global old_desc_rem_ind
            global old_time_rem
            old_time_rem = time
            old_desc_rem_ind = i
            if call.data == reminders[time][0][i] + "del_rem":
                reminders[time][0].remove(reminders[time][0][i])
                if len(reminders[time][0]) == 0:
                    del reminders[time]
                    reminders_time_list.remove(time)
                bot.send_message(call.message.chat.id, 'Напоминание удалено')
            elif call.data == reminders[time][0][i] + "ed_desc_rem":
                new_desc_rem = bot.send_message(call.message.chat.id, 'Введите новое описание того, о чем мне нужно напомнить')
                bot.register_next_step_handler(new_desc_rem, desc_rem_edit)
            elif call.data == reminders[time][0][i] + "ed_time_rem":
                new_time_rem = bot.send_message(call.message.chat.id,'Введите новое время, когда хотите получить напоминание')
                bot.register_next_step_handler(new_time_rem, time_rem_edit)


def desc_rem_edit(message):
    global reminders
    reminders[old_time_rem][0][old_desc_rem_ind] = message.text
    bot.send_message(message.from_user.id, "Напоминание отредактировано!")

def time_rem_edit(message):
    global reminders
    global reminders_time_list
    new_time = message.text
    is_year = 0
    for i in new_time:
        if i == ".":
            is_year += 1
    thedate = 0
    if is_year == 2:
        thedate = datetime.datetime.strptime(new_time, '%d.%m.%Y %H:%M')
    else:
        thedate = datetime.datetime.strptime(new_time, '%d.%m %H:%M')
        thedate = thedate.replace(year=curr_day.year)
    reminders_time_list.append(thedate)
    reminders[thedate] = reminders[old_time_rem]
    reminders[thedate][1] = "{}.{}.{} {}:{}".format(thedate.day, thedate.month, thedate.year, thedate.hour, thedate.minute)
    reminders_time_list.remove(old_time_rem)
    del reminders[old_time_rem]
    bot.send_message(message.from_user.id, "Время напоминания отредактировано!")

def add_reminder(message):
    global curr_reminder
    curr_reminder = message.text
    time_to_remind = bot.send_message(message.from_user.id, '''Когда Вы хотите, чтобы я Вам об этом напомнил?
Присылайте ответ в формате *дд.мм.гггг чч:мм*
Год можно не указывать, тогда автоматически поставится текущий.''')
    bot.register_next_step_handler(time_to_remind, reminder_added)

def reminder_added(message):
    global reminders
    time_to_remind = message.text
    is_year = 0
    for i in time_to_remind:
        if i == ".":
            is_year += 1
    thedate = 0
    if is_year == 2:
        thedate = datetime.datetime.strptime(time_to_remind, '%d.%m.%Y %H:%M')
    else:
        thedate = datetime.datetime.strptime(time_to_remind, '%d.%m %H:%M')
        thedate = thedate.replace(year=curr_day.year)
    if reminders.get(thedate, None) is None:
        reminders[thedate] = ([], "{}.{}.{} {}:{}".format(thedate.day, thedate.month, thedate.year, thedate.hour, thedate.minute))
    reminders[thedate][0].append(curr_reminder)
    reminders_time_list.append(thedate)
    reminders_time_list.sort()
    bot.send_message(message.from_user.id, 'Добавлено! :)')


bot.polling(none_stop=True)
