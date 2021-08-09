from config import BOT_TOKEN, PAYMENT_TOKEN
from modules import *

order = {}
order_num = 0
bot = telebot.TeleBot(BOT_TOKEN)


# Функции бота
def start(update, context):
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=main_menu_message(),
        reply_markup=main_menu_keyboard())


def first_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=choose_drink_menu_message(),
        reply_markup=first_menu_keyboard())


def second_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=choose_drink_menu_message(),
        reply_markup=second_menu_keyboard())


# Функция оплаты заказа
def pay(update: Update, context: CallbackContext):
    global order_num
    query = update.callback_query
    coffee_list = str(query.data).split(' ')
    chat_id = query.message.chat_id
    order_num = order_num + 1
    title = 'Ваш заказ № {} в "{}"'.format(order_num, coffee_list[0])
    description = "Нажмите на кнопку для оплаты вашего {}:".format(coffee_list[1])
    payload = "Byu-a-Coffee"
    provider_token = PAYMENT_TOKEN
    currency = "RUB"
    price = int(coffee_list[2])
    # Сумма для Юкассы 100рублей = "10000" поэтому умножаем на 100
    prices = [LabeledPrice("Цена", price * 100)]
    # отправляем счет клиенту в телеграм
    context.bot.send_invoice(chat_id, title, description, payload, provider_token, currency, prices)
    # Составляем лог заказа
    global order
    date = datetime.today()
    order['order_number'] = order_num
    order['date'] = date.strftime("%b %d %Y %H:%M:%S")
    order['id'] = chat_id
    order['firstname'] = query.message.chat.first_name
    order['lastname'] = query.message.chat.last_name
    order['username'] = query.message.chat.username
    order['cafe'] = coffee_list[0]
    order['coffee'] = coffee_list[1]
    order['price'] = coffee_list[2]


# Функция отправки информации о заказе исполнителю
def send_order_executer():
    # Открываем файл с исполнителями(Кофейнями)
    file = open('executors.json', 'r')
    content = json.load(file)
    # по циклу перебираем кофейни
    for k, v in content.items():
        for i in range(len(v)):
            # Если находим нужное название кофейни отправляем сообщение с заказом
            if v[i]['cafe'] == order['cafe']:
                bot.send_message(v[i]['id'], 'Заказ № {}: {}. Сумма: {} рублей. Получатель: {}'
                                 .format(order['order_number'],
                                         order['coffee'],
                                         order['price'],
                                         order['firstname']))


# Функция проверки платежа
def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    # Проверка платежа от бота
    if query.invoice_payload != "Byu-a-Coffee":
        # Если платеж не содержит нужной информации в Payload выводим ошибку
        query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        query.answer(ok=True)


# После проведения платежа выводим сообщение об успехе и фиксируем данные в файл
def successful_payment_callback(update: Update, context: CallbackContext):
    # При успешной оплате записываем заказ в файл
    try:
        with open('orders.txt', 'a') as file:
            global order
            file.write(str(order) + '\n')
            file.close()
    except FileNotFoundError:
        pass
    except FileExistsError:
        pass
    # Сообщщение об успехе клиенту!
    update.message.reply_text("Ваш заказ № {}. Оплата прошла успешно!\n"
                              "Спасибо, что выбрали наш сервис!".format(order_num))
    # Отправляем заказ в кофейню
    send_order_executer()


# Клавиатура
# Главное меню
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('SURFCoffee', callback_data='1')],
                [InlineKeyboardButton('Кооператив Черный', callback_data='2')]]
    return InlineKeyboardMarkup(keyboard)


# Меню при переходе в SURFCoffee
def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Латте - 250₽', callback_data='SURFCoffee Латте 250')],
                [InlineKeyboardButton('Капучино - 200₽', callback_data='SURFCoffee Капучино 200')],
                [InlineKeyboardButton('РАФ - 300₽', callback_data='SURFCoffee РАФ 300')],
                [InlineKeyboardButton('Флэт-Уайт - 150₽', callback_data='SURFCoffee Флэт-Уайт 150')],
                [InlineKeyboardButton('В главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


# Меню при переходе в Кооператив Черный
def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Американо - 150₽', callback_data='Кооператив_Черный Американо 150')],
                [InlineKeyboardButton('Эспрессо - 150₽', callback_data='Кооператив_Черный Эспрессо 150')],
                [InlineKeyboardButton('Капучино - 200₽', callback_data='Кооператив_Черный Капучино 200')],
                [InlineKeyboardButton('Малиновый РАФ - 350₽', callback_data='Кооператив_Черный Малиновый_РАФ 350')],
                [InlineKeyboardButton('Латте - 200₽', callback_data='Кооператив_Черный Латте 200')],
                [InlineKeyboardButton('В главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


# Сообщения при выводе меню
def main_menu_message():
    return 'Выберите кофейню:'


def choose_drink_menu_message():
    return 'Выберите напиток:'


# Действия
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    # Главное меню и выбор кофе
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='2'))

    # Вызов оплаты
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="SURFCoffee Латте 250"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="SURFCoffee Капучино 200"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="SURFCoffee РАФ 300"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="SURFCoffee Флэт-Уайт 150"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="Кооператив_Черный Американо 150"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="Кооператив_Черный Эспрессо 150"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="Кооператив_Черный Капучино 200"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="Кооператив_Черный Малиновый_РАФ 350"))
    updater.dispatcher.add_handler(CallbackQueryHandler(pay, pattern="Кооператив_Черный Латте 200"))

    # Вызов проверки платежа
    updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    # Вызов сообщения об успешной оплате
    updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()


if __name__ == '__main__':
    main()
