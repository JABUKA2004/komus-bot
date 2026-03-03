# bot.py

# 1. Подключаем необходимые библиотеки
import telebot
import re

# 2. Здесь нужно вставить ТОКЕН, который ты получил от BotFather
TOKEN = "8762922219:AAFIKLz49TTg8a_lA06QxXFjGwec57dYCaM"

# 3. Вставь сюда свой Telegram ID, чтобы бот пересылал заказы тебе
# Как узнать свой ID: напиши в Telegram @userinfobot, нажми Start, и он пришлет твой ID.
ADMIN_CHAT_ID = "899080613"

# 4. Создаем бота
bot = telebot.TeleBot(TOKEN)

# 5. Текст инструкции, которую увидит пользователь
INSTRUCTION_TEXT = """
📝 **Инструкция по составлению заказа (Интернет-магазин Комус)**

Для того чтобы сделать заказ, отправь мне сообщение в следующем формате:

`Артикул товара - Количество`

**Пример:**
123456 - 2
789012 - 5

Ты можешь отправить несколько позиций сразу, каждую с новой строки.

После того как отправишь список, я перешлю его менеджеру для оформления.
"""

# 6. Команда /start
@bot.message_handler(commands=['start'])
def send_instruction(message):
    # Отправляем пользователю инструкцию
    bot.send_message(message.chat.id, INSTRUCTION_TEXT, parse_mode='Markdown')
    # Можно добавить небольшое подтверждение
    bot.send_message(message.chat.id, "✅ Отправляй свой список в формате: Артикул - Количество")

# 7. Обработка текстовых сообщений (кроме команд)
@bot.message_handler(func=lambda message: True)
def handle_order(message):
    # Проверяем, не команда ли это (на всякий случай)
    if message.text.startswith('/'):
        return

    # Сообщаем пользователю, что заказ принят
    bot.reply_to(message, "✅ Спасибо! Ваш заказ принят и передан менеджеру.")

    # Формируем сообщение для администратора (меня)
    user_info = f"Заказ от пользователя: @{message.from_user.username} (ID: {message.from_user.id})\n\n"
    order_text = f"Текст заказа:\n{message.text}"

    admin_message = user_info + order_text

    # Отправляем заказ администратору
    bot.send_message(ADMIN_CHAT_ID, admin_message)

    # 8. (НЕОБЯЗАТЕЛЬНО, НО ПОЛЕЗНО) Простейшая проверка формата
    lines = message.text.strip().split('\n')
    has_error = False
    error_message = "⚠️ Проверь формат следующих строк (должно быть 'Артикул - Количество'):\n"

    for i, line in enumerate(lines):
        line = line.strip()
        if line: # если строка не пустая
            # Ищем шаблон "цифры - цифры"
            if not re.match(r'^\d+\s*-\s*\d+$', line):
                error_message += f"Строка {i+1}: {line}\n"
                has_error = True

    if has_error:
        # Если нашли ошибки в формате, отправляем предупреждение пользователю
        bot.send_message(message.chat.id, error_message)
    # else:
        # Если хочешь подтверждать, что формат верный, можно раскомментировать:
        # bot.send_message(message.chat.id, "✅ Формат всех строк верный.")

# 9. Запускаем бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
