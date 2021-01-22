import pygame
import os
import sys
import subprocess


class Level:  # класс для генерации уровня
    def generate_level(self, level):  # генерация уровня из файла с картой
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':  # по значению x, y на карте изображение перемещается на определенную позицию
                    Tile('swamp', x, y)
                elif level[y][x] == '+':
                    Tile('river', x, y)
                elif level[y][x] == '/':
                    Tile('path_round_left_up', x, y)
                elif level[y][x] == '"':
                    Tile('path_round_left_down', x, y)
                elif level[y][x] == '#':
                    Tile('path_center', x, y)
                elif level[y][x] == '*':
                    Tile('sprike_down', x, y)
                elif level[y][x] == '$':
                    Tile('path_center', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '-':
                    Tile('swamp2', x, y)
                elif level[y][x] == '&':
                    Tile('grass', x, y)
                elif level[y][x] == '=':
                    Tile('path_round_right_down', x, y)
                elif level[y][x] == '%':
                    Tile('path_round_right_up', x, y)
                elif level[y][x] == '^':
                    Tile('path_str_up', x, y)
                elif level[y][x] == '(':
                    Tile('path_str_left', x, y)
                elif level[y][x] == ')':
                    Tile('path_str_right', x, y)
                elif level[y][x] == ',':
                    Tile('path_str_down', x, y)
                elif level[y][x] == ';':
                    Tile('path_str_right', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == ':':
                    Tile('path_str_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '?':
                    Tile('path_str_left', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '}':
                    Tile('path_str_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '{':
                    Tile('path_round_right_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == ']':
                    Tile('path_round_right_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '[':
                    Tile('path_round_left_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '|':
                    Tile('path_round_left_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '~':
                    Tile('path_gor', x, y)
                elif level[y][x] == '_':
                    Tile('path_vert', x, y)
                elif level[y][x] == '!':
                    Tile('target', x, y)
                else:
                    Tile('path_center', x, y)
                    new_player = Player(player_image, 6, 1, x, y)
        return new_player, x, y

    def decor_first(self):  # некоторые украшения первого уровня
        Tile('image_grass', 10, 4.5)
        Tile('image_plant', 0, 0)
        Tile('image_seaweed', 3, 3)
        Tile('image_house', 1, 7)
        Tile('image_tree', 4, 9.5)
        Tile('image_swamp', 12, 2)
        Tile('image_big_tree', 13, 11)

    def decor_third(self):  # некоторые украшения третьего уровня
        Tile('sign_image', 7.4, 5.1)
        Tile('donkey', 6, 3.5)

    def load_image(self, name):  # загрузка картинки
        fullname = os.path.join('images', name)  # тк у меня все картинки находятся в папке images, то я строю к ней
        image = pygame.image.load(fullname)  # путь
        return image

    def load_level(self, filename):  # загрузка уровня из текстового файла с картой
        filename = "levels/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):  # класс для расставления спрайтов в окне pygame
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        if 'path' in tile_type or tile_type == 'target':  # по названию спрайта проверяю можно ли будет персонажу ходить
            mozhno_group.add(all_sprites.sprites()[-1])  # по нему или нет и добавляю в соответствующую группу
            if 'target' in tile_type:
                target_group.add(all_sprites.sprites()[-1])
        elif 'zhuk' in tile_type:
            zhuk_group.add(all_sprites.sprites()[-1])
        elif 'sprike' in tile_type:
            sprike_group.add(all_sprites.sprites()[-1])
        else:
            nelzay_group.add(all_sprites.sprites()[-1])


class Player(pygame.sprite.Sprite):  # класс для спрайта и передвижения персонажа
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames_player = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame_player = 0
        self.image = self.frames_player[self.cur_frame_player]
        self.rect = self.rect.move(x * tile_width, y * tile_height)  # вставка спрайта на определенную позицию

    def cut_sheet(self, sheet, columns, rows):  # обрезка спрайта
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_player.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):  # движение спрайта
        self.cur_frame_player = (self.cur_frame_player + 1) % len(self.frames_player)
        self.image = self.frames_player[self.cur_frame_player]

    def move_right(self):  # движение персонажа вправо
        self.rect.x += 45  # условно перемещаю спрайт вправо
        if not pygame.sprite.spritecollide(player, nelzay_group, False):  # проверяю, сталкивается ли спрайт
            # с спрайтом, на который ему нельзя заходить, если нет - движение вправо
            pygame.sprite.spritecollide(player, zhuk_group, True)  # если сталкивается с жуком, он его ест
            if pygame.sprite.spritecollide(player, target_group, False):  # если встает на мишень
                global on_target
                on_target = True
            for i in pygame.sprite.spritecollide(player, sprike_group, False):
                if i.image == tile_images['sprike_down']:  # если встает на шипы и они опущенны, то шипы поднимаются
                    Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                else:  # а если они подняты, то персонаж умирает
                    global player_die
                    player_die = True
        else:  # если да, то движения вправо не будет
            self.rect.x -= 45

    def move_left(self):  # со всем остальным движением все аналогично
        self.rect.x -= 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            for i in pygame.sprite.spritecollide(player, sprike_group, False):
                if i.image == tile_images['sprike_down']:
                    Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                else:
                    global player_die
                    player_die = True
        else:
            self.rect.x += 45

    def move_up(self):
        self.rect.y += 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            for i in pygame.sprite.spritecollide(player, sprike_group, False):
                if i.image == tile_images['sprike_down']:
                    Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                else:
                    global player_die
                    player_die = True
        else:
            self.rect.y -= 45

    def move_down(self):
        self.rect.y -= 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            for i in pygame.sprite.spritecollide(player, sprike_group, False):
                if i.image == tile_images['sprike_down']:
                    Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                else:
                    global player_die
                    player_die = True
        else:
            self.rect.y += 45


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    mozhno_group = pygame.sprite.Group()  # спрайты, на которые персонажу можно вставать
    nelzay_group = pygame.sprite.Group()  # спрайты, на которые персонажу нельзя вставать
    sprike_group = pygame.sprite.Group()  # спрайты с шипами
    zhuk_group = pygame.sprite.Group()  # спрайты с жуками
    target_group = pygame.sprite.Group()  # спрайты с мишенью
    player_group = pygame.sprite.Group()
    FPS = 20
    clock = pygame.time.Clock()
    pygame.display.set_icon(Level().load_image("icon.png"))  # загрузка иконки
    pygame.display.set_caption('shrek swamp')  # загрузка названия окна
    size = width, height = 675, 675
    screen = pygame.display.set_mode(size)
    tile_images = {  # загрузка изображений
        'path_round_left_up': Level().load_image('path1.png'),
        'river': Level().load_image('swamp1.png'),
        'sprike_down': Level().load_image('sprike1.png'),
        'sign_image': Level().load_image('sign_image.png'),
        'donkey': Level().load_image('donkey_image.png'),
        'zhuk': Level().load_image('zhuk.png'),
        'path_round_right_up': Level().load_image('path4.png'),
        'swamp': Level().load_image('swamp3.png'),
        'swamp2': Level().load_image('swamp4.png'),
        'grass': Level().load_image('grass.png'),
        'sprike_up': Level().load_image('sprike2.png'),
        'path_round_left_down': Level().load_image('path2.png'),
        'path_round_right_down': Level().load_image('path3.png'),
        'path_center': Level().load_image('path5.png'),
        'path_gor': Level().load_image('path_gor.png'),
        'path_vert': Level().load_image('path_vert.png'),
        'path_str_up': Level().load_image('path6.png'),
        'path_str_left': Level().load_image('path7.png'),
        'path_str_down': Level().load_image('path8.png'),
        'path_str_right': Level().load_image('path9.png'),
        'zhuk_str_right': Level().load_image('zhuk_right.png'),
        'zhuk_str_down': Level().load_image('zhuk_down.png'),
        'zhuk_str_left': Level().load_image('zhuk_left.png'),
        'zhuk_str_up': Level().load_image('zhuk_up.png'),
        'zhuk_round_right': Level().load_image('zhuk_round_right.png'),
        'zhuk_round_right2': Level().load_image('zhuk_round_right2.png'),
        'zhuk_round_left2': Level().load_image('zhuk_round_left2.png'),
        'zhuk_round_left': Level().load_image('zhuk_round_left.png'),
        'target': Level().load_image('target.png'),
        'image_plant': Level().load_image("plant.png"),
        'image_seaweed': Level().load_image("seaweed.png"),
        'image_wood': Level().load_image("wood.png"),
        'image_tree': Level().load_image("tree.png"),
        'image_swamp': Level().load_image("swamp5.png"),
        'image_big_tree': Level().load_image("tree2.png"),
        'image_house': Level().load_image("house.png"),
        'image_grass': Level().load_image("grass2.png"),
        'lose': Level().load_image('lose.png')
    }
    player_image = Level().load_image("shrek_idet.png")
    player_die = False  # если персонаж умер - True
    on_target = False  # если персонаж на мишени - True
    level_number = 1  # номер уровня
    tile_width = tile_height = 45  # размер спрайта
    player, level_x, level_y = Level().generate_level(Level().load_level('level 1.0.txt'))  # загрузка первого уровня
    Level().decor_first()  # украшение первого уровня
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # если нажата правая стрелка
                    x_now = player.rect.x // tile_width  # "запоминаю" нахождение персонажа на поле
                    y_now = player.rect.y // tile_height
                    player.kill()  # "убиваю" его
                    player = Player(Level().load_image("shrek_idet.png"), 6, 1, x_now, y_now)  # и на его место вставляю
                    repeat = 0  # определенный спрайт (в зависимости от направления движения)
                    player.move_right()  # проверка на движение в том направлении и само движение, если оно возможно
                    while repeat < 6:  # обновление спрайта (тк он должен двигаться во время передвижения, т е должны
                        clock.tick(FPS)  # изменяться картинки (их 6, поэтому обновление происходит 6 раз)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        repeat += 1
                if event.key == pygame.K_LEFT:  # с остальным движением все аналогично
                    x_now = player.rect.x // tile_width
                    y_now = player.rect.y // tile_height
                    player.kill()
                    player = Player(Level().load_image("shrek_idet5.png"), 6, 1, x_now, y_now)
                    repeat = 0
                    player.move_left()
                    while repeat < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        repeat += 1
                if event.key == pygame.K_UP:
                    x_now = player.rect.x // tile_width
                    y_now = player.rect.y // tile_height
                    player.kill()
                    player = Player(Level().load_image("shrek_up.png"), 1, 1, x_now, y_now)
                    player.move_down()
                    clock.tick(FPS)
                    player.update()
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    x_now = player.rect.x // tile_width
                    y_now = player.rect.y // tile_height
                    player.kill()
                    player = Player(Level().load_image("shrek_down.png"), 1, 1, x_now, y_now)
                    player.move_up()
                    clock.tick(FPS)
                    player.update()
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
        if len(zhuk_group.sprites()) == 0 and on_target:  # если персонаж на мишени и все жуки собраны
            x_now = player.rect.x // tile_width
            y_now = player.rect.y // tile_height
            player.kill()
            player = Player(Level().load_image("shrek_win.png"), 6, 1, x_now, y_now)  # спрайт перехода на новый уровень
            repeat = 0
            while repeat < 6:
                clock.tick(FPS)
                player.update()
                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
                repeat += 1
            player.kill()
            subprocess.call('python win.py')  # картинка, что игрок выиграл
            all_sprites = pygame.sprite.Group()  # формирование нового уровня
            mozhno_group = pygame.sprite.Group()
            nelzay_group = pygame.sprite.Group()
            sprike_group = pygame.sprite.Group()
            zhuk_group = pygame.sprite.Group()
            target_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            player_image = Level().load_image("shrek_idet.png")
            player_die = False
            on_target = False
            if level_number == 1:  # и его загрузка
                player, level_x, level_y = Level().generate_level(Level().load_level('level 2.0.txt'))
                level_number = 2
            elif level_number == 2:
                player, level_x, level_y = Level().generate_level(Level().load_level('level 3.0.txt'))
                Level().decor_third()
                level_number = 3
            elif level_number == 3:
                pygame.quit()  # после третьего уровня игра заканчивается
                subprocess.call('python end.py')
                sys.exit()
        if player_die:  # если игрок умер
            x_now = player.rect.x // tile_width
            y_now = player.rect.y // tile_height
            player.kill()
            player = Player(Level().load_image("shrek_umer.png"), 6, 1, x_now, y_now)
            repeat = 0
            while repeat < 6:
                clock.tick(FPS)
                player.update()
                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
                repeat += 1
            pygame.quit()
            subprocess.call('python lose.py')  # картинка, что игрок проиграл
            sys.exit()
        all_sprites.draw(screen)  # "рисование" спрайтов в окне
        zhuk_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
