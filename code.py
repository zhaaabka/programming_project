import telebot
from telebot import types
import ast

TOKEN = '1770257533:AAEhX110czS9QLcUyupCQRxu_aNlhKb1s_g'

bot = telebot.TeleBot(TOKEN)

new = ''
look_tasks = {}
data_list = [] #можно и словарь типа {"описание": данные, "дедлайн": данные, "важность": данные} сделать, но нужно ли?

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
            bot.send_message(message.from_user.id, "Пока не умею сортировать по важности :(") 
            
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
        elif call.data == i + 'delete':
            del look_tasks[i];
            bot.send_message(call.message.chat.id, 'Дело удалено!');
        elif call.data == i + 'desc':
            desc = "Описание: "
            desc += look_tasks[i][0] + "\n" + "Дедлайн: " + look_tasks[i][1] + "\n" + 'Важность: ' + look_tasks[i][2]
            bot.send_message(call.message.chat.id, desc)

bot.polling(none_stop=True)
