from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer  
        self.pokemon_number = randint(1, 1000)
        self.hp = randint(5, 100)
        self.power = randint(1, 100)
        self.was_attacked = False  # Новый атрибут для отслеживания состояния атаки

        
        self.img = self.get_img()
        self.name = self.get_name()
        self.abilities = self.get_abilities()
        #self.stats = self.get_stats()

        # Новые свойства: уровень, опыт и необходимый опыт до следующего уровня
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100  # Начальный опыт для повышения уровня

        Pokemon.pokemons[pokemon_trainer] = self


    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['abilities']:
                return (data['abilities'][0]['ability']['name'])
            else:
                return "No abilities found"
        else:
            return "Lightning-rod"  
    
    #def get_stats(self):
        #url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        #response = requests.get(url)
        #if response.status_code == 200:
            #data = response.json()
            #if data['stats']:
                #stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                #return stats
            #else:
                #return "No stats found"
        #else:
            # Статистика по умолчанию для Пикачу
            #return {"hp": 35, "attack": 55, "defense": 40, "special-attack": 50, "special-defense": 50, "speed": 90}

    # Метод для получения опыта
    def gain_experience(self, exp_points):
        self.experience += exp_points
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    # Метод для повышения уровня
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_next_level += 100  
        self.hp += 10 
        self.power += 5
        # Повышаем характеристики покемона с каждым уровнем
        #for stat in self.stats:
            #self.stats[stat] += 10  # Повышение всех статов на 10 за уровень


    # Метод для получения информации о покемоне
    def info(self):
        return (f"Имя твоего покемона: {self.name}\n"
                f"Уровень: {self.level}\n"
                f"Опыт: {self.experience}/{self.experience_to_next_level}\n"
                #f"Статистика: \n{self.stats}"
                f"Здоровье : {self.hp}\n"
                f"Сила: {self.power}\n")
    

    # Метод для получения картинки покемона
    def show_img(self):
        return self.img

    # Метод для показа способностей покемона
    def show_abilities(self):
        return f"Способности: {self.abilities}"

    # Метод для показа статистики покемона
    #def show_stats(self):
        #stats_info = "\n".join([f"{stat}: {value}" for stat, value in self.stats.items()])
        #return f"Статистика:\n{stats_info}"

    # Метод для кормления покемона (получение опыта)
    def feed(self):
        self.gain_experience(50)
        return f"{self.name} получил 50 опыта!"

    # Новый метод атаки
    def attack(self, enemy):
        enemy.was_attacked = True 
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"

        if self.hp <= 0:
            return f"{self.name} не может атаковать, он побежден!"
        
        # Расчет урона
        enemy.hp -= self.power
        
        if enemy.hp <= 0:
            enemy.hp = 0
            result = f"{self.name} атаковал {enemy.pokemon_trainer} и нанес {self.power} урона. {enemy.pokemon_trainer} побежден!"
            self.gain_experience(100)  # Опыт за победу
        else:
            result = f"{self.name} атаковал {enemy.pokemon_trainer} и нанес {self.power} урона. У {enemy.pokemon_trainer} осталось {enemy.hp} HP."
        
        return result
    
    def heal(self):
        if self.was_attacked:
            self.hp += 20  # Можно установить любое значение лечения
            self.was_attacked = False  # Сбрасываем состояние после лечения
            return f"{self.name} восстановил здоровье! Теперь у него {self.hp} hp"
        else:
            return f"{self.name} не был атакован и не нуждается в лечении."

class Wizard(Pokemon):
    def info(self):
        return f"Это покемон-волшебник"


class Fighter(Pokemon):
    def info(self):
        return f"Это покемон-боец"
    
    def attack(self, enemy):
        super_power = randint(5,15)   
        self.power += super_power
        результат = super().attack(enemy)
        self.power -= super_power
        return результат + f"\nБоец применил супер-атаку силой:{super_power} "




