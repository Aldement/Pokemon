import telebot 
import random
from config import token

from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = random.randint(1,10)
        if chance == 1 or chance >= 7:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 7 or chance == 8:
            pokemon = Wizard(message.from_user.username)
        elif chance == 9 or chance == 10:
            pokemon = Fighter(message.from_user.username)

        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_message(message.chat.id, pokemon.show_abilities())
    #bot.send_message(message.chat.id, pokemon.show_stats())
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

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
            bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['heal'])
def heal_pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        # Проверка состояния атаки перед лечением
        res = pok.heal()
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, "Вы не являетесь покемоном и не можете быть вылечены.")

@bot.message_handler(commands=['info'])
def info_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())
    else:
        bot.send_message(message.chat.id, "У вас нет покемона.")

bot.infinity_polling(none_stop=True)

