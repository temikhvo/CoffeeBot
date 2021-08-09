# CoffeeBot
Бот для заказа кофе

########################## СПИСОК ФАЙЛОВ ##################################

 1. Bot.py - главный файл бота
  
 2. add_executor.py - добавление кофейнь
  
 3. config.py - конфигурационный файл с токенами
  
 4. modules.py - подключение модулей
  
 5. executors.json - данные кофейнь
  
 6. orders.txt - лог заказов
  

########################## ОПИСАНИЕ ФУНКЦИИ ##################################
  
  main(): Функция запуска всех функций бота
  
  start(update, context): Вывод стартовой клавиатуры с выбором кофейни
  
  main_menu(update, context): Вывод клавиатуры с выбором кофейни
  
  first_menu(update, context): Вывод клавиатуры для выбора напитков из кофейни № 1
  
  second_menu(update, context): Вывод клавиатуры для выбора напитков из кофейни № 2
  
  pay(update: Update, context: CallbackContext): Вывод оплата и подготовка информации для записи в лог заказов(order.txt)
  
  precheckout_callback(update: Update, context: CallbackContext): Проверка оплаты
  
  successful_payment_callback(update: Update, context: CallbackContext): Отправка покупателю сообщения об успешной оплате и запись в лог заказов(order.txt)
  
  send_order_executer(): Отправка заказа в кофейню
  
################################## ФУНКЦИОНАЛЬНАЯ КЛАВИАТУРА ##################################

  main_menu_keyboard(): Клавиатура выбора кофейни
  
  first_menu_keyboard(): Клавиатура первой кофейни
  
  second_menu_keyboard(): Клавиатура второй кофейни
  
  main_menu_message(): Сообщение главного меню
  
  choose_drink_menu_message(): Сообщение при выборе напитка
