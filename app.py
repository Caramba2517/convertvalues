from keys import *
from telebot import *
from config import TOKEN
from convertator import ConvertatorFull, ConvertatorRate, ConversionExc

bot = telebot.TeleBot(TOKEN)

ans1 = []
ans2 = []


@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, {message.from_user.first_name}\n\n" \
        f"Я бот, умеющий показывать курсы валют и конвертировать валюты:\n" \
        f"\n Список команд:\n" \
        f"/doit - мой основной функционал" \
        f"\n/values - список доступных валют\n" \
        f"/help - краткая информация обо мне"
    bot.send_message(message.chat.id, mess, reply_markup=DelKeyboard)


@bot.message_handler(commands=['help'])
def help(message):
    mess = f"Я бот, умеющий показывать курсы валют и конвертировать валюты:\n\n" \
           f"Обрати внимание, что сумму в валюте нужно указывать без запятых (можно использовать точку)\n" \
           f"(Пример: 1000.5)\n\n" \
           f"Список команд:\n" \
           f"/doit - мой основной функционал" \
           f"\n/values - список доступных валют\n" \
           f"\n\nTelegram Bot for convertation v0.1 by @Caramba"
    bot.send_message(message.chat.id, mess, reply_markup=DelKeyboard)


@bot.message_handler(commands=['values'])
def values(message):
    mess = f"Список доступных валют:\n" \
           f"\n{coin1} - могу показать курс в рублях и конвертировать в другие доступные валюты\n" \
           f"{coin2} - могу показать курс в рублях и конвертировать в другие доступные валюты\n" \
           f"{coin3} - могу показать в курс в рублях и конвертировать в другие доступные валюты\n" \
           f"\nОбратите внимание, что напрямую 🇷🇺 рубли конвертировать я не умею," \
           f" но могу конвертировать другие валюты в рубли."
    bot.send_message(message.chat.id, mess, reply_markup=DelKeyboard)


@bot.message_handler(commands=['doit'])
def doit(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(startbut1)
    item2 = types.KeyboardButton(startbut2)
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите, что я могу для вас сделать: ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def step1(message):
    if message.text == startbut1:
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text=coin1, callback_data=coin1)
        item2 = types.InlineKeyboardButton(text=coin2, callback_data=coin2)
        item3 = types.InlineKeyboardButton(text=coin3, callback_data=coin3)
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, f'{startbut1}:', reply_markup=markup)

    elif message.text == startbut2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(coin1)
        item2 = types.KeyboardButton(coin2)
        item3 = types.KeyboardButton(coin3)
        markup.add(item1, item2, item3)
        msg = bot.send_message(message.chat.id, f'Выберите валюту для конвертации:', reply_markup=markup)
        bot.register_next_step_handler(msg, step2)
    else:
        bot.send_message(message.chat.id, f'Пожалуйста, выберите функцию.\n'
                                          'Выберите /help - чтобы узнать что я умею.', reply_markup=DelKeyboard)


def step2(message):
    ans1.append(message.text)
    if message.text == coin1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(usd1)
        item2 = types.KeyboardButton(usd2)
        item3 = types.KeyboardButton(usd3)
        markup.add(item1, item2, item3)
        msg = bot.send_message(message.chat.id, f'Выберите валюту в которую хотите конвертировать:', reply_markup=markup)
        bot.register_next_step_handler(msg, step3)

    elif message.text == coin2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(eur1)
        item2 = types.KeyboardButton(eur2)
        item3 = types.KeyboardButton(eur3)
        markup.add(item1, item2, item3)
        msg = bot.send_message(message.chat.id, f'Выберите валюту, в которую хотите конвертировать:', reply_markup=markup)
        bot.register_next_step_handler(msg, step3)

    elif message.text == coin3:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(gel1)
        item2 = types.KeyboardButton(gel2)
        item3 = types.KeyboardButton(gel3)
        markup.add(item1, item2, item3)
        msg = bot.send_message(message.chat.id, f'Выберите валюту, в которую хотите конвертировать:', reply_markup=markup)
        bot.register_next_step_handler(msg, step3)

    else:
        bot.send_message(message.chat.id, f'Пожалуйста, выберите валюту на кнопках\n'
                                          f'Выберите /doit - чтобы начать заново.', reply_markup=DelKeyboard)
        ans1.pop()


def step3(message):
    ans2.append(message.text)
    msg = bot.send_message(message.chat.id, f'Введите сумму для конвертации: ', reply_markup=DelKeyboard)
    bot.register_next_step_handler(msg, step4)


def step4(message):
    try:
        amount = message.text.replace(' ', '')
        quote = "".join(ans1)
        base = "".join(ans2)

        total = ConvertatorFull.get_price(amount, quote, base)
        text = f'{amount}{quote} 👉 {base}\n\n{total}'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(next)
        item2 = types.KeyboardButton(end)
        markup.add(item1, item2)
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)

        ans1.pop()
        ans2.pop()
    except ConversionExc as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так =(\n{e}')
        ans1.pop()
        ans2.pop()

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось выполнить команду =(\n{e}')
        ans1.pop()
        ans2.pop()
    else:
        bot.register_next_step_handler(msg, step5)


def step5(message):
    if message.text == next:
        bot.send_message(message.chat.id, f'Выберите команду для продолжения:\n\n'
                                          f'/doit - основной функционал\n'
                                          f'/values - список доступных валют\n'
                                          f'/help - краткая информация обо мне', reply_markup=DelKeyboard)
    elif message.text == end:
        bot.send_message(message.chat.id, 'Возвращайтесь, я буду скучать!', reply_markup=DelKeyboard)


@bot.callback_query_handler(func=lambda callback: callback.data)
def step_rate(callback):
    quote = callback.data
    text = ConvertatorRate.get_rate(quote)
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=f'{quote} = {text} рублей', reply_markup=None)


bot.polling(non_stop=True)
