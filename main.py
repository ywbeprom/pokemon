import random

element_bonus = {
    "fire": {"water": 0.75, "earth": 1.5, "air": 1.0, "electric": 1.0},
    "water": {"fire": 1.5, "earth": 0.75, "air": 1.0, "electric": 1.0},
    "earth": {"fire": 0.75, "water": 1.5, "air": 1.0, "electric": 1.0},
    "air": {"fire": 1.0, "water": 1.0, "earth": 1.5, "electric": 0.75},
    "electric": {"fire": 1.0, "water": 1.5, "earth": 0.75, "air": 1.0}
}
possible_names = ["Charmander", "Squirtle", "Bulbasaur", "Pikachu", "Eevee"]
elements = ["fire", "water", "earth", "air", "electric"]

def generate_pokemon(level=1):
    name = random.choice(possible_names)
    element = random.choice(elements)
    max_hp = 50 + level * 50
    attack = 20 + level * 20
    return {
        'name': name,
        'element': element,
        'level': level,
        'hp': max_hp,
        'max_hp': max_hp,
        'attack': attack,
        'exp': 0
    }


starter_deck = [generate_pokemon(1) for _ in range(3)]

player = {
    "lives": 3,
    "deck": starter_deck.copy()
}
def calculate_damage(attacker, defender):
    base_damage=attacker['attack']
    att_elem=attacker['element']
    def_elem=defender["element"]
    if att_elem == def_elem:
        bonus=1.0
    else:
        bonus=element_bonus[att_elem][def_elem]
    random_damage = base_damage * bonus* random.uniform(0.9,1.2)
    return round(random_damage)    


def battle(attacker,defender):
    attacker_counter = 0
    defender_counter = 0
    while True:
        attacker_counter+=1
        damage_to_defender = calculate_damage(attacker, defender)
        if attacker_counter == 3:
            damage_to_defender *= 2
            defender['hp']-= damage_to_defender
            print(f"Критический удар! {attacker['name']} наносит {damage_to_defender} урона. У {defender['name']} осталось {defender['hp']} HP.")
            attacker_counter=0
        else:
            defender['hp']-= damage_to_defender
            print(f"{attacker['name']} наносит {damage_to_defender} урона. У {defender['name']} осталось {defender['hp']} HP.")
        if defender['hp'] <=0:
            print(f"{defender['name']} повержен!")
            return 'attacker_wins'
        
        else:
            defender_counter += 1
            damage_to_attacker = calculate_damage(defender, attacker)
            if defender_counter == 3:
                damage_to_attacker *= 2
                attacker['hp']-=damage_to_attacker
                print(f"Критический удар! {defender['name']} наносит {damage_to_attacker} урона.У {attacker['name']} осталось {attacker['hp']} HP.")
                defender_counter=0
            else:
                attacker['hp']-=damage_to_attacker
                print(f"{defender['name']} наносит {damage_to_attacker} урона.У {attacker['name']} осталось {attacker['hp']} HP.")
            if attacker['hp'] <=0:
                print(f"{attacker['name']} повержен!")
                return 'defender_wins'


def gain_exp(player_pokemon,count):
    player_pokemon['exp']+=count
    while player_pokemon['exp'] >= 100*player_pokemon['level']:
        need_exp=100*player_pokemon['level']
        player_pokemon['exp'] -= need_exp
        player_pokemon['level']+=1
        player_pokemon['max_hp'] = 50 + player_pokemon['level'] * 50
        player_pokemon['attack'] = 20 + player_pokemon['level'] * 5
        player_pokemon['hp'] = player_pokemon['max_hp'] 
        print(f"{player_pokemon['name']} повысил уровень до {player_pokemon['level']}!") 



def heal_pokemon(pokemon):
    pokemon['hp']=pokemon['max_hp']

def print_deck(deck):
     for i in range(len(deck)):
        pokemon = deck[i]
        print(f"{i+1}. {pokemon['name']} ({pokemon['element']}) lvl:{pokemon['level']} HP:{pokemon['hp']}/{pokemon['max_hp']} ATK:{pokemon['attack']}")
         

def lvl_calc(turn):
    max_lvl = int(1 + turn / 5)
    return random.choice(list(range(1, max_lvl + 1))[-3:])        


def main_cycle():
    total_wins=0
    print("Добро пожаловать в игру Pokemon!")


    while player['lives']>0:
        opponent_level=lvl_calc(total_wins)
        opponent = generate_pokemon(opponent_level)

        print('Твоя колода:')
        print_deck(player['deck'])

        print(f"Противник: {opponent['name']} ({opponent['element']}) lvl:{opponent['level']} HP:{opponent['hp']}/{opponent['max_hp']} ATK:{opponent['attack']}")

        while True:
            choice=int(input('Введи число от 1 до 3: '))
            if choice==0:
                print('Введи число от 1 до 3: ')
            if 1 <= choice <= len(player['deck']):
                break

        player_pokemon = player["deck"][choice-1]
        opponent_copy = opponent.copy()
        print(f"{player_pokemon['name']} vs {opponent_copy['name']}")
                
        result=battle(player_pokemon, opponent_copy)

        if result=='attacker_wins':
                print('Победа')
                total_wins+=1
                gain_exp(player_pokemon, 50 + opponent['level'] * 10)
                heal_pokemon(player_pokemon)

                answer = input(f"Забрать {opponent['name']} в колоду? (да/нет): ").lower()
                if answer == "да":
                    if len(player['deck']) < 5:
                        player['deck'].append(opponent)
                        print("Новый покемон добавлен в колоду!")
                    else:
                        print("Твоя колода полна. Выбери покемона для замены (0 - отказ):")
                        print_deck(player['deck'])

                        while True:
                            idx = int(input("Твой выбор: "))
                            if idx == 0:
                                print("Покемон не добавлен.")
                                break
                            if 1 <= idx <= 5:
                                player['deck'].pop(idx - 1)
                                player['deck'].append(opponent)
                                print("Покемон заменён!")
                                break
                            else:
                                print("Введи число от 1 до 5 или 0.")


        elif result == 'defender_wins':
                print('Поражение')
                heal_pokemon(player_pokemon)
                player['lives']-=1
                print(f"Осталось жизней: {player['lives']}")
                if player['lives'] == 0:
                  print("Игра окончена.")
                  break
                

        else:
                print("Ничья!")
                heal_pokemon(player_pokemon)
                

        if not player['deck']:
                print("У тебя не осталось покемонов! Добавляем нового...")
                player['deck'].append(generate_pokemon(1))

    print(f'Ты набрал {total_wins} побед. Спасибо за игру!')


main_cycle()             
