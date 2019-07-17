import os

from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import pdf2image
TEMP_DIR = './temp'

SEND_FILE, SELECT_SIZE, SELECT_PAGE = range(3)


def convert(bot, update):
    pass


def receive_file(bot, update):
    file = bot.get_file(update.message.document.file_id)
    file.download(os.path.join(TEMP_DIR, '{}.pdf'.format(update.message.from_user.id)))


def cancel(update, context):
    update.message.reply_text('Operation cancelled', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    token = os.environ.get('BOT_TOKEN')
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    updater = Updater(token)
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('convert', convert)],
        states={
            SEND_FILE: MessageHandler(Filters.document.pdf, receive_file),
            SELECT_SIZE: [],
            SELECT_PAGE: []
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
