from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)

        
        self.img = self.get_img()
        self.name = self.get_name()
        self.abilities = self.get_abilities()
        self.stats = self.get_stats()

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
    
    def get_stats(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['stats']:
                stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                return stats
            else:
                return "No stats found"
        else:
            # Статистика по умолчанию для Пикачу
            return {"hp": 35, "attack": 55, "defense": 40, "special-attack": 50, "special-defense": 50, "speed": 90}

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
        # Повышаем характеристики покемона с каждым уровнем
        for stat in self.stats:
            self.stats[stat] += 10  # Повышение всех статов на 10 за уровень

    # Метод для получения информации о покемоне
    def info(self):
        return (f"Имя твоего покемона: {self.name}\n"
                f"Уровень: {self.level}\n"
                f"Опыт: {self.experience}/{self.experience_to_next_level}\n"
                f"Статистика: \n{self.stats}")

    # Метод для получения картинки покемона
    def show_img(self):
        return self.img

    # Метод для показа способностей покемона
    def show_abilities(self):
        return f"Способности: {self.abilities}"

    # Метод для показа статистики покемона
    def show_stats(self):
        stats_info = "\n".join([f"{stat}: {value}" for stat, value in self.stats.items()])
        return f"Статистика:\n{stats_info}"

    # Метод для кормления покемона (получение опыта)
    def feed(self):
        self.gain_experience(50)
        return f"{self.name} получил 50 опыта!"




