import telegram
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


bot_token = "5999764893:AAHiKhdh5MmC_7p6Er0DkipjRPOZYOljyOE"
chat_id = "-935758006"
bot = telebot.TeleBot(bot_token)

class TelegramBot:

    @bot.message_handler(content_types=['photo'])
    def photo(self):
        bot.send_message(chat_id, "photoWork")



    def start(self):
            keyboard = [
                [InlineKeyboardButton("Button 1", callback_data='button1')],
                [InlineKeyboardButton("Button 2", callback_data='button2')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the message with buttons
            message_text = "Какой-то столик просит счет"
            bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
            self.setUpdater()

    def button_click(update, context):

        query = update.callback_query
        button_clicked = query.data

        # Handle the button click based on the button identifier
        if button_clicked == 'button1':
            print("work")
            user = query.from_user.first_name
            deleted_message = query.message
            context.bot.delete_message(chat_id=deleted_message.chat_id, message_id=deleted_message.message_id)
            context.bot.send_message(chat_id=deleted_message.chat_id, text=f"{user} zabral zakaz!")
        else:
            print("doesnt work")


    def setUpdater(self):
        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher

        button_handler = CallbackQueryHandler(self.button_click)
        dispatcher.add_handler(button_handler)
