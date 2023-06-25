import django
import os
import sys
import sqlite3
import qrcode as qrcode
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters, CallbackQueryHandler

import django
from telegram.ext import Updater, CommandHandler
from telegram.error import BadRequest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

django.setup()

from app.models import *

from app.views import get_value_from_model_using_sql


objects = ChatIds.objects.all()

START = 1



class Bot:

    def __init__(self, token):
        self.caffeName = ""
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher


    def connect_db(self):
        conn = sqlite3.connect('ChatIds.db')
        cur = conn.cursor()
        chatId = "2412532124"
        caffeName = "Test name"
        cur.execute('''CREATE TABLE IF NOT EXISTS main_chatids 
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           caffeName VARCHAR(500) NOT NULL, 
                           chatId VARCHAR(500) NOT NULL)''')
        cur.execute("INSERT INTO main_chatids (caffeName, chatId) VALUES (?, ?)", (caffeName, chatId))
        conn.commit()
        cur.close()
        conn.close()


    def createUrl(self, table_id):
        return f"localhost2r12r43134tableid={table_id}&name={self.name}"

    def start(self, update, context):
        button1 = KeyboardButton("/QRs", callback_data='set_table')
        reply_markup = ReplyKeyboardMarkup([[button1]])
        chat_id = update.message.chat_id
        message_text = "Добро пожаловать"
        context.bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
        self.connect_db()

    def button_click(self, update, context):
        query = update.callback_query
        button_clicked = query.data
        print(button_clicked)

        user = query.from_user.first_name
        deleted_message = query.message
        context.bot.send_message(chat_id=deleted_message.chat_id, text=f"{user} принял заказ! {button_clicked}")

        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                              reply_markup=None)

    def generateQRCode(self, update, context):
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text="Напишите промежуток столов для которых нужно создать QR коды "
                                                       "(например: '1 10' числа идут включительно) или же один номер "
                                                       "стола")
        return START

    def generate_qr_code(self, update, context):
        chat_id = update.message.chat_id
        input_text = update.message.text
        self.caffeName = get_value_from_model_using_sql("caffeName", chat_id, "chatId")

        # Split the input into two digits
        digits = input_text.split()

        # Cheks is it range or just one table
        if len(digits) == 1 and digits[0].isdigit():
            print("Entered first if")
            self.createQr(context, int(digits[0]), chat_id)
            return ConversationHandler.END
        # Check for correct input
        elif len(digits) != 2 or not digits[0].isdigit() or not digits[1].isdigit():
            print("Entered second if")
            context.bot.send_message(chat_id=chat_id,
                                     text="Вы неправильно ввели промежуток. Он должен выглядеть так '1 10'")
            return START

        print("Work here")
        # Convert the digits to integers
        start_digit = min(int(digits[0]), int(digits[1]))
        end_digit = max(int(digits[0]), int(digits[1]))

        # Generate and send QR codes for each item ID within the range
        for i in range(start_digit, end_digit + 1):
            self.createQr(context, i, chat_id)
        return ConversationHandler.END

    def createQr(self, context, table_id, chat_id):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"http://127.0.0.1:8000/tableId?tableId={table_id}&name={self.caffeName}")
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Save the QR code image
        image_path = f"qrcode_{table_id}.png"
        qr_image.save(image_path)

        # Send the QR code image to the user
        context.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'))
        os.remove(image_path)

    def cancel(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Command cancelled.")
        return ConversationHandler.END

    def run(self):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("QRs", self.generateQRCode)],
            states={
                START: [MessageHandler(Filters.text, self.generate_qr_code)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        self.dispatcher.add_handler(conversation_handler)
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_click))

        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    token = '5999764893:AAHiKhdh5MmC_7p6Er0DkipjRPOZYOljyOE'
    bot = Bot(token)
    bot.run()
