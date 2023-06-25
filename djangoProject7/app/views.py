from django.shortcuts import render
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .models import ChatIds
from django.db import connection




class Adress:
    bot = telebot.TeleBot("5999764893:AAHiKhdh5MmC_7p6Er0DkipjRPOZYOljyOE")
    def setCaffeName(self, caffeName):
        self.caffeName = caffeName

    def setChatId(self, chatId):
        self.chatId = chatId

    def getChatId(self):
        return self.chatId

    def getCaffeName(self):
        return self.caffeName


class Message:
    def __init__(self):
        self.table_id = None
        self.message = None

    def __int__(self, table_id, message):
        self.table_id = table_id
        self.message = message

    def setTableId(self, table_id):
        self.table_id = table_id

    def setMessage(self, message):
        self.message = str(self.table_id) + " " + message

    def getMessage(self):
        return self.message

    def getTableId(self):
        return self.table_id


message = Message()
adress = Adress()




def send_html_message(request):
    start()
    return render(request, 'last.html')



def index(request):
    message.setTableId(request.GET.get('tableId'))
    name = request.GET.get('name')
    adress.setChatId(get_value_from_model_using_sql("chatId", name, "caffeName"))
    return render(request, 'main.html')


staticmethod
def get_value_from_model_using_sql(find, name, value):
    sql_query = f"SELECT {find} FROM app_ChatIds WHERE {value} = '{name}'"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchone()  # Retrieve the first row
        if result:
            attribute_value = result[0]  # Access the attribute value
            return attribute_value
    return None


def start():
        # Create the inline keyboard with buttons
        if message.getTableId():
            print(message.getTableId())

            keyboard = [
                [InlineKeyboardButton("Принять заказ ", callback_data=str(message.getTableId()))],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the message with buttons
            message_text = str(message.getTableId()) + " столик вызывает официанта"
            adress.bot.send_message(chat_id=adress.getChatId(), text=message_text, reply_markup=reply_markup)
        else:
            print("Doesnt work")





