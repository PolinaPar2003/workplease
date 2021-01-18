import pygame


class LevelFirst:
    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('swamp', x, y, 1)
                elif level[y][x] == '+':
                    Tile('river', x, y, 1)
                elif level[y][x] == '/':
                    Tile('path_round_left_up', x, y, 1)
                elif level[y][x] == '"':
                    Tile('path_round_left_down', x, y, 1)
                elif level[y][x] == '#':
                    Tile('path_center', x, y, 1)
                elif level[y][x] == '*':
                    Tile('sprike_down', x, y, 1)
                elif level[y][x] == '$':
                    Tile('path_center', x, y, 1)
                    Tile('zhuk', x, y, 1)
                elif level[y][x] == '-':
                    Tile('swamp2', x, y, 1)
                elif level[y][x] == '&':
                    Tile('grass', x, y, 1)
                elif level[y][x] == '=':
                    Tile('path_round_right_down', x, y, 1)
                elif level[y][x] == '%':
                    Tile('path_round_right_up', x, y, 1)
                elif level[y][x] == '^':
                    Tile('path_str_up', x, y, 1)
                elif level[y][x] == '(':
                    Tile('path_str_left', x, y, 1)
                elif level[y][x] == ')':
                    Tile('path_str_right', x, y, 1)
                elif level[y][x] == ',':
                    Tile('path_str_down', x, y, 1)
                elif level[y][x] == ';':
                    Tile('path_str_right', x, y, 1)
                    Tile('zhuk', x, y, 1)
                elif level[y][x] == ':':
                    Tile('path_str_down', x, y, 1)
                    Tile('zhuk', x, y, 1)
                elif level[y][x] == '?':
                    Tile('path_str_left', x, y, 1)
                    Tile('zhuk', x, y, 1)
                elif level[y][x] == '}':
                    Tile('path_str_up', x, y, 1)
                    Tile('zhuk', x, y, 1)
                elif level[y][x] == '{':
                    Tile('zhuk_round_right', x, y, 1)
                elif level[y][x] == ']':
                    Tile('zhuk_round_right2', x, y, 1)
                elif level[y][x] == '[':
                    Tile('zhuk_round_left2', x, y, 1)
                elif level[y][x] == '|':
                    Tile('zhuk_round_left', x, y, 1)
                elif level[y][x] == '~':
                    Tile('path_gor', x, y, 1)
                elif level[y][x] == '_':
                    Tile('path_vert', x, y, 1)
                elif level[y][x] == '!':
                    Tile('target', x, y, 1)
                else:
                    Tile('path_center', x, y, 1)
                    #Player(, 6, 1, 60, 50)
                    new_player = Player(player_image, 6, 1, x, y)
        return new_player, x, y

    def decor(self):
        Tile('image_grass', 327, 329, 0)
        Tile('image_plant', 0, 5, 0)
        Tile('image_seaweed', 127, 107, 0)
        Tile('image_house', 10, 320, 0)
        Tile('image_tree', 170, 440, 0)
        Tile('image_swamp', 540, 90, 0)
        Tile('image_big_tree', 570, 500, 0)

    def load_image(self, name, colorkey=None):
        image = pygame.image.load(name)
        return image

    def load_level(self, filename):
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, sr):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        if sr == 1:
            self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        else:
            self.rect = self.rect.move(pos_x, pos_y)
        if 'path' in tile_type or 'zhuk' in tile_type or 'sprike' in tile_type or tile_type == 'target':
            mozhno_group.add(all_sprites.sprites()[-1])
        else:
            nelzay_group.add(all_sprites.sprites()[-1])


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_height)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move_right(self):
        #if not pygame.sprite.spritecollide(player, nelzay_group, False):
            self.rect.x += 45
        #else:
            #self.rect.x += 45
            #check = False
            #for i in pygame.sprite.spritecollide(player, nelzay_group, False):
                #rect_player = player.image.get_rect()
                #rect_sprite = i.image.get_rect()
                #if rect_player.midtop[1] > rect_sprite.midtop[1]:
                    #print("top")
                #elif rect_player.midleft[0] > rect_sprite.midleft[0]:
                    #print("left")
                #if rect_player.midright[0] >= rect_sprite.midright[0]:
                    #print(rect_player.midright[0], rect_sprite.midright[0])
                    #check = True
                    #break
                #else:
                    #print(rect_player.midright[0], rect_sprite.midright[0])
                    #check = False
            #if check is False:
                #self.rect.x += 45


    def move_left(self):
        #if not pygame.sprite.spritecollide(player, nelzay_group, False):
            self.rect.x -= 45

    def move_up(self):
        #if not pygame.sprite.spritecollide(player, nelzay_group, False):
            self.rect.y += 45

    def move_down(self):
        #if not pygame.sprite.spritecollide(player, nelzay_group, False):
            self.rect.y -= 45


