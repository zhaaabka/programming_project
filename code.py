import telebot
from telebot import types
import ast
import random #чтобы отправлять случайную картинку из списка

TOKEN = '1768268284:AAEmnrx9HHxjZgd6eDmmjgfKptnPAsHY6e0'

bot = telebot.TeleBot(TOKEN)

new = ''
look_tasks = {}
data_list = [] #можно и словарь типа {"описание": данные, "дедлайн": данные, "важность": данные} сделать, но нужно ли?
image_list = ['https://images.unsplash.com/photo-1511044568932-338cba0ad803?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80', 'https://images.unsplash.com/photo-1494256997604-768d1f608cac?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1101&q=80']
#пока в списке две произвольных картинки с котами
#я думаю, стоит загрузить все нужные нам картинки в отдельную папку на гитхабе + давать ссылки туда, чтобы точно ничего не сломалось

@bot.message_handler(commands=['start', 'help'])
def what_to_do(message):
      keyboard = types.ReplyKeyboardMarkup(True, True);
      keyboard.row('Записать новое дело', 'Посмотреть записанные дела');
      bot.send_message(message.from_user.id, 'Что Вы хотите сделать?', reply_markup=keyboard)

@bot.message_handler(content_types = ['text'])
def new(message, f=None):
    if message.text == 'Посмотреть записанные дела':
      keyboard2 = types.ReplyKeyboardMarkup(True, True)
      keyboard2.row('Сортировать дела', 'Не сортировать')
      sort = bot.send_message(message.from_user.id, "Сортировать дела?", reply_markup=keyboard2)
      bot.register_next_step_handler(sort, qstn)

    elif message.text == 'Записать новое дело':
        msg = bot.send_message(message.from_user.id, 'Напишите, как называется ваше дело');
        bot.register_next_step_handler(msg, get_new)

def qstn(message, f=None):
    if message.text == 'Не сортировать':
        for i in look_tasks.keys():
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            key_done_task = types.InlineKeyboardButton(text='Сделано', callback_data= i + 'done');
            key_delete_tasks= types.InlineKeyboardButton(text='Удалить', callback_data= i + 'delete');
            key_show_desc = types.InlineKeyboardButton(text='Посмотреть описание', callback_data = i + 'desc')
            keyboard.add(key_done_task, key_delete_tasks, key_show_desc);
            bot.send_message(message.from_user.id, text=i, reply_markup=keyboard)
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
        for i in sorted(new_list, key=lambda x: x[1], reverse=True): #когда разберёмся с дедлайнами, будет многоуровневая: сначала по важности, потом по дл
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            key_done_task = types.InlineKeyboardButton(text='Сделано', callback_data= i[0] + 'done');
            key_delete_tasks= types.InlineKeyboardButton(text='Удалить', callback_data= i[0] + 'delete');
            key_show_desc = types.InlineKeyboardButton(text='Посмотреть описание', callback_data = i[0] + 'desc')
            keyboard.add(key_done_task, key_delete_tasks, key_show_desc);
            bot.send_message(message.from_user.id, text=i[0], reply_markup=keyboard)
            
def get_new(message):
    global new  
    new = message.text;
    look_tasks[new] = []
    data = bot.send_message(message.from_user.id, 'Введите описание вашего дела')
    bot.register_next_step_handler(data, add_data)

def add_data(message):
      data = message.text
      global data_list
      data_list.append(data)
      data2 = bot.send_message(message.from_user.id, 'Укажите дедлайн')
      bot.register_next_step_handler(data2, add_data2)

def add_data2(message):
      data = message.text
      global data_list
      data_list.append(data)
      data3 = bot.send_message(message.from_user.id, 'Укажите важность по шкале 0-10') #или 1-4?
      bot.register_next_step_handler(data3, add_data3)

def add_data3(message):
      data = message.text
      global data_list
      data_list.append(data)
      global new
      look_tasks.update({new: data_list})
      #я пока делала словарь "задача": [описание, дедлайн, важность]
      #но несложно сделать и словарь "задача": {"описание": данные, "дедлайн": данные, "важность": данные}
      #просто не знаю, как лучше
      data_list = []
      bot.send_message(message.from_user.id, 'Добавил :)')

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    for i in list(look_tasks):
        if call.data == i + 'done':
            del look_tasks[i];
            bot.send_message(call.message.chat.id, 'Поздравляю! :)');
            bot.send_photo(call.message.chat.id, random.choice(image_list)) 
        elif call.data == i + 'delete':
            del look_tasks[i];
            bot.send_message(call.message.chat.id, 'Дело удалено!');
        elif call.data == i + 'desc':
            desc = "Описание: "
            desc += look_tasks[i][0] + "\n" + "Дедлайн: " + look_tasks[i][1] + "\n" + 'Важность: ' + look_tasks[i][2]
            bot.send_message(call.message.chat.id, desc)

bot.polling(none_stop=True)
