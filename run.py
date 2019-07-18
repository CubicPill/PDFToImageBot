import os

import pdf2image
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

TEMP_DIR = './temp'

SEND_FILE, SELECT_SIZE, SELECT_PAGE, SELECT_FORMAT = range(4)


def convert(bot, update):
    update.message.reply_text('Send the PDF file to be converted')


def cleanup(user_id):
    pass


def receive_file(bot, update):
    file = bot.get_file(update.message.document.file_id)
    file.download(os.path.join(TEMP_DIR, '{}.pdf'.format(update.message.from_user.id)))
    return SELECT_SIZE


def select_dpi(bot, update):
    return SELECT_PAGE


def select_size(bot, update):
    return SELECT_PAGE


def select_page(bot, update):
    return SELECT_FORMAT


def select_format(bot, update):
    do_convert(update.message.from_user.id)
    cleanup(update.message.from_user.id)
    return ConversationHandler.END


def do_convert(user_id, size=None, dpi=None):
    if not size and not dpi:
        return False
    pdf2image.convert_from_path(os.path.join(TEMP_DIR, '{}.pdf'.format(user_id)))
    return True


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
            SELECT_SIZE: [MessageHandler(Filters.text, select_dpi), MessageHandler(Filters.text, select_size)],
            SELECT_PAGE: [MessageHandler(Filters.text, select_page)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
