import telebot #импортируем необходимую библиотеку и созданные файлы
from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN) #создаем бота

@bot.message_handler(commands=['start', 'help']) #обработка ботом комманд /start, /help и вывод инструкции
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюты перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values']) #обработка ботом комманды /values, которая выводит список доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text']) #обрабатывает сообщение пользователя и конвертирует выбранные валюты
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values
        total = ValueConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
