import pygame
import sys
import pyautogui
import os.path

from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle
from pygame import font
from random import randint

pygame.init()

# By Cl0ud

# SETUP SETTINGS
FPS = 60
MONITOR_WIDTH, MONITOR_HEIGHT = pyautogui.size()

DISPLAY_WIDTH = MONITOR_WIDTH
DISPLAY_HEIGHT = MONITOR_HEIGHT

percentage = 0

# GAME GLOBAL VARIABLES
isRunning = True
timer = 0
score = 0
click_damage = 1
game_paused = False
pos = [0, 0]  # MOUSE POSITION
mouse_click = False
enemies_killed = 1

chain_stacks = 0
drain_stacks = 0
defense_stacks = 0
execute_stacks = 0
luck_stacks = 0

# PLAYER STATUS VARIABLES

money = 0
cpu_level = 0
anti_virus_level = 0
ssd_level = 0
hd_level = 0
ram_level = 0

player_variables = []

file_check = os.path.exists('player_status.txt')

# Check da existência do txt que armazena os dados do jogador
# caso o txt não exista, um será criado
if not file_check:
    with open('player_status.txt', 'w') as file:
        file.write('money\n')
        file.write('0\n')
        file.write('cpu_level\n')
        file.write('0\n')
        file.write('anti_virus_level\n')
        file.write('0\n')
        file.write('ssd_level\n')
        file.write('0\n')
        file.write('hd_level\n')
        file.write('0\n')
        file.write('ram_level\n')
        file.write('0\n')


# Carrega os dados do jogador, lê o arquivo insere em uma lista
# cada índice da lista representa um atributo dentro do jogo
# como dinheiro e os niveis dos itens comprados pelo jogador
def load_variables():
    global money, cpu_level, anti_virus_level, ssd_level, hd_level, ram_level, player_variables

    with open('player_status.txt', 'r') as file:
        player_variables = file.read().split()

    money = int(player_variables[1])
    cpu_level = int(player_variables[3])
    anti_virus_level = int(player_variables[5])
    ssd_level = int(player_variables[7])
    hd_level = int(player_variables[9])
    ram_level = int(player_variables[11])

load_variables()

def show_variables():
    print('CPU LEVEL {}, VIDA {}'.format(cpu_level, cpu.MAX_HP + cpu_level))
    print('RAM LEVEL {}, DANO {}'.format(ram_level, click_damage + ram_level * 2))
    print('SSD LEVEL {}, DANO EM % DA VIDA MÁXIMA {}'.format(ssd_level, 2.5 * ssd_level))
    print('HD LEVEL {}, LENTIDÃO {}'.format(hd_level, 0.15 * hd_level))
    print('SCANNER LEVEL {}, DANO DO SCANNER {}'.format(anti_virus_level, 2.5 + 0.5 * anti_virus_level))

# Sobreecresve dados no save do jogador, esse método pede
# a linha que será alterada e o novo valor a ser adicionado
# nessa nova linha

def save_variables():
    with open('player_status.txt', 'w') as file:
        list_size = range(len(player_variables))
        for word in list_size:
            if word == 1:
                file.write(str(money))
                file.write('\n')
            elif word == 3:
                file.write(str(cpu_level))
                file.write('\n')
            elif word == 5:
                file.write(str(anti_virus_level))
                file.write('\n')
            elif word == 7:
                file.write(str(ssd_level))
                file.write('\n')
            elif word == 9:
                file.write(str(hd_level))
                file.write('\n')
            elif word == 11:
                file.write(str(ram_level))
                file.write('\n')
            else:
                file.write(player_variables[word])
                file.write('\n')


# IMPORTAÇÃO DOS ARQUVOS UTILIZADOS NO JOGO

# SETUP
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

# FONTS CONFIG
DEFAULT_FONT = font.Font('Fonts/game_over.ttf', 120)
PERCENTAGE_FONT = font.Font('Fonts/game_over.ttf', 90)
HEALTH_FONT = font.Font('Fonts/game_over.ttf', 60)
TITLE_FONT = font.Font('Fonts/game_over.ttf', 200)

# SOUNDS
click_sound = pygame.mixer.Sound('Sounds/click_sound.wav')
click_sound.set_volume(1)

# MUSICS
current_song = 'Sounds/Menu CPU - Final.mp3'
pygame.mixer.music.load(current_song)
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

# SPRITES
normal_sprites = [load('Images/normal_vertical_1.png'), load('Images/normal_vertical_2.png'),
                  load('Images/normal_horizontal_1.png'), load('Images/normal_horizontal_2.png'),
                  load('Images/normal_diagonal_1.png'), load('Images/normal_diagonal_2.png')]

for i in range(len(normal_sprites)):
    normal_sprites[i] = pygame.transform.scale2x(normal_sprites[i].convert_alpha())


fast_sprites = [load('Images/rapido_vertical_1.png'), load('Images/rapido_vertical_2.png'),
                  load('Images/rapido_horizontal_1.png'), load('Images/rapido_horizontal_2.png'),
                  load('Images/rapido_diagonal_1.png'), load('Images/rapido_diagonal_2.png')]

for i in range(len(fast_sprites)):
    fast_sprites[i] = pygame.transform.scale2x(fast_sprites[i].convert_alpha())


child_sprites = [load('Images/filho_1.png'), load('Images/filho_2.png')]

for i in range(len(child_sprites)):
    child_sprites[i] = pygame.transform.scale2x(child_sprites[i].convert_alpha())


worm_sprites = [load('Images/worm_1.png'), load('Images/worm_2.png')]

for i in range(len(worm_sprites)):
    worm_sprites[i] = pygame.transform.scale2x(worm_sprites[i].convert_alpha())


worm_virus = load('Images/virus_worm.png').convert_alpha()
cpu_good = load('Images/CPU.png').convert_alpha()
cpu_bad = load('Images/CPU 2.png').convert_alpha()
cpu_hurt = load('Images/CPU 3.png').convert_alpha()

mouse_image = load('Images/mouse_image.png').convert_alpha()
mouse_image2 = load('Images/mouse_image2.png').convert_alpha()

cpu_good = pygame.transform.scale(cpu_good, (96, 96))
cpu_bad = pygame.transform.scale(cpu_bad, (96, 96))
cpu_hurt = pygame.transform.scale(cpu_hurt, (96, 96))

scanner = load('Images/scanner.png').convert_alpha()
scanner_coll = load('Images/scanner_coll.png').convert_alpha()

heal_item = load('Images/heal_item.png').convert_alpha()
health_item = load('Images/health_item.png').convert_alpha()
damage_item = load('Images/damage_item.png').convert_alpha()
chain_item = load('Images/chain_item.png').convert_alpha()
drain_item = load('Images/drain_item.png').convert_alpha()
defense_item = load('Images/defense_item.png').convert_alpha()
execute_item = load('Images/guillotine_item.png').convert_alpha()
luck_item = load('Images/luck_item.png').convert_alpha()

