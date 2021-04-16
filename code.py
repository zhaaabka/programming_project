import telebot
from telebot import types

TOKEN = '1770257533:AAEhX110czS9QLcUyupCQRxu_aNlhKb1s_g'

bot = telebot.TeleBot(TOKEN)

new = ''
look_tasks = []

@bot.message_handler(commands=['start', 'help'])
def what_to_do(message):
      keyboard = types.InlineKeyboardMarkup();
      key_new_task = types.InlineKeyboardButton(text='Записать новое дело', callback_data='new');
      keyboard.add(key_new_task);
      key_look_tasks= types.InlineKeyboardButton(text='Посмотреть записанные дела', callback_data='look');
      keyboard.add(key_look_tasks);
      question = 'Что Вы хотите сделать?';
      bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'new':
        bot.send_message(call.message.chat.id, 'Напишите:');
        
        @bot.message_handler(content_types=['text'])
        def get_new(message):
            global new;
            new = message.text;
            global look_tasks;
            look_tasks.append(new);
            bot.send_message(message.from_user.id, 'Добавил :)');

    elif call.data == 'look':
        bot.send_message(call.message.chat.id, look_tasks);

bot.polling(none_stop=True)