#class AnimatedSprite(pygame.sprite.Sprite):
    #def __init__(self, sheet, columns, rows, x, y):
        #super().__init__(all_sprites)
        #self.frames = []
        #self.cut_sheet(sheet, columns, rows)
        #self.cur_frame = 0
        #self.image = self.frames[self.cur_frame]
        #self.rect = self.rect.move(x, y)

    #def cut_sheet(self, sheet, columns, rows):
        #self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                #sheet.get_height() // rows)
        #for j in range(rows):
            #for i in range(columns):
                #frame_location = (self.rect.w * i, self.rect.h * j)
                #self.frames.append(sheet.subsurface(pygame.Rect(
                    #frame_location, self.rect.size)))

    #def update(self):
        #self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        #self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    mozhno_group = pygame.sprite.Group()
    nelzay_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = None
    FPS = 20
    clock = pygame.time.Clock()
    pygame.display.set_icon(LevelFirst().load_image("icon.png"))
    pygame.display.set_caption('shrek swamp')
    size = width, height = 675, 675
    screen = pygame.display.set_mode(size)
    tile_images = {
        'path_round_left_up': LevelFirst().load_image('path1.png'),
        'river': LevelFirst().load_image('swamp1.png'),
        'sprike_down': LevelFirst().load_image('sprike1.png'),
        'zhuk': LevelFirst().load_image('zhuk.png'),
        'path_round_right_up': LevelFirst().load_image('path4.png'),
        'swamp': LevelFirst().load_image('swamp3.png'),
        'swamp2': LevelFirst().load_image('swamp4.png'),
        'grass': LevelFirst().load_image('grass.png'),
        'path_round_left_down': LevelFirst().load_image('path2.png'),
        'path_round_right_down': LevelFirst().load_image('path3.png'),
        'path_center': LevelFirst().load_image('path5.png'),
        'path_gor': LevelFirst().load_image('path_gor.png'),
        'path_vert': LevelFirst().load_image('path_vert.png'),
        'path_str_up': LevelFirst().load_image('path6.png'),
        'path_str_left': LevelFirst().load_image('path7.png'),
        'path_str_down': LevelFirst().load_image('path8.png'),
        'path_str_right': LevelFirst().load_image('path9.png'),
        'zhuk_str_right': LevelFirst().load_image('zhuk_right.png'),
        'zhuk_str_down': LevelFirst().load_image('zhuk_down.png'),
        'zhuk_str_left': LevelFirst().load_image('zhuk_left.png'),
        'zhuk_str_up': LevelFirst().load_image('zhuk_up.png'),
        'zhuk_round_right': LevelFirst().load_image('zhuk_round_right.png'),
        'zhuk_round_right2': LevelFirst().load_image('zhuk_round_right2.png'),
        'zhuk_round_left2': LevelFirst().load_image('zhuk_round_left2.png'),
        'zhuk_round_left': LevelFirst().load_image('zhuk_round_left.png'),
        'target': LevelFirst().load_image('target.png'),
        'image_plant': LevelFirst().load_image("plant.png"),
        'image_seaweed': LevelFirst().load_image("seaweed.png"),
        'image_wood': LevelFirst().load_image("wood.png"),
        'image_tree': LevelFirst().load_image("tree.png"),
        'image_swamp': LevelFirst().load_image("swamp5.png"),
        'image_big_tree': LevelFirst().load_image("tree2.png"),
        'image_house': LevelFirst().load_image("house.png"),
        'image_grass': LevelFirst().load_image("grass2.png")
    }
    player_image = LevelFirst().load_image("shrek_idet.png")
    tile_width = tile_height = 45
    player, level_x, level_y = LevelFirst().generate_level(LevelFirst().load_level('level 1.0.txt'))
    LevelFirst().decor()
    #dragon =
    running = True
    while running:
        clock.tick(FPS)
        #all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_idet.png"), 6, 1, x, y)
                    s = 0
                    #spritemove = True
                    while s < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                    player.move_right()
                if event.key == pygame.K_LEFT:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_idet2.png"), 6, 1, x, y)
                    s = 0
                    while s < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                    player.move_left()
                if event.key == pygame.K_UP:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_up.png"), 1, 1, x, y)
                    s = 0
                    while s < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                    player.move_down()
                if event.key == pygame.K_DOWN:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_down.png"), 1, 1, x, y)
                    s = 0
                    while s < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                    player.move_up()
        all_sprites.draw(screen)
        player_group.draw(screen)
        #tiles_group.draw(screen)
        pygame.display.flip()
    pygame.quit()