btn_start = load('Images/btn_play2.png').convert_alpha()
btn_exit = load('Images/btn_exit.png').convert_alpha()
btn_shop = load('Images/btn_shop.png').convert_alpha()
btn_main = load('Images/btn_mainmenu.png').convert_alpha()
btn_resume = load('Images/btn_resume.png').convert_alpha()
btn_reset = load('Images/btn_reset.png').convert_alpha()
btn_credits = load('Images/btn_credits.png').convert_alpha()
btn_htplay = load('Images/btn_howtoplay.png').convert_alpha()
btn_back = load('Images/btn_back.png').convert_alpha()
btn_upgrade = load('Images/btn_upgrade.png').convert_alpha()
btn_maximized = load('Images/btn_maximized.png').convert_alpha()

# BACKGROUND
bg_jogo1 = load('Images/bg_jogo1.png').convert()
bg_jogo1 = pygame.transform.scale(bg_jogo1, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_jogo2 = load('Images/bg_jogo2.png').convert()
bg_jogo2 = pygame.transform.scale(bg_jogo2, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


pause_bg = load('Images/pause_bg.png').convert_alpha()
pause = pygame.transform.scale(pause_bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

htplay = pygame.transform.scale(load('Images/htplay.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
htplay2 = pygame.transform.scale(load('Images/htplay2.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
htplay3 = pygame.transform.scale(load('Images/htplay3.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
htplay4 = pygame.transform.scale(load('Images/htplay4.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
htplay5 = pygame.transform.scale(load('Images/htplay5.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
htplay6 = pygame.transform.scale(load('Images/htplay6.png').convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))


shop_bg = load('Images/shop_bg.png').convert()
shop_bg = pygame.transform.scale(shop_bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

mainmenu_background = load('Images/Fundo.png')
mainmenu_background = pygame.transform.scale(mainmenu_background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


# DIVERSAS CLASSES UTILIZADAS PARA CRIAR UM PADRÃO E PODE UTILIZAR DA ORIENTAÇÃO A OBJETOS
# A CLASSE SPRITE JÁ VEM POR PADRÃO COM VARIÁVEIS E METODOS PRÓPRIOS QUE AJUDAM NA CRIAÇÃO
# DE INIMIGOS, BOTÕES, PLAYER
class CPU(Sprite):

    damage_invulnerability = 0
    hurt_image = 0
    timer = 0
    last_life = 0

    def __init__(self):
        super().__init__()
        self.image = cpu_good
        width = self.image.get_width()
        height = self.image.get_height()
        self.MAX_HP = 3 + cpu_level
        self.HP = self.MAX_HP
        self.damage_invulnerability = 0
        self.hurt_image = 0
        self.timer = 0
        self.image = cpu_good
        self.rect = self.image.get_rect(center=(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))
        self.last_life = self.MAX_HP

    def update(self):
        global defense_stacks, FPS, drain_stacks, timer
        self.cpu_animation()

        if self.HP > self.last_life and self.HP - self.last_life > 1 or (self.HP - self.last_life > 0.1 and timer % 120 == 0):
            Text_Group.add(
                Text('+{:.2f}'.format(self.HP - self.last_life),
                     (0, 255, 0), 100, 2,
                     [self.rect.centerx,
                      self.rect.centery], 0))
            self.last_life = self.HP

        if self.HP != self.last_life:
            self.last_life = self.HP

        if self.hurt_image > 0:
            self.hurt_image -= 1 / FPS
        if self.damage_invulnerability > 0:
            self.damage_invulnerability -= 1 / FPS

        if pygame.sprite.groupcollide(Cpu_Group, Virus_Group, False, True):
            self.got_hit()

        if self.HP > self.MAX_HP:
            self.HP = self.MAX_HP
        if drain_stacks > 0 and len(Virus_Group) > 0:
            self.drain_effect()

        if defense_stacks > 0:
            self.emergency_defense()

    def emergency_defense(self):
        global timer
        # self.timer recebe o valor de 0,16 por tick mais a vida máxima excedente de 3
        self.timer += (1 + (self.MAX_HP - 3) / 6) / FPS

        if self.HP < self.MAX_HP:
            # cura a cpu com base na vida perdida multiplicado pelos perks
            if (self.MAX_HP - self.HP) * (0.005 * defense_stacks) < 0.15:
                self.HP += (self.MAX_HP - self.HP) * (0.005 * defense_stacks) / FPS
            else:
                self.HP += 0.15 / FPS
            # print('Curado em {}'.format((self.MAX_HP - self.HP) * (0.005 + defense_stacks * 0.001)/ FPS))

        # quando self.timer for maior que 1 e a vida for menor ou igual a vida máxima ou tiverem mais de 6 inimigos
        # a cpu irá atirar, ela também atirará nos primeiros 15 segundos de partida
        if self.timer >= 3 and (self.HP <= self.MAX_HP / 2 or len(Virus_Group) >= 5 or self.HP < 5 or timer < 900):
            self.timer = 0
            if len(Virus_Group) > 0:
                for i in range(1 + int((self.MAX_HP - 3) / 6)):
                    random = randint(0, len(Virus_Group) - 1)
                    thunder(self.rect.center, Virus_Group.sprites()[random].rect.center, (255, 255, 0), 6)
                    Virus_Group.sprites()[random].life -= defense_stacks + self.MAX_HP + (
                            Virus_Group.sprites()[random].max_life - Virus_Group.sprites()[random].life) / 6
                    Text_Group.add(
                        Text('{:.1f}'.format(
                            (defense_stacks + self.MAX_HP + (
                            Virus_Group.sprites()[random].max_life - Virus_Group.sprites()[random].life) / 6)),
                            (55, 255, 20), 50, 0.6,
                            [Virus_Group.sprites()[random].rect.centerx, Virus_Group.sprites()[random].rect.centery], 1))

    def drain_effect(self):
        global drain_stacks, click_damage, timer

        if self.HP < self.MAX_HP:
            if (self.MAX_HP * 0.001 * len(Virus_Group))  < 0.15:
                self.HP += (self.MAX_HP * 0.001 * len(Virus_Group)) / FPS
            else:
                self.HP += 0.15 / FPS
        for enemy in Virus_Group:
            # causa dano com base na quantidade de perks e com base na vida perdida também com base no número de perks
            enemy.life -= (0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks)) / FPS
            if timer % 30 == 0:
                if len(str(0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks) / FPS)) == 4:
                    Text_Group.add(
                        Text('{:.3f}'.format(
                             (0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks)) / FPS),
                             (255, 127, 127), 40, 0.5,
                             [enemy.rect.centerx, enemy.rect.centery], 1))
                elif len(str(0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks) / FPS)) == 3:
                    Text_Group.add(
                        Text('{:.2f}'.format(
                             (0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks)) / FPS),
                             (255, 127, 127), 40, 0.5,
                             [enemy.rect.centerx, enemy.rect.centery], 1))
                else:
                    Text_Group.add(
                        Text('{:.2f}'.format(
                            (0.5 * drain_stacks + (enemy.max_life - enemy.life) * (0.009 * drain_stacks)) / FPS),
                            (255, 127, 127), 40, 0.5,
                            [enemy.rect.centerx, enemy.rect.centery], 1))

    def got_hit(self):
        if self.damage_invulnerability <= 0:
            self.HP -= 1
            self.damage_invulnerability = 0.10
            self.hurt_image = 0.65

    def cpu_animation(self):
        if self.HP >= (self.MAX_HP / 2) and self.hurt_image <= 0:
            self.image = cpu_good
        elif self.HP < (self.MAX_HP / 2) and self.hurt_image <= 0:
            self.image = cpu_bad
        if self.hurt_image > 0:
            self.image = cpu_hurt


class Item(Sprite):
    type = None
    movement = True
    timer = 0
    luck_pick = 0

    def __init__(self, perk):
        super().__init__()
        if not perk:
            if randint(0, 9) < 8:
                x = randint(0, 2)
                if x == 0:
                    self.type = 'Health'
                    self.image = health_item
                elif x == 1:
                    self.type = 'Damage'
                    self.image = damage_item
                else:
                    if randint(0, 2) == 0:
                        self.type = 'Heal'
                        self.image = heal_item
                    else:
                        self.type = 'Damage'
                        self.image = damage_item
            else:
                x = randint(0, 4)
                if x == 0:
                    self.type = 'Chain'
                    self.image = pygame.transform.scale(chain_item, (chain_item.get_width() / 3,
                                                                     chain_item.get_height() / 3))
                elif x == 1:
                    self.type = 'Drain'
                    self.image = drain_item
                elif x == 2:
                    self.type = 'Defense'
                    self.image = pygame.transform.scale(defense_item, (defense_item.get_width() / 3,
                                                                       defense_item.get_height() / 3))
                elif x == 3 and execute_stacks < 5:
                    self.type = 'Execute'
                    self.image = execute_item
                elif x == 4:
                    self.type = 'Luck'
                    self.image = luck_item
                else:
                    self.type = 'Drain'
                    self.image = drain_item
        else:
            x = randint(0, 4)
            if x == 0:
                self.type = 'Chain'
                self.image = pygame.transform.scale(chain_item, (chain_item.get_width() / 3,
                                                                 chain_item.get_height() / 3))
            elif x == 1:
                self.type = 'Drain'
                self.image = drain_item
            elif x == 2:
                self.type = 'Defense'
                self.image = pygame.transform.scale(defense_item, (defense_item.get_width() / 3,
                                                                   defense_item.get_height() / 3))
            elif x == 3 and execute_stacks < 5:
                self.type = 'Execute'
                self.image = execute_item
            elif x == 4:
                self.type = 'Luck'
                self.image = luck_item
            else:
                self.type = 'Drain'
                self.image = drain_item

        self.rect = self.image.get_rect()
        if self.type != 'Chain' and self.type != 'Defense':
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, DISPLAY_WIDTH - self.image.get_width())
        self.rect.y = randint(0, DISPLAY_HEIGHT - self.image.get_height())

    def update(self):
        global pos, mouse_click, luck_stacks

        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            mouse_click = True
            if self.type == 'Heal' and cpu.HP < cpu.MAX_HP:
                self.kill()
            elif self.type != 'Heal':
                Text_Group.add(
                    Text('ITEM COLETADO!',
                         (0, 255, 0), 60, 2,
                         [self.rect.centerx, self.rect.centery], 0))
                self.kill()

        if luck_stacks <= 9:
            if self.luck_pick >= 5 - luck_stacks * 0.5:
                if self.rect.centerx > DISPLAY_HEIGHT / 2:
                    speed = -2
                else:
                    speed = 2
                if self.type != 'Heal':
                    Text_Group.add(
                        Text('COLETADO!',
                            (0, 255, 0), 60, 2,
                            [self.rect.centerx, self.rect.centery], 0))
                    self.kill()
        elif self.luck_pick >= 0.5:
            speed = 0
            if self.rect.centerx > DISPLAY_HEIGHT / 2:
                speed = -2
            else:
                speed = 2
            if self.type != 'Heal':
                Text_Group.add(
                    Text('COLETADO!',
                        (0, 255, 0), 60, 2,
                        [self.rect.centerx, self.rect.centery], 0))
                self.kill()

        if luck_stacks > 0:
            self.luck_pick += 1 / FPS
        self.timer += 1 / FPS

        if self.timer > 0.2:
            self.timer = 0
            self.movement = not self.movement

        if self.timer >= 0.1:
            if self.movement:
                self.rect.y += 1
            else:
                self.rect.y -= 1

    def kill(self):
        self.item_picked()
        Sprite.kill(self)

    def item_picked(self):
        global click_damage, chain_stacks, drain_stacks, defense_stacks, execute_stacks, luck_stacks
        if self.type == 'Heal':
            if cpu.HP < cpu.MAX_HP:
                cpu.HP += 1 + (cpu.MAX_HP - cpu.HP) / 3
        elif self.type == 'Health':
            cpu.MAX_HP += 1
            cpu.HP += 1
        elif self.type == 'Damage':
            click_damage = (click_damage + 0.50) * 1.10
            #print('Damage {}'.format(click_damage))
        elif self.type == 'Chain':
            chain_stacks += 1
        elif self.type == 'Drain':
            drain_stacks += 1
        elif self.type == 'Defense':
            defense_stacks += 1
        elif self.type == 'Execute':
            execute_stacks += 1
        elif self.type == 'Luck':
            luck_stacks += 1


class Button(Sprite):
    width = 0
    height = 0
    scale = 1
    scene = ''
    original_image = None

    def __init__(self, x, y, image, scale, scene):
        super().__init__()
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.scene = scene
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        global money

        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (int(self.width * 1.05), int(self.height * 1.05)))
        else:
            self.image = self.original_image
        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            if self.scene == 'main game' and Game_state.game_state != 'pause' or self.scene == 'reset':
                Game_state.reset = 0
            if self.scene == 'reset':
                # BOTÃO METODOS
                Game_state.reset = 0
                Game_state.game_state = 'main game'
            else:
                Game_state.game_state = self.scene
                if self.scene == 'resume':
                    pygame.mixer.music.unpause()


class Game_State:
    i = 0
    images_htplay = [htplay, htplay2, htplay6, htplay3, htplay4, htplay5]
    index = 0

    def __init__(self):
        self.game_state = 'main menu'
        self.reset = 0
        self.randPos = 0
        self.randX = 0
        self.randY = 0
        self.image_change = True

    def main_game(self):
        global timer, score, money, enemies_killed, click_damage, chain_stacks, drain_stacks, execute_stacks, percentage, current_song

        save_variables()

        if current_song != 'Sounds/Up and Down - Final.mp3':
            current_song = 'Sounds/Up and Down - Final.mp3'
            pygame.mixer.music.unload()
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)


        percentage = (score * 100) / 8000000

        if timer % 30 == 0:
            self.image_change = not self.image_change

        if self.image_change:
            display.blit(bg_jogo1, (0, 0))
        else:
            display.blit(bg_jogo2, (0, 0))

        if (50 - int(timer/1800) * 10) > 0:
            spawning_time = 25 + (50 - int(timer/1800) * 10)
        else:
            spawning_time = 25

        if cpu.HP <= 0 or percentage >= 100:
            Game_state.game_state = 'pause'

        if luck_stacks > 1 and cpu.HP >= cpu.MAX_HP:
            if enemies_killed % 16 == 0:
                Item_Group.add(Item(False))
                enemies_killed -= 15
        else:
            if enemies_killed % 21 == 0:
                Item_Group.add(Item(False))
                enemies_killed -= 15

        if self.reset == 0:  # RESETAR PARTIDA E VARIAVEIS
            self.reset_game()
        timer += 1

        #print(spawning_time)
        if timer % 600 == 0:
            if self.randPos == 0:
                Virus_Group.add(Enemy(Worms_Model,
                                      randint(0, DISPLAY_WIDTH),
                                      self.randY * DISPLAY_HEIGHT, 'Mother'))

            else:
                Virus_Group.add(Enemy(Worms_Model,
                                      (randint(0, DISPLAY_WIDTH)),
                                      self.randY * DISPLAY_HEIGHT, 'Mother'))

        if timer % spawning_time == 0:
            self.randPos = randint(0, 1)
            self.randX = randint(0, 1)
            self.randY = randint(0, 1)

            if self.randPos == 0:
                if randint(0, 5) == 0:
                    Virus_Group.add(Enemy(Fast_Virus_Model,
                                          (randint(0, DISPLAY_WIDTH)),
                                          self.randY * DISPLAY_HEIGHT, 'Fast'))
                else:
                    Virus_Group.add(Enemy(Virus_Model,
                                          (randint(0, DISPLAY_WIDTH)),
                                          self.randY * DISPLAY_HEIGHT, 'Normal'))

            else:
                if randint(0, 5) == 0:
                    Virus_Group.add(Enemy(Fast_Virus_Model,
                                          (self.randX * DISPLAY_WIDTH),
                                          (randint(0, DISPLAY_HEIGHT)), 'Fast'))
                else:
                    Virus_Group.add(Enemy(Virus_Model,
                                          (self.randX * DISPLAY_WIDTH),
                                          (randint(0, DISPLAY_HEIGHT)), 'Normal'))

        Cpu_Group.update()
        Cpu_Group.draw(display)

        display.blit(pygame.transform.scale2x(cpu.image), (-36, DISPLAY_HEIGHT - cpu.image.get_height() * 2 + 30))

        Scanner_Group.update()
        Scanner_Group.draw(display)

        Virus_Group.update()
        Virus_Group.draw(display)

        Worms_Group.update()
        Worms_Group.draw(display)

        Item_Group.update()
        Item_Group.draw(display)

        Text_Group.update()

        # DISPLAYS
        score_display = DEFAULT_FONT.render(
            f'Pontuacao:{int(score)}',
            True,
            (255, 255, 255)
        )

        display.blit(score_display, (118, DISPLAY_HEIGHT - score_display.get_rect().bottom))

        percentage_display = PERCENTAGE_FONT.render(
            f'PORCENTAGEM DE ARQUIVOS VERIFICADOS: {percentage:.2f}%',
            True,
            (255, 255, 255)
        )

        display.blit(percentage_display, (0, 0))

        hp_display = DEFAULT_FONT.render(
            f'Saude da CPU:{"{:.1f}".format(cpu.HP)}/{int(cpu.MAX_HP)}',
            True,
            (255, 255, 255)
        )
        display.blit(hp_display, (118, DISPLAY_HEIGHT - hp_display.get_rect().bottom - 50))

    def reset_game(self):
        global score, enemies_killed, click_damage, drain_stacks, chain_stacks, defense_stacks, money, execute_stacks, timer, drain_stacks, luck_stacks, current_song
        self.reset += 1
        #show_variables()

        pygame.mixer.music.rewind()

        timer = 0
        score = 0
        Virus_Group.empty()
        Worms_Group.empty()
        Scanner_Group.empty()
        Text_Group.empty()
        Item_Group.empty()
        Item_Group.add(Item(True))
        if anti_virus_level > 0:
            Scanner_Group.add(Scanner())

        enemies_killed = 1
        click_damage = 1 + ram_level * 3.5
        cpu.MAX_HP = 3 + cpu_level * 1
        cpu.HP = cpu.MAX_HP

        chain_stacks = 0
        drain_stacks = 0
        defense_stacks = 0
        execute_stacks = 0
        luck_stacks = 0

        self.game_state = 'main game'

    def main_menu(self):
        global money, current_song
        # display.blit(mainmenu_background, (0, 0))

        display.fill((255, 248, 220))

        title_display = TITLE_FONT.render(
            f'CPU - CENTRAL DE PANICO URGENTE',
            True,
            (0, 0, 0)
        )
        display.blit(title_display, (DISPLAY_WIDTH / 2 - title_display.get_width() / 2, -10))
        display.blit(mainmenu_background, (0, 0))

        if current_song != 'Sounds/Menu CPU - Final.mp3':
            current_song = 'Sounds/Menu CPU - Final.mp3'
            pygame.mixer.music.unload()
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)

        Button_Group.draw(display)
        Button_Group.update()

    def exit(self):
        pygame.quit()
        sys.exit()

    def pause(self):
        # DISPLAYS

        # print('Base damage: {}'.format(click_damage))
        # print('Chain stacks: {}'.format(chain_stacks))
        # print('Drain stacks: {}'.format(drain_stacks))
        # print('\n\n\n\n\n\n')

        Status_Group.add(Status(damage_item, click_damage, (255, 255, 255), 140, -250, False))
        Status_Group.add(Status(health_item, cpu.MAX_HP, (255, 255, 255), 140, -200, False))
        Status_Group.add(Status(chain_item, chain_stacks, (255, 255, 255), 140, -130, True))
        Status_Group.add(Status(drain_item, drain_stacks, (255, 255, 255), 140, -70, False))
        Status_Group.add(Status(defense_item, defense_stacks, (255, 255, 255), 140, 0, True))
        Status_Group.add(Status(execute_item, execute_stacks, (255, 255, 255), 140, 75, False))
        Status_Group.add(Status(luck_item, luck_stacks, (255, 255, 255), 140, 150, False))

        display.blit(pygame.transform.scale2x(cpu.image), (-36, DISPLAY_HEIGHT - cpu.image.get_height() * 2 + 30))

        score_display = DEFAULT_FONT.render(
            f'Pontuacao:{int(score)}',
            True,
            (255, 255, 255)
        )

        display.blit(score_display, (118, DISPLAY_HEIGHT - score_display.get_rect().bottom))

        hp_display = DEFAULT_FONT.render(
            f'Saude da CPU:{"{:.1f}".format(cpu.HP)}/{int(cpu.MAX_HP)}',
            True,
            (255, 255, 255)
        )
        display.blit(hp_display, (118, DISPLAY_HEIGHT - hp_display.get_rect().bottom - 50))

        Cpu_Group.draw(display)
        Scanner_Group.draw(display)
        Virus_Group.draw(display)
        Worms_Group.draw(display)
        Item_Group.draw(display)
        Text_Group.update()

        display.blit(pause_bg, (0, 0))

        Status_Group.draw(display)
        Status_Group.update()
        Status_Group.empty()

        if percentage >= 100:
            pause_display = TITLE_FONT.render(
                f'O COMPUTADOR FOI LIMPO.',
                True,
                (0, 0, 0)
            )
        elif cpu.HP > 0:
            pause_display = TITLE_FONT.render(
                f'JOGO PAUSADO.',
                True,
                (0, 0, 0)
            )
        else:
            pause_display = TITLE_FONT.render(
                f'VOCE PERDEU.',
                True,
                (0, 0, 0)
            )

        display.blit(pause_display, (DISPLAY_WIDTH / 2 - pause_display.get_width() / 2, -10))

        Pause_Group.draw(display)
        Pause_Group.update()

    def htplay(self):

        display.blit(self.images_htplay[self.index], (0, 0))

        images_display = DEFAULT_FONT.render(
            f'{self.index + 1}/{len(self.images_htplay)} - USE AS SETAS DO TECLADO PARA MUDAR A IMAGEM',
            True,
            (255, 255, 255)
        )
        display.blit(images_display, (0, 0 - 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.index + 1 < len(self.images_htplay):
                        self.index += 1
                    else:
                        self.index = 0
                if event.key == pygame.K_LEFT:
                    if self.index - 1 >= 0:
                        self.index -= 1
                    else:
                        self.index = len(self.images_htplay) - 1

        HTPlay_Group.draw(display)
        HTPlay_Group.update()

    def shop(self):
        display.blit(shop_bg, (0, 0))

        money_display = DEFAULT_FONT.render(
            f'Dinheiro:{int(money)}',
            True,
            (255, 255, 255)
        )
        display.blit(money_display, (0 + 50, 0 + 120))

        Shop_Group.draw(display)
        Shop_Group.update()
        load_variables()


    def state_manager(self):
        global score
        if self.game_state == 'main game':

            self.main_game()
        elif self.game_state == 'main menu':
            self.main_menu()
        elif self.game_state == 'how to play':
            self.htplay()
        elif self.game_state == 'shop':
            self.shop()
        elif self.game_state == 'exit':
            self.exit()
        elif self.game_state == 'pause':
            self.pause()
        elif self.game_state == 'resume':
            if cpu.HP > 0:
                self.game_state = 'main game'
                self.main_game()
            else:
                self.game_state = 'pause'
                self.pause()


class Enemy(Sprite):

    def __init__(self, info, x, y, name):
        super().__init__()
        # ENEMY CLASS ATRIBUTES
        # ORDEM VIDA, GAP DE VIDA, MOV SPEED, MOV COOLDOWN, SCORE BASE, IMAGEM, ESCALA, TIPO

        self.type = info[7]
        self.id = randint(0, 99999999)
        self.name = name

        self.anim_timer = 0
        self.anim_num = 0
        self.time_alive = 0
        self.slow = 0
        self.spawn_timer = 0

        if self.type != 'Worm':
            if int(score / info[1]) <= 10000:
                self.max_life = info[0] + int(score / info[1])
            else:
                self.max_life = 10000
        else:
            if info[0] * (1 + int(score / info[1])) <= 8000:
                self.max_life = info[0] * (1 + int(score / info[1]))
            else:
                self.max_life = 12000

        self.life = self.max_life
        self.last_hit = self.max_life
        self.movement_speed = info[2]
        self.movement_speed_save = self.movement_speed
        self.speed_movement = info[3]
        self.movement_cooldown = self.speed_movement
        self.slow_speed = self.movement_speed * 0.50
        self.base_score = info[4]
        self.direction = [0, 0]

        # SPRITE CLASS ATRIBUTES

        self.image = info[5][0]
        self.sprites = info[5]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.click_check()
        self.check_life()

        if self.anim_timer < 0.25 :
            self.anim_timer += 1 / FPS
        else:
            self.anim_timer = 0
            if self.anim_num == 0:
                self.anim_num = 1
            else:
                self.anim_num = 0

        if self.name == 'Normal' or self.name == 'Fast':
            self.animation(self.sprites)
        else:
            self.image = self.sprites[0 + self.anim_num]


        if self.life > 0:
            self.display_health()

        if self.time_alive <= 4:
            self.time_alive += 1 / FPS

        if self.slow > 0:
            self.movement_speed = self.slow_speed
            self.slow -= 1 / FPS
        else:
            self.movement_speed = self.movement_speed_save

        if self.type != 'Worm':
            self.movement()
        elif self.rect.bottom > DISPLAY_HEIGHT or self.rect.right > DISPLAY_WIDTH or self.rect.top < 0 or self.rect.left < 0:
            self.movement()

        if self.type == 'Worm':
            self.spawn_timer -= 1 / FPS
            if self.spawn_timer <= 0:
                self.spawn_timer = 1.5
                Virus_Group.add(Enemy(Worms_Child_Model, self.rect.centerx, self.rect.centery, 'Child'))

        if self.life > 0:
            self.draw_life()

    def kill(self):
        global score, money, enemies_killed, chain_stacks, drain_stacks, luck_stacks
        enemies_killed += 1

        if self.type != 'Worm':
            score += (self.base_score * self.max_life) * ((8 - self.time_alive) / 8)
        else:
            score += (self.base_score * (self.max_life / 8)) * ((8 - self.time_alive) / 8)
            if randint(0, 2) > 0:
                Item_Group.add(Item(True))

        self.chain_effect()

        if luck_stacks > 0:
            x = randint(1, 100)
            if x <= luck_stacks:
                Text_Group.add(
                    Text('ITEM GERADO!',
                         (0, 255, 0), 80, 1.5,
                         [cpu.rect.centerx, cpu.rect.top], 0))
                Item_Group.add(Item(False))

        if self.name == 'Normal':
            money += 3
        elif self.name == 'Fast':
            money += 5
        elif self.name == 'Mother':
            money += 8
        elif self.name == 'Child':
            money += 1

        Sprite.kill(self)

    def display_health(self):
        hp_display = HEALTH_FONT.render(str('{:.1f}'.format(self.life)),
                                         True,
                                         (255, 255, 255)
                                         )
        display.blit(hp_display, (self.rect.centerx - hp_display.get_width() / 2, self.rect.y - hp_display.get_height()))

    def click_check(self):
        global pos, mouse_click
        # CALCULO DE DANO NO INIMGO AO CLICAR

        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            mouse_click = True
            self.life -= click_damage + (ssd_level * 0.05 * self.max_life)
            self.slow = hd_level * 0.20
            Text_Group.add(
                Text('{:.2f}'.format(click_damage + (ssd_level * 0.05 * self.max_life)),
                     (255, 255, 255), 65, 0.5,
                     [self.rect.centerx,
                      self.rect.centery], 0))

    def chain_effect(self):
        global click_damage
        max_chains = 0
        if len(Virus_Group) > 1 and chain_stacks > 0:
            if int(click_damage / 25) <= 3:
                max_chains = int(click_damage / 20)
            else:
                max_chains = 3

            #print(max_chains)
            for i in range(1 + randint(0, max_chains)):
                random = -1
                while random == -1 or Virus_Group.sprites()[random].id == self.id:
                    random = randint(0, len(Virus_Group) - 1)

                if len(Virus_Group) >= random:
                    Virus_Group.sprites()[random].life -= (click_damage / 3 + Virus_Group.sprites()[random].max_life * (0.07 + 0.01 * chain_stacks))
                    # print('Default damage: {}'.format(click_damage * ((chain_stacks / 2))))
                    # print('Targe Life: {}, Extra Damage: {}'.format(Virus_Group.sprites()[random].max_life, Virus_Group.sprites()[random].max_life / 4))
                    # print('Boosted damage: {}'.format((click_damage * (chain_stacks / 2) + Virus_Group.sprites()[random].max_life * 0.25)))
                    thunder(self.rect.center, Virus_Group.sprites()[random].rect.center, (255, 255, 0), 6)
                    Text_Group.add(Text('{:.1f}'.format(click_damage / 3 + Virus_Group.sprites()[random].max_life * (0.07 + 0.01 * chain_stacks)),
                                        (255, 255, 0), 120, 0.8,
                                        [Virus_Group.sprites()[random].rect.centerx,
                                         Virus_Group.sprites()[random].rect.centery], 0))

    def check_life(self):
        global execute_stacks

        if self.life <= 0:
            self.kill()

        if 0.25 + self.max_life * (execute_stacks * 0.05) >= self.life > 0 and execute_stacks > 0:
            Text_Group.add(
                Text('DELETADO!',
                     (0, 0, 0), 80, 0.8,
                     [self.rect.centerx, self.rect.centery], 0))

            self.kill()

    def draw_life(self):
        pygame.draw.rect(display, (0, 0, 0),
                         (self.rect.centerx - self.image.get_width() / 2 - 2,
                          self.rect.y - 3,
                          (self.image.get_width() + 3),
                          9))
        pygame.draw.rect(display, (255, 0, 0),
                         (self.rect.centerx - (self.image.get_width() * ((self.life / self.max_life) / 2)),
                          self.rect.y - 1,
                          self.image.get_width() * (self.life / self.max_life),
                          5))

    def movement(self):
        global display

        cpu_pos = (display.get_width() / 2, display.get_height() / 2)

        if self.movement_cooldown <= 0:
            if abs(cpu_pos[0] - self.rect.centerx) > 15:
                if cpu_pos[0] > self.rect.centerx:
                    self.direction[0] = 1
                    self.rect.x += self.movement_speed
                else:
                    self.direction[0] = 2
                    self.rect.x -= self.movement_speed

            else:
                self.direction[0] = 0

            if abs(cpu_pos[1] - self.rect.centery) > 15:
                if cpu_pos[1] > self.rect.centery:
                    self.direction[1] = 1
                    self.rect.y += self.movement_speed * 0.5
                else:
                    self.direction[1] = 2
                    self.rect.y -= self.movement_speed * 0.5
            else:
                self.direction[1] = 0

            self.movement_cooldown = self.speed_movement
        else:
            self.movement_cooldown -= 1 / FPS

    def animation(self, sprites):

        ## direction 0  = 1 a esquerda
        ## direction 0  = 2 a direita
        ## direction 1  = 1 acima
        ## direction 1  = 2 abaixo

        if self.direction[0] != 0 and self.direction[1] != 0:
            if self.direction[0] == 1 and self.direction[1] == 2:
                self.image = self.sprites[4 + self.anim_num]
            elif self.direction[0] == 1 and self.direction[1] == 1:
                self.image = pygame.transform.flip(self.sprites[4 + self.anim_num], False, True)
            elif self.direction[0] == 2 and self.direction[1] == 2:
                self.image = pygame.transform.flip(self.sprites[4 + self.anim_num], True, False)
            elif self.direction[0] == 2 and self.direction[1] == 1:
                self.image = pygame.transform.flip(self.sprites[4 + self.anim_num], True, True)
        else:
            if self.direction[0] == 0:
                if self.direction[1] == 1:
                    self.image = pygame.transform.flip(self.sprites[0 + self.anim_num], False, True)
                else:
                    self.image = self.sprites[0 + self.anim_num]
            else:
                if self.direction[0] == 1:
                    self.image = self.sprites[2 + self.anim_num]
                else:
                    self.image = pygame.transform.flip(self.sprites[2 + self.anim_num], True, False)


class Scanner(Sprite):
    direction = 1
    mov_speed = 26
    mov_speed_save = mov_speed
    collision = 0

    cooldown = 0
    size = 12

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(scanner, (self.size, DISPLAY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0

    def update(self):
        global timer

        self.movement()
        if self.collision > 0:
            self.image = self.image = pygame.transform.scale(scanner_coll, (self.size, DISPLAY_HEIGHT))
            self.mov_speed = self.mov_speed_save / 8
            self.collision -= 1 / FPS
        else:
            if self.cooldown <= 0:
                self.image = pygame.transform.scale(scanner, (self.size, DISPLAY_HEIGHT))
                self.mov_speed = self.mov_speed_save

        if self.cooldown > 0:
            self.cooldown -= 1 / FPS
            self.mov_speed = 0

        for enemy in Virus_Group:
            if self.rect.colliderect(enemy.rect) and self.cooldown <= 0:
                self.damage_effect(enemy)
                enemy.life -= (click_damage * (2.5 + (anti_virus_level * 0.5)) + (0.05 * ssd_level * enemy.max_life)) / FPS
                enemy.slow = hd_level * 0.20
                self.collision = 0.05
                if timer % 5 == 0:
                    Text_Group.add(Text(
                        '{:.2f}'.format((click_damage * (2.5 + (anti_virus_level * 0.5)) + (0.05 * ssd_level * enemy.max_life)) / FPS),
                        (255, 0, 0), 30, 0.4,
                        [enemy.rect.centerx,
                         enemy.rect.centery], 0))

    def random_color(self):
        return (randint(100, 255), randint(100, 255), randint(100, 255))

    def random_width(self):
        return (randint(3, 9))

    def damage_effect(self, enemy):
        thunder((self.rect.centerx, enemy.rect.centery + randint(10, 100)), enemy.rect.center, self.random_color(), 6)
        thunder((self.rect.centerx, enemy.rect.centery), enemy.rect.center, (255, 255, 0), 6)
        thunder((self.rect.centerx, enemy.rect.centery - randint(10, 100)), enemy.rect.center, self.random_color(), 6)

    def movement(self):
        if self.direction == 1:
            self.rect.x += self.mov_speed
            if self.rect.x > DISPLAY_WIDTH:
                self.direction = 0
                self.cooldown = 5 - anti_virus_level
        else:
            self.rect.x -= self.mov_speed
            if self.rect.x < 0:
                self.direction = 1
                self.cooldown = 5 - anti_virus_level


class Text(Sprite):
    time = 0
    total_time = 0
    text = ''
    color = ()
    font = None
    default_display = ''
    speed = 0
    pos = []

    def __init__(self, text, color, size, time, position, speed):
        super().__init__()
        self.image = None
        self.time = time
        self.total_time = self.time
        self.text = text
        self.color = color
        self.speed = speed
        self.font = pygame.font.Font('Fonts/game_over.ttf', size)
        self.pos = position
        self.pos[0] += randint(-60, 60)
        self.pos[1] += randint(-40, 40)
        self.default_display = self.font.render(str(self.text),
                                                True,
                                                color
                                                )

    def update(self):
        self.pos[1] -= self.speed

        self.default_display = self.font.render(str(self.text),
                                                True,
                                                self.color
                                                )

        display.blit(self.default_display, self.pos)
        self.time -= 1 / FPS

        if self.time <= 0:
            self.kill()


class Status(Sprite):
    text = ''
    color = ()
    font = None
    default_display = ''
    pos = [0, 0]

    def __init__(self, image, text, color, size, vposition, rescale):
        super().__init__()
        self.image = image
        if not rescale:
            self.image = pygame.transform.scale(image, (self.image.get_width() * 4, self.image.get_height() * 4))
        else:
            self.image = pygame.transform.scale(image, (self.image.get_width() / 3, self.image.get_height() / 3))
        self.rect = self.image.get_rect()
        self.pos = (DISPLAY_WIDTH / 2,  (DISPLAY_HEIGHT / 2 + vposition) - size / 2)
        self.rect.topleft = (self.pos[0] - self.image.get_width(), self.pos[1] + 15)
        self.text = text
        if type(text) == float:
            self.text = '{:.2f}'.format(text)

        self.color = color
        self.font = pygame.font.Font('Fonts/game_over.ttf', size)
        self.default_display = self.font.render(str(f':{self.text}'),
                                                True,
                                                color
                                                )

    def update(self):
        display.blit(self.default_display, self.pos)


class Shop_Button(Sprite):
    level = 0
    attribute = ''
    price = 0
    scale = 0
    above_text = ''
    below_text = ''
    description_text = ''
    above_font = pygame.font.Font('Fonts/game_over.ttf', 120)
    below_font = pygame.font.Font('Fonts/game_over.ttf', 60)
    description_font = pygame.font.Font('Fonts/game_over.ttf', 50)

    def __init__(self, x, y, attribute, price, scale):
        super().__init__()
        self.image = btn_upgrade
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.attribute = attribute
        self.price = price
        self.scale = scale

        if self.attribute == 'cpu':
            self.above_text = 'CPU'
            self.description_text = 'Aumenta a vida maxima'
        elif self.attribute == 'antivirus':
            self.above_text = 'ANTI-VIRUS'
            self.description_text = 'Um scanner horizontal vai te auxiliar a matar inimigos'
        elif self.attribute == 'ram':
            self.above_text = 'RAM'
            self.description_text = 'Aumenta o dano base do clique'
        elif self.attribute == 'ssd':
            self.above_text = 'SSD'
            self.description_text = 'Causa dano extra com base na vida maxima dos inimigos'
        elif self.attribute == 'hd':
            self.above_text = 'HD'
            self.description_text = 'Aplica lentidao ao causar dano'

        self.description_text_display = self.description_font.render(
            f'{self.description_text}',
            True,
            (255, 255, 255)
        )

    def update(self):
        global anti_virus_level, cpu_level, ram_level, hd_level, ssd_level, money

        if self.attribute == 'cpu':
            self.below_text = f'Nivel: {cpu_level} Preco: {self.price + (cpu_level * self.scale)}'
            self.level = cpu_level
        elif self.attribute == 'antivirus':
            self.below_text = f'Nivel: {anti_virus_level} Preco: {self.price + (anti_virus_level * self.scale)}'
            self.level = anti_virus_level
        elif self.attribute == 'ram':
            self.below_text = f'Nivel: {ram_level} Preco: {self.price + (ram_level * self.scale)}'
            self.level = ram_level
        elif self.attribute == 'ssd':
            self.below_text = f'Nivel: {ssd_level} Preco: {self.price + (ssd_level * self.scale)}'
            self.level = ssd_level
        elif self.attribute == 'hd':
            self.below_text = f'Nivel: {hd_level} Preco: {self.price + (hd_level * self.scale)}'
            self.level = hd_level

        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0] and self.level < 5:
            if money >= self.price + self.level * self.scale:
                if self.attribute == 'ram':
                    ram_level += 1
                elif self.attribute == 'cpu':
                    cpu_level += 1
                    print(cpu_level)
                elif self.attribute == 'antivirus':
                    anti_virus_level += 1
                elif self.attribute == 'hd':
                    hd_level += 1
                elif self.attribute == 'ssd':
                    ssd_level += 1
                money -= self.price + self.level * self.scale
                save_variables()

        above_text_display = self.above_font.render(
            f'{self.above_text}',
            True,
            (255, 255, 255)
        )
        below_text_display = self.below_font.render(
            f'{self.below_text}',
            True,
            (255, 255, 255)
        )

        if self.level >= 5:
            display.blit(above_text_display,
                         (self.rect.centerx - above_text_display.get_width() / 2, self.rect.top - 65))
            display.blit(self.description_text_display,
                         (self.rect.centerx - self.description_text_display.get_width() / 2, self.rect.y - 10))
        else:
            display.blit(above_text_display,
                         (self.rect.centerx - above_text_display.get_width() / 2, self.rect.top - 35))
            display.blit(self.description_text_display, (self.rect.centerx - self.description_text_display.get_width() / 2, self.rect.y + 20))
        display.blit(below_text_display, (self.rect.centerx - below_text_display.get_width() / 2, self.rect.bottom))

        if self.level < 5:
            self.image = btn_upgrade
        else:
            self.image = btn_maximized


# CRIAÇÃO DE GRUPOS
# Os grupos possibilitam a agrupamento de vários sprites em um único local
# facilitando no processo de desenhar os sprites e chamar o seu metodo update


cpu = CPU()

Cpu_Group = GroupSingle()
Cpu_Group.add(cpu)

Scanner_Group = Group()

Virus_Group = Group()

Worms_Group = Group()

Item_Group = Group()

Text_Group = Group()

Shop_Group = Group()

Status_Group = Group()

Game_state = Game_State()

# BUTTON GROUPS

# MAIN MENU BUTTONS
Button_Group = Group()
Button_Group.add(Button(0, DISPLAY_HEIGHT - 480, btn_start, 1, 'main game'))
Button_Group.add(Button(0, DISPLAY_HEIGHT - 360, btn_htplay, 1, 'how to play'))
Button_Group.add(Button(0, DISPLAY_HEIGHT - 240, btn_shop, 1, 'shop'))
Button_Group.add(Button(0, DISPLAY_HEIGHT - 120, btn_exit, 1, 'exit'))


# PAUSE BUTTONS
Pause_Group = Group()
Pause_Group.add(Button(0, DISPLAY_HEIGHT - 120, btn_resume, 1, 'resume'))
Pause_Group.add(Button(DISPLAY_WIDTH / 2 - 200, DISPLAY_HEIGHT - 120, btn_reset, 1, 'reset'))
Pause_Group.add(Button(DISPLAY_WIDTH - 380, DISPLAY_HEIGHT - 140, btn_main, 1, 'main menu'))

# HOW TO PLAY BUTTONS
HTPlay_Group = Group()
HTPlay_Group.add(Button(0, DISPLAY_HEIGHT - 130, btn_back, 0.8, 'main menu'))

# SHOP BUTTONS
Shop_Group.add(Button(0, DISPLAY_HEIGHT - 130, btn_back, 0.8, 'main menu'))
Shop_Group.add(Shop_Button(DISPLAY_WIDTH / 2 - 200, DISPLAY_HEIGHT / 2 - 50, 'antivirus', 450, 200))
Shop_Group.add(Shop_Button(DISPLAY_WIDTH / 2 + DISPLAY_WIDTH / 4 - 200, DISPLAY_HEIGHT / 2 - 200, 'ram', 200, 150))
Shop_Group.add(Shop_Button(DISPLAY_WIDTH / 2 + DISPLAY_WIDTH / 4 - 200, DISPLAY_HEIGHT / 2 + 100, 'ssd', 350, 250))
Shop_Group.add(Shop_Button(DISPLAY_WIDTH / 2 - DISPLAY_WIDTH / 4 - 200, DISPLAY_HEIGHT / 2 - 200, 'cpu', 300, 150))
Shop_Group.add(Shop_Button(DISPLAY_WIDTH / 2 - DISPLAY_WIDTH / 4 - 200, DISPLAY_HEIGHT / 2 + 100, 'hd', 250, 200))


# Modelos de Inimigo
# ORDEM VIDA, GAP DE VIDA, MOV SPEED, MOV COOLDOWN, SCORE BASE, IMAGEM, ESCALA, TIPO
Virus_Model = [2, 2000, 15, 0.1, 30, normal_sprites, 2, None]
Fast_Virus_Model = [1.5, 4500, 30, 0.05, 80, fast_sprites, 0.40, None]
Worms_Model = [8, 5000, 30, 0, 1500, worm_sprites, 0.9, 'Worm']
Worms_Child_Model = [1.5, 1000000, 15, 0.2, 10, child_sprites, 0.30, None]


def thunder(entity, target, color, size):
    between_pos = []

    if len(Virus_Group) > 0:
        if entity[0] < target[0]:
            between_pos.append(randint(entity[0], target[0]))
        else:
            between_pos.append(randint(target[0], entity[0]))

        if entity[1] < target[1]:
            between_pos.append(randint(entity[1], target[1]))
        else:
            between_pos.append(randint(target[1], entity[1]))

    dark_color = (int(color[0] / 1.3), int(color[1] / 1.3), int(color[2] / 1.3))

    pygame.draw.line(display, dark_color, entity, between_pos, size)
    pygame.draw.line(display, color, between_pos, target, int(size / 1.3))


def music_manager():
    if Game_state.game_state == 'main game':
        pygame.mixer.music.set_volume(0.3)
    elif Game_state.game_state == 'main menu':
        pygame.mixer.music.set_volume(0.3)
    else:
        pygame.mixer.music.set_volume(0.3)


# LAÇO PRINCIPAL DO JOGO
while isRunning:
    # Por tick chama o método state_manager que analise o estado atual do jogo e roda
    # um laço de repetição específico, cada laço representa um estado do jogo
    # como, tela inicial, loja, jogo
    Game_state.state_manager()

    # Verificação do estado do jogo para alterar o volume da música

    music_manager()

    # Verifica a posição e o click do mouse
    pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (Game_state.game_state == 'main game' or Game_state.game_state == 'pause'):
                if Game_state.game_state == 'pause' and cpu.HP > 0 and percentage < 100:
                    Game_state.game_state = 'main game'
                    pygame.mixer.music.unpause()
                else:
                    Game_state.game_state = 'pause'
                    pygame.mixer.music.pause()
            if event.key == pygame.K_LEFT and Game_state.game_state == 'main game':
                # Item_Group.add(Item(True))
                cpu.HP += 1

    pygame.display.update()
    clock.tick(FPS)
