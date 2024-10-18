import telebot 
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    #if message.from_user.username not in Pokemon.pokemons.keys():
    pokemon = Pokemon(message.from_user.username)
    bot.send_message(message.chat.id, pokemon.info())
    bot.send_photo(message.chat.id, pokemon.show_img())
    bot.send_message(message.chat.id, pokemon.show_abilities())
    bot.send_message(message.chat.id, pokemon.show_stats())
    #else:
    #bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        response = pokemon.feed()  
        bot.send_message(message.chat.id, response)  # Сообщаем о результате
        bot.send_message(message.chat.id, pokemon.info())  # Обновленная информация о покемоне
    else:
        bot.reply_to(message, "У тебя пока нет покемона. Напиши /go для создания покемона.")  # Если покемона нет

bot.infinity_polling(none_stop=True)

