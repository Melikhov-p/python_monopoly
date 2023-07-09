from mon_classes import *

COMMANDS_BASE = {
    '1': 'Бросить кубики',
    'lay': 'Заложить поле',
    'build': 'Построить корпус',
    'info': 'Информация',
    'exit': 'Закончить игру'
}
COMMANDS_FIELD = {
    'buy': 'Купить поле',
    '0': 'Пропустить'
}


def main():
    game = Game()
    p1 = game.p1
    p2 = game.p2
    players = [p1, p2]
    while True:
        for player in players:
            separator = '--------------------------------------------------------------'
            step_by = f'ХОД ИГРОКА {player.name.upper()}'
            print(separator)
            print('|' * int((len(separator)-len(step_by))/2) + step_by + '|' * int((len(separator)-len(step_by))/2))
            print(separator)
            need_command(player, game)  # Вызов ф-ии запроса команды у игрока


def need_command(player: Player, game):
    noneGroup = True
    command_base_lines = []
    for com, value in COMMANDS_BASE.items():
        command_base_lines.append(f'{com}: {value}')
    draw_info(command_base_lines)  # Отрисовка команд в таблице
    command = input(f'Команда игрок - ({player.name}): ')
    print('▼'*16)
    if command == '1':  # Бросок кубиков
        dropped_sides = player.roll_the_dice([game.Cub1, game.Cub2])
        print(f'Позиция: {player.position}')
        for group in game.game_board.groups:  # Проверка на какое поле встал игрок
            for field in group.fields:
                if player.position == field.id:  # Поле ничье - предложение купить
                    field_action(player, field, game)
                    noneGroup = False
                    break
        if noneGroup:
            print('ПОЛЕ пусто')
            input('Enter для продолжения')
        if dropped_sides[0] == dropped_sides[1]:  # Если выпал дубль - ещё один ход
            print('Выпал дубль, ещё один ход.')
            need_command(player, game)
        return 'next'
    elif command == 'lay':
        print([field.name for field in player.fields])
        field_name_to_lay = input('Название поля которое хотите заложить: ')
        field_to_lay = player.get_field_by_name(field_name_to_lay)
        if field_to_lay is None:
            print(f'Неверное имя поля: {field_name_to_lay}')
            need_command(player, game)  # Ход не тратится
        result_lay = player.lay_field(field_to_lay)
        if result_lay:
            print(f'Поле {field_name_to_lay} заложен (Деньги + {field_to_lay.pledge})')
        need_command(player, game)  # Ход не тратится
    elif command == 'build':
        players_field_to_build = [field.name for field in player.fields if field.group.check_group_owner()]
        if len(players_field_to_build) != 0:
            print(players_field_to_build)
            field_name_to_build = input('На каком поле построить корпус?: ')
            field_to_build = player.get_field_by_name(field_name_to_build)
            if field_to_build is None:
                print(f'Неверное имя поля: {field_name_to_build}')
                need_command(player, game)  # Ход не тратится
            result_build = player.build_field(field_to_build)
            if result_build:
                print(f'На поле {field_name_to_build} построен корпус. Новая рента {field_to_build.rent}')

        else:
            print('Нет ни одной группы поле')
        need_command(player, game)
    elif command == 'info':
        draw_info([
            f'Позиция: {player.position}',
            f'ИМЯ: {player.name}',
            f'СЧЕТ: {player.money}',
            f'МОИ ПОЛЯ: {[field.name for field in player.fields]}'])
        input('Enter для продолжения')
        need_command(player, game)  # Ход не тратится

    elif command == 'exit':
        print('EXIT')
        exit(0)

    elif command not in COMMANDS_BASE.keys():
        print('НЕВЕРНАЯ КОМАНДА')
        input('Enter для продолжения')
        need_command(player, game)

def field_action(player: Player, field: Field, game: Game):  # Ф-ия для действий полей (ПОЛЯ-карточки прибавляют/убавляют деньги/позицию)
    if field.type == 'card':
        print('---Поле шанс---')
        value = random.choice(list(game.card_actions.keys()))
        action = random.choice(game.card_actions[value])
        if value == 'money':
            player.money += action
        elif value == 'position':
            player.position += action
        draw_info([value + ' ' + str(action)])
        print('---Поле шанс---')
    if field.holder is None and field.type != 'card':  # Поле ничье - предложение купить
        print(f'ПОЛЕ {field.name} ({field.group.name}) // {field.cost} RUB')
        command_fields_lines = []
        for com, value in COMMANDS_FIELD.items():
            command_fields_lines.append(f'{com}: {value}')
        draw_info(command_fields_lines)  # Отрисовка команд для поля в таблице
        command = input(f'Команда ({player.name}): ')
        if command == 'buy':
            player.buy_field(field)
            field.group.check_group_owner()  # Проверка принадлежат все поля из группы одному человеку - если да, повышаем ренту
        elif command == '0':
            pass
    elif field.holder is not None and field.holder != player:  # Поле кому-то принадлежит - платим ренту
        player.pay_rent(field)
        print(f'{field.name} || Рента игроку {field.holder.name} (-{field.rent}) || Оставшийся баланс: {player.money} ')


def draw_info(lines: list):
    width_border = len(max(lines, key=len))
    for line in lines:
        print('+' + '-' * width_border + '+')
        print('|' + line + ' ' * (width_border - len(line)) + '|')
    print('+' + '-' * width_border + '+')


if __name__ == '__main__':
    main()
