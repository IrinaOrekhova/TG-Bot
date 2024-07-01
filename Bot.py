import telebot
from config import keys, TOKEN
from extensions import ConvertionException, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', ])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты>\<в какую валюту перевести>\<количество переводимой валюты> \''
            '\nЧтобы увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(content_types=['photo', ])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, 'Классный мем XDD')

@bot.message_handler(content_types=['audio', 'voice', ])
def handle_audio_voice(message: telebot.types.Message):
    bot.reply_to(message, 'У тебя великолепный голос!')

@bot.message_handler(content_types=['video', ])
def handle_video(message: telebot.types.Message):
    bot.reply_to(message, 'Смотрю на тебя и сердце радуется!')

@bot.message_handler(content_types=['document', 'location', 'contact', 'sticker', ])
def handle_document_location_contact_sticer(message: telebot.types.Message):
    bot.reply_to(message, 'Прости, я эту вашу наскальную живопись не понимаю.')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = APIException.get_prise(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e} ")
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)