import random

from mon_classes import *

COMMANDS_BASE = {
    '1': 'Бросить кубики',
    'info': 'Информация',
    '0': 'Закончить игру'
}
COMMANDS_FIELD = {
    '2': 'Купить поле',
    '0': 'Пропустить'
}

def main():
    game = Game()
    p1 = game.p1
    p2 = game.p2
    players = [p1, p2]
    while True:
        for player in players:
            r = need_command(player, game)  # Вызов ф-ии запроса команды у игрока
            if r == 'again':
                need_command(player, game)
            print('-------------------------------')


def need_command(player: Player, game):
    for com, value in COMMANDS_BASE.items():
        print(f'{com}: {value}')
    command = input(f'Команда игрок - ({player.name}): ')
    if command == '1':  # Бросок кубиков
        dropped_sides = player.roll_the_dice([game.Cub1, game.Cub2])
        print(f'Позиция: {player.position}')
        for group in game.game_board.groups:  # Проверка на какое поле встал игрок
            for field in group.fields:
                if player.position == field.id:  # Поле ничье - предложение купить
                    field_action(player, field, game)
                    break
        if dropped_sides[0] == dropped_sides[1]:  # Если выпал дубль - ещё один ход
            return 'again'
        return 'next'
    elif command == 'info':
        print(f'''
        Позиция: {player.position}
        ИМЯ: {player.name}
        СЧЕТ: {player.money}
        МОИ ПОЛЯ: {[field.name for field in player.fields]}                
        ''')
        return 'again'

def field_action(player: Player, field: Field, game: Game):  # Ф-ия для действий полей (ПОЛЯ-карточки прибавляют/убавляют деньги/позицию)
    if field.type == 'card':
        print('---Поле шанс---')
        value = random.choice(list(game.card_actions.keys()))
        action = random.choice(game.card_actions[value])
        if value == 'money':
            player.money += action
        elif value == 'position':
            player.position += action
        print(value + ' ' + str(action))
        print('---Поле шанс---')
    if field.holder is None and field.type != 'card':  # Поле ничье - предложение купить
        print(f'ПОЛЕ {field.name} ({field.group.name}) // {field.cost} RUB')
        for com, value in COMMANDS_FIELD.items():
            print(f'{com}: {value}')
        command = input(f'Команда ({player.name}): ')
        if command == '2':
            player.buy_field(field)
        elif command == '0':
            pass
    elif field.holder is not None and field.holder != player:  # Поле кому-то принадлежит - платим ренту
        player.pay_rent(field)
        print(f'{field.name} || Рента игроку {field.holder.name} (-{field.rent}) || Оставшийся баланс: {player.money} ')


if __name__ == '__main__':
    main()
