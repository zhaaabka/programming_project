import telebot
from telebot import types
import ast

TOKEN = '1770257533:AAEhX110czS9QLcUyupCQRxu_aNlhKb1s_g'

bot = telebot.TeleBot(TOKEN)

new = ''
look_tasks = {}

@bot.message_handler(commands=['start', 'help'])
def what_to_do(message):
      keyboard = types.ReplyKeyboardMarkup(True, True);
      keyboard.row('Записать новое дело', 'Посмотреть записанные дела');
      bot.send_message(message.from_user.id, 'Что Вы хотите сделать?', reply_markup=keyboard)

@bot.message_handler(content_types = ['text'])
def new(message, f=None):
    if message.text == 'Посмотреть записанные дела':
        for i in look_tasks.keys():
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            key_done_task = types.InlineKeyboardButton(text='Сделано', callback_data= i + 'done');
            key_delete_tasks= types.InlineKeyboardButton(text='Удалить', callback_data= i + 'delete');
            keyboard.add(key_done_task, key_delete_tasks);
            bot.send_message(message.from_user.id, text=i, reply_markup=keyboard)
    elif message.text == 'Записать новое дело':
        msg = bot.send_message(message.from_user.id, 'Напишите:');
        bot.register_next_step_handler(msg, get_new)

def get_new(message):
    new = message.text;
    look_tasks.update({new: ['data', 'deadline', 'importance']});
    bot.send_message(message.from_user.id, 'Добавил :)');

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    for i in list(look_tasks):
        if call.data == i + 'done':
            del look_tasks[i];
            bot.send_message(call.message.chat.id, 'Поздравляю! :)');

bot.polling(none_stop=True)
