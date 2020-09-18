import logging
import telebot
from apteka import HomeBot
import settings

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
# apihelper.proxy = config.proxy
bot = telebot.TeleBot(settings.TOKEN)
df = {}


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Нажав по этой кнопке вы можете написать разработчику чат бота', url='t.me/RKamynin'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) Для получения списка доступных действий для введите /action.\n' +
        '2) Для получения справки введите /help.\n',
        reply_markup=keyboard
    )


@bot.message_handler(commands=["action"])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("Самые низкие цены на лекарства", callback_data="get-DRUGS"),
    )
    bot.send_message(
        message.chat.id, "Выберите интересующее вас действие:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text and message.text.startswith("drugs"))
def all_commands(message):
    drugs = message.text.replace('drugs ', '').split(', ')
    bot.send_message(message.chat.id, 'я начал поиск для вас, это может занять пару минут')
    print(drugs)
    print(message.chat.id)
    print(type(message.chat.id))
    order = HomeBot(drugs)
    df[message.chat.id] = order
    order.message_minprice(message.chat.id)


@bot.message_handler(func=lambda message: message.text and message.text.startswith("/recount_"))
def recount(message):
    mess = message.text.replace('/recount_', '')
    print(mess)
    order = df[message.chat.id]
    order.change(int(mess))
    print(order.prices_df)
    order.message_minprice(message.chat.id)


@bot.message_handler(commands=["price_list"])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_message(
        message.chat.id, "полный прайс лист:",
        reply_markup=keyboard
    )
    order = df[message.chat.id]
    order.message_pricelst(message.chat.id)


@bot.message_handler(func=lambda message: message.text and message.text.startswith("/TOP3_"))
def top3(message):
    mess = message.text.replace('/TOP3_', '')
    order = df[message.chat.id]
    order.message_top3(index=int(mess), chat_id=message.chat.id)


@bot.message_handler(func=lambda message: message.text and message.text.startswith("/order_"))
def make_order(message):
    mess = message.text.replace('/order_', '')
    order = df[message.chat.id]
    order.ordering(int(mess))
    bot.send_message(message.chat.id, 'товар добавлен в корзину')


bot.polling(none_stop=True)
