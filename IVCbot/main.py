from telegram.ext import Updater, MessageHandler, Filters
from config import *
from cam_control.screenshot import *


def message_handler(bot, update):
    user = update.effective_user
    message = update.effective_message.text
    if user.id not in legalUsers:
        update.message.reply_text('Я с такими, как ты, не общаюсь. '
                                  'Твой id: {}'.format(user.id))
        return

    elif message == 'Сделай скрин':
        bot.send_photo(user.id, open(get_screen(cam1['name'], cam1['ip']), 'rb'))
        bot.send_photo(user.id, open(get_screen(cam2['name'], cam2['ip']), 'rb'))
        print('Сделал скрины')

    elif message == 'Запись идет?' or message == 'Запись идёт?':
        update.message.reply_text('Камера 1: ' + str(check_record(cam1['name'], pathVideo)))
        update.message.reply_text('Камера 2: ' + str(check_record(cam2['name'], pathVideo)))
        print('Проверил запись')



def main():
    bot = Updater(
        TG_TOKEN,
        base_url='https://telegg.ru/orig/bot'
    )

    handler = MessageHandler(Filters.all, message_handler)
    bot.dispatcher.add_handler(handler)
    bot.start_polling()

    bot.idle()


if __name__ == '__main__':
    main()
