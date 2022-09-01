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
            r = need_command(player, game) # Вызов ф-ии запроса команды у игрока
            if r == 'again':
                need_command(player, game)
            print('-------------------------------')


def need_command(player: Player, game):
    for com, value in COMMANDS_BASE.items():
        print(f'{com}: {value}')
    command = input(f'Команда игрок - ({player.name}): ')
    if command == '1':  # Бросок кубиков
        player.roll_the_dice([game.Cub1, game.Cub2])
        print(f'Позиция: {player.position}')
        for group in game.game_board.groups:  # Проверка на какое поле встал игрок
            for field in group.fields:
                if player.position == field.id and field.holder is None:  # Поле ничье - предложение купить
                    print(f'ПОЛЕ {field.name} ({field.group.name}) // {field.cost} RUB')
                    for com, value in COMMANDS_FIELD.items():
                        print(f'{com}: {value}')
                    command = input(f'Команда ({player.name}): ')
                    if command == '2':
                        player.buy_field(field)
                        return 'next'
                    elif command == '0':
                        break
                elif player.position == field.id and player is not field.holder:  # Поле кому-то принадлежит - платим ренту
                    player.pay_rent(field)
                    print(f'{player.money} (-{field.rent})')
                    break
        return 'next'
    elif command == 'info':
        print(f'''
        ИМЯ: {player.name}
        СЧЕТ: {player.money}
        МОИ ПОЛЯ: {[field.name for field in player.fields]}                
        ''')
        return 'again'



if __name__ == '__main__':
    main()
