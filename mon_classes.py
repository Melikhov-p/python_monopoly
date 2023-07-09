import random


class Board:
    def __init__(self):
        self.size = 40
        self.groups = []


class Group:
    def __init__(self, name, board: Board):
        self.name = name
        self.fields = []
        board.groups.append(self)
        self.group_owner = None

    def check_group_owner(self):  # Ф-ия проверки принадлежности всех полей группы одному человеку
        holders = [field.holder for field in self.fields]
        if len(holders) == len(self.fields) and len(set(holders)) == 1:
            self.group_owner = holders[0]
            for field in self.fields:
                field.collected_all_fields()
            return True


class Field:
    def __init__(self, id: int, name: str, cost: int, group: Group, type, rent: int, holder=None):
        self.id = id
        self.name = name
        self.cost = cost
        self.group = group
        self.type = type
        self.rent = rent
        self.holder = holder
        self.pledge = self.cost / 2
        self.pledge_status = False
        self.field_level = 0
        group.fields.append(self)

    def collected_all_fields(self):  # Все поля из группы у одного человек - повышаем ренту
        self.rent = self.rent + self.rent * 0.15

    def build(self):  # Построить филиал на поле
        if self.group.check_group_owner() and self.field_level <= 3:  # Проверка на принадлежность всех полей одному игроку
            self.rent = self.rent + self.rent * 0.3
            return True
        elif self.field_level >= 3:
            print('Достигнут лимит филиалов')
            return False


class Player:
    def __init__(self, id: int, name, money):
        self.id = id
        self.money = money
        self.name = name
        self.fields = []
        self.position = 0

    def get_field_by_name(self, field_name: str):
        for field in self.fields:
            if field_name == field.name:
                return field
        return None

    def buy_field(self, field: Field):  # Ф-ия купить поле
        if self.money >= field.cost and field.holder is None:
            self.fields.append(field)
            self.money -= field.cost
            field.holder = self
            return True
        else:
            return None

    def lay_field(self, field: Field):  # Ф-ия заложить поле
        if field.holder == self:
            self.money += field.pledge
            field.pledge_status = True
            return True

    def roll_the_dice(self, Cubes: list):  # Ф-ия бросить кубик
        dropped_sides = []
        for Cube in Cubes:
            dropped_sides.append(Cube.roll())
        print(f'Выпало: {dropped_sides[0]} и {dropped_sides[1]}')
        self.move(sum(dropped_sides))  # Ф-ия движение по кубику
        return dropped_sides

    def move(self, steps_amount):
        self.position += steps_amount
        if self.position > 40:
            self.money += 2000
            self.position -= 40
            print(f'{self.name} за прохождение круга +2000')

    def pay_rent(self, field: Field):  # Ф-ия заплатить ренту
        if self.money >= field.rent:
            self.money -= field.rent
            field.holder.money += field.rent

    def __str__(self):
        return self.name


class Cube:
    def __init__(self):
        self.sides = [1, 2, 3, 4, 5, 6]

    def roll(self):
        return random.choice(self.sides)


class Game:
    def __init__(self):
        # Players
        self.p1 = Player(1, 'P1', 15000)
        self.p2 = Player(2, 'P2', 15000)
        # Board
        self.game_board = Board()
        # Groups
        self.food_group = Group('food', self.game_board)
        self.auto_group = Group('auto', self.game_board)
        self.hotel_group = Group('hotel', self.game_board)
        self.cards = Group('cards', self.game_board)
        # Fields
        self.BK_field = Field(1, 'BK', 2400, self.food_group, 'classic', 220)
        self.McD_field = Field(2, 'McD', 2500, self.food_group, 'classic', 220)
        self.KFC_field = Field(3, 'KFC', 2600, self.food_group, 'classic', 250)

        self.BMW_field = Field(4, 'BMW', 2000, self.auto_group, 'classic', 250)
        self.Audi_field = Field(5, 'Audi', 2000, self.auto_group, 'classic', 250)
        self.Ford_field = Field(6, 'Ford', 2000, self.auto_group, 'classic', 250)
        self.Mercedes_field = Field(7, 'Mercedes', 2000, self.auto_group, 'classic', 250)

        self.card_1 = Field(9, 'Card', 0, self.cards, 'card', 0)
        self.card_2 = Field(18, 'Card', 0, self.cards, 'card', 0)
        self.card_3 = Field(27, 'Card', 0, self.cards, 'card', 0)
        self.card_4 = Field(36, 'Card', 0, self.cards, 'card', 0)

        self.Hyat_field = Field(10, 'Hyat', 3000, self.hotel_group, 'classic', 300)
        self.Raddison_field = Field(11, 'Raddison', 3200, self.hotel_group, 'classic', 315)
        self.Holliday_field = Field(12, 'Holliday', 3300, self.hotel_group, 'classic', 350)

        # Cubes
        self.Cub1 = Cube()
        self.Cub2 = Cube()
        self.card_actions = {'money': [2000, -2000, 1000, -1000, 5000, -5000], 'position': [2, 5, 4, -3, -8, -1]}

        # self.p1.buy_field(self.BK_field)
        # self.p1.buy_field(self.McD_field)
        # self.p1.buy_field(self.KFC_field)