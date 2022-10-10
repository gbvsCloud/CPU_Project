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


# Sobreecresve dados no save do jogador, esse método pede
# a linha que será alterada e o novo valor a ser adicionado
# nessa nova linha
def save_variables(line, new_value):
    with open('player_status.txt', 'w') as file:
        list_size = range(len(player_variables))
        for word in list_size:
            if word == line and line != None:
                file.write(str(new_value))
                file.write('\n')
            else:
                file.write(player_variables[word])
                file.write('\n')


#IMPORTAÇÃO DOS ARQUVOS UTILIZADOS NO JOGO
# SETUP
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

# FONTS CONFIG
DEFAULT_FONT = font.Font('Fonts/game_over.ttf', 120)
TITLE_FONT = font.Font('Fonts/game_over.ttf', 200)

# SOUNDS
click_sound = pygame.mixer.Sound('Sounds/click_sound.wav')
click_sound.set_volume(1)

# MUSICS
pygame.mixer.music.load('Sounds/Spooktune.mp3')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

# SPRITES
virus_image = load('Images/virus.png').convert_alpha()
fast_virus = load('Images/virus_rapido.png').convert_alpha()
worm_virus = load('Images/virus_worm.png')
cpu = load('Images/cpu.jpg')
scanner = load('Images/scanner.png')
scanner_coll = load('Images/scanner_coll.png')

heal_item = load('Images/heal_item.png')
health_item = load('Images/health_item.png')
damage_item = load('Images/damage_item.png')
chain_item = load('Images/chain_item.png')
drain_item = load('Images/drain_item.png')
defense_item = load('Images/defense_item.png')

btn_start = load('Images/btn_start.png')
btn_exit = load('Images/btn_exit.png')
btn_shop = load('Images/btn_shop.png')
btn_main = load('Images/btn_mainmenu.png')
btn_resume = load('Images/btn_resume.png')
btn_reset = load('Images/btn_reset.png')
btn_credits = load('Images/btn_credits.png')
btn_htplay = load('Images/btn_howtoplay.png')
btn_back = load('Images/btn_back.png')

# BACKGROUND
background = load('Images/windowserror.png').convert()
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

pause_bg = load('Images/pause_bg.png').convert_alpha()
pause = pygame.transform.scale(pause_bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

htplay = load('Images/htplay.png').convert()
htplay = pygame.transform.scale(htplay, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

shop_bg = load('Images/shop_bg.png').convert()
shop_bg = pygame.transform.scale(shop_bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

mainmenu_background = load('Images/mainmenu_bg.png').convert()
mainmenu_background = pygame.transform.scale(mainmenu_background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))


#DIVERSAS CLASSES UTILIZADAS PARA CRIAR UM PADRÃO E PODE UTILIZAR DA ORIENTAÇÃO A OBJETOS
# A CLASSE SPRITE JÁ VEM POR PADRÃO COM VARIÁVEIS E METODOS PRÓPRIOS QUE AJUDAM NA CRIAÇÃO
# DE INIMIGOS, BOTÕES, PLAYER
class CPU(Sprite):

    HP = 3
    MAX_HP = 3
    damage_invulnerability = 0
    timer = 0

    def __init__(self, scale):
        super().__init__()
        self.image = cpu
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (width * scale, height * scale))
        self.rect = self.image.get_rect(center=(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2))

    def update(self):
        global defense_stacks, FPS, drain_stacks, timer
        if self.damage_invulnerability > 0:
            self.damage_invulnerability -= 1 / FPS
        if pygame.sprite.groupcollide(Cpu_Group, Virus_Group, False, True):
            self.got_hit()

        if self.HP > self.MAX_HP:
            self.HP = self.MAX_HP
        if drain_stacks > 0:
            self.drain_effect()
        #if (drain_stacks == 1 and timer <= 1800) or timer <= 1800:
           # cpu.HP += (cpu.MAX_HP - cpu.HP) * (0.005 * drain_stacks) / 1.5
        if defense_stacks > 0:
            self.emergency_defense()

    def emergency_defense(self):
        global timer
        self.timer += (1 + len(Virus_Group) / 12) / FPS

        if self.HP < self.MAX_HP:
            self.HP += (self.MAX_HP - self.HP) * (0.005 * defense_stacks) / FPS
            #print('Curado em {}'.format((self.MAX_HP - self.HP) * (0.005 + defense_stacks * 0.001)/ FPS))

        if self.timer >= 0.5 and (self.HP <= self.MAX_HP / 2 or len(Virus_Group) >= 6 or self.HP < 5 or timer < 900):
            self.timer = 0
            if len(Virus_Group) > 0:
                random = randint(0, len(Virus_Group) - 1)
                thunder(self.rect.center, Virus_Group.sprites()[random].rect.center, (0, 255, 50), 5)
                Virus_Group.sprites()[random].life -= defense_stacks + self.MAX_HP + (Virus_Group.sprites()[random].max_life - Virus_Group.sprites()[random].life) / 6

    def drain_effect(self):
        global drain_stacks, click_damage
        for enemy in Virus_Group:
            enemy.life -= (drain_stacks + (click_damage / 2) + (enemy.max_life - enemy.life) * (0.05 * drain_stacks)) / FPS
            self.HP += self.MAX_HP * 0.001 / FPS
            #print('Vida curada {}'.format(enemy.max_life * 0.01 / FPS))

    def got_hit(self):
        if self.damage_invulnerability <= 0:
            self.HP -= 1
            self.damage_invulnerability = 0.10


class Item(Sprite):
    type = None
    movement = True
    timer = 0

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
                x = randint(0, 2)
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
        else:
            x = randint(0, 2)
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
        self.rect = self.image.get_rect()
        if self.type != 'Chain' and self.type != 'Defense':
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, DISPLAY_WIDTH - self.image.get_width())
        self.rect.y = randint(0, DISPLAY_HEIGHT - self.image.get_height())

    def update(self):
        global pos, mouse_click

        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            mouse_click = True
            self.kill()

        self.timer += 1/FPS

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
        global click_damage, chain_stacks, drain_stacks, defense_stacks
        if self.type == 'Heal':
            if cpu.HP < cpu.MAX_HP:
                cpu.HP += 1 + (cpu.MAX_HP - cpu.HP) / 3
        elif self.type == 'Health':
            cpu.MAX_HP += 1
            cpu.HP += 1
        elif self.type == 'Damage':
            click_damage += 1
        elif self.type == 'Chain':
            chain_stacks += 1
        elif self.type == 'Drain':
            drain_stacks += 1
        elif self.type == 'Defense':
            defense_stacks += 1


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
            self.image = pygame.transform.scale(self.image, (int(self.width * 0.90), int(self.height * 0.90)))
        else:
            self.image = self.original_image
        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            if self.scene == 'main game' and Game_state.game_state != 'pause' or self.scene == 'reset':
                Game_state.reset = 0
            if self.scene == 'reset':
                #BOTÃO METODOS
                Game_state.reset = 0
                Game_state.game_state = 'main game'
            else:
                if self.scene == 'main menu':
                    money += int(score * 0.01)
                    save_variables(1, money)
                Game_state.game_state = self.scene


class Shop_Button(Sprite):
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
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (int(self.width * 0.90), int(self.height * 0.90)))
        else:
            self.image = self.original_image
        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            ...


class Game_State:
    reset = 0

    def __init__(self):
        self.game_state = 'main menu'
        self.randPos = 0
        self.randX = 0
        self.randY = 0

    def main_game(self):
        global timer, score, money, enemies_killed, click_damage, chain_stacks, drain_stacks, execute_stacks

        if len(Scanner_Group) <= 0:
            ...
        # Scanner_Group.add(Scanner())

        if cpu.HP <= 0:
            money += int(score * 0.01)
            save_variables(1, money)
            Game_state.game_state = 'pause'

        if enemies_killed % 20 == 0:
            Item_Group.add(Item(False))
            enemies_killed = 1


        if self.reset == 0:  # RESETAR PARTIDA E VARIAVEIS
            self.reset_game()

        timer += 1
        display.blit(background, (0, 0))

        if timer % 600 == 0:
            if self.randPos == 0:
                Virus_Group.add(Enemy(Worms_Model,
                                      randint(0, DISPLAY_WIDTH),
                                      self.randY * (DISPLAY_HEIGHT)))

            else:
                Virus_Group.add(Enemy(Worms_Model,
                                      (randint(0, DISPLAY_WIDTH)),
                                      (self.randY * (DISPLAY_HEIGHT))))

        if timer % 60 == 0:
            self.randPos = randint(0, 1)
            self.randX = randint(0, 1)
            self.randY = randint(0, 1)

            if self.randPos == 0:
                if randint(0, 5) == 0:
                    Virus_Group.add(Enemy(Fast_Virus_Model,
                                          (randint(0, DISPLAY_WIDTH)),
                                          (self.randY * (DISPLAY_HEIGHT))))
                else:
                    Virus_Group.add(Enemy(Virus_Model,
                                          (randint(0, DISPLAY_WIDTH)),
                                          (self.randY * (DISPLAY_HEIGHT))))

            else:
                if randint(0, 5) == 0:
                    Virus_Group.add(Enemy(Fast_Virus_Model,
                                          (self.randX * ((DISPLAY_WIDTH))),
                                          (randint(0, DISPLAY_HEIGHT))))
                else:
                    Virus_Group.add(Enemy(Virus_Model,
                                          (self.randX * (DISPLAY_WIDTH)),
                                          (randint(0, DISPLAY_HEIGHT))))

        Cpu_Group.update()
        Cpu_Group.draw(display)

        Scanner_Group.update()
        Scanner_Group.draw(display)

        Virus_Group.update()
        Virus_Group.draw(display)

        Item_Group.update()
        Item_Group.draw(display)

        Worms_Group.update()
        Worms_Group.draw(display)

        # DISPLAYS
        score_display = DEFAULT_FONT.render(
            f'Pontuacao:{int(score)}',
            True,
            (255, 255, 255)
        )

        display.blit(score_display, (0, DISPLAY_HEIGHT - score_display.get_rect().bottom))

        hp_display = DEFAULT_FONT.render(
            f'Saude da CPU:{"{:.1f}".format(cpu.HP)}/{int(cpu.MAX_HP)}',
            True,
            (255, 255, 255)
        )
        display.blit(hp_display, (0, DISPLAY_HEIGHT - hp_display.get_rect().bottom - 50))


    def reset_game(self):
        global score, enemies_killed, click_damage, drain_stacks, chain_stacks, defense_stacks, money, execute_stacks

        money += int(score * 0.01)
        save_variables(1, money)

        score = 0

        Virus_Group.empty()
        Worms_Group.empty()
        Scanner_Group.empty()
        Item_Group.empty()
        Item_Group.add(Item(True))
        #Scanner_Group.add(Scanner())

        enemies_killed = 1
        click_damage = 1
        cpu.MAX_HP = 3
        cpu.HP = cpu.MAX_HP

        chain_stacks = 0
        drain_stacks = 0
        defense_stacks = 0
        execute_stacks = 0

        self.reset += 1

    def main_menu(self):

        # display.blit(mainmenu_background, (0, 0))
        display.fill((255, 255, 255))


        title_display = TITLE_FONT.render(
            f'CPU - CENTRAL DE PANICO URGENTE',
            True,
            (38, 83, 24)
        )
        display.blit(title_display, (DISPLAY_WIDTH / 2 - title_display.get_width() / 2, -10))

        Button_Group.draw(display)
        Button_Group.update()

    def exit(self):
        pygame.quit()
        sys.exit()

    def pause(self):
        # DISPLAYS


        #print('Base damage: {}'.format(click_damage))
        #print('Chain stacks: {}'.format(chain_stacks))
        #print('Drain stacks: {}'.format(drain_stacks))
        #print('\n\n\n\n\n\n')

        display.blit(background, (0, 0))

        hp_display = DEFAULT_FONT.render(
            f'Saude da CPU:{int(cpu.HP)}/{int(cpu.MAX_HP)}',
            True,
            (255, 255, 255)
        )
        display.blit(hp_display, (0, DISPLAY_HEIGHT - hp_display.get_rect().bottom - 50))

        score_display = DEFAULT_FONT.render(
            f'Pontuacao:{int(score)}',
            True,
            (255, 255, 255)
        )
        display.blit(score_display, (0, DISPLAY_HEIGHT - score_display.get_rect().bottom))

        Cpu_Group.draw(display)
        Scanner_Group.draw(display)
        Virus_Group.draw(display)
        Worms_Group.draw(display)
        Item_Group.draw(display)

        display.blit(pause_bg, (0, 0))

        if cpu.HP > 0:
            pause_display = TITLE_FONT.render(
                f'JOGO PAUSADO.',
                True,
                (38, 83, 24)
            )
        else:
            pause_display = TITLE_FONT.render(
                f'VOCE PERDEU.',
                True,
                (38, 83, 24)
            )

        display.blit(pause_display, (DISPLAY_WIDTH / 2 - pause_display.get_width() / 2, -10))

        Pause_Group.draw(display)
        Pause_Group.update()

    def htplay(self):
        display.blit(htplay, (0, 0))
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
    movement_cooldown = 0
    movement_speed = 0
    movement_speed_save = movement_speed
    base_score = 0
    final_score = 0
    time_alive = 0
    max_life = 0
    life = 0

    id = 0
    #SPECIAL VIRUS
    type = None
    spawn_timer = 1.5

    def __init__(self, info, x, y):
        super().__init__()
        # ENEMY CLASS ATRIBUTES
        #ORDEM VIDA, GAP DE VIDA, MOV SPEED, MOV COOLDOWN, SCORE BASE, IMAGEM, ESCALA, TIPO

        self.type = info[7]
        self.id = randint(0, 99999999)

        if self.type != 'Worm':
            if int(score / info[1]) <= info[0] * 10000:
                self.max_life = info[0] + int(score / info[1])
            else:
                self.max_life = 100
        else:
            if info[0] * (1 + int(score / info[1])) <= 12000:
                self.max_life = info[0] * (1 + int(score / info[1]))
            else:
                self.max_life = 6000

        self.life = self.max_life
        self.movement_speed = info[2]
        self.movement_speed_save = self.movement_speed
        self.movement_cooldown = info[3]
        self.base_score = info[4]

        # SPRITE CLASS ATRIBUTES

        self.image = pygame.transform.scale(info[5], (info[5].get_width() * info[6], info[5].get_height() * info[6]))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.click_check()
        self.check_life()

        if self.type != 'Worm':
            self.movement()
        elif self.rect.bottom > DISPLAY_HEIGHT or self.rect.right > DISPLAY_WIDTH or self.rect.top < 0 or self.rect.left < 0:
            self.movement()

        if self.type == 'Worm':
            self.spawn_timer -= 1/FPS
            if self.spawn_timer <= 0:
                self.spawn_timer = 1.5
                Virus_Group.add(Enemy(Worms_Child_Model, self.rect.centerx, self.rect.centery))

        if self.life > 0:
            self.draw_life()

    def kill(self):
        global score, enemies_killed, chain_stacks, drain_stacks
        enemies_killed += 1

        if self.type != 'Worm':
            score += (self.base_score * self.max_life)
        else:
            score += (self.base_score * (self.max_life / 6))

        self.chain_effect()

        if self.type == 'Worm':
            if randint(0, 2) > 0:
                Item_Group.add(Item(True))

        Sprite.kill(self)

    def click_check(self):
        global pos, mouse_click
        #CALCULO DE DANO NO INIMGO AO CLICAR
        if self.rect.collidepoint(pos) and mouse_click == False and pygame.mouse.get_pressed()[0]:
            mouse_click = True
            self.life -= click_damage + (self.max_life - self.life) * 0.05

    def chain_effect(self):
        if len(Virus_Group) > 1 and chain_stacks > 0:
            for i in range(int(chain_stacks / 3) + 1):
                random = -1
                while random == -1 or Virus_Group.sprites()[random].id == self.id:
                    random = randint(0, len(Virus_Group) - 1)

                if len(Virus_Group) >= random:
                    Virus_Group.sprites()[random].life -= (click_damage * (chain_stacks / 2) + Virus_Group.sprites()[random].max_life * 0.25)
                    #print('Default damage: {}'.format((click_damage * (1 + chain_stacks))))
                    #print('Targe Life: {}, Extra Damage: {}'.format(Virus_Group.sprites()[random].max_life, Virus_Group.sprites()[random].max_life / 4))
                    #print('Boosted damage: {}'.format((click_damage * (1 + chain_stacks) + Virus_Group.sprites()[random].max_life / 4)))
                    thunder(self.rect.center, Virus_Group.sprites()[random].rect.center, (255, 255, 0), 6)

    def check_life(self):
        global execute_stacks
        if self.life <= 0 or self.life <= self.max_life * ((execute_stacks * 2.5) / 100):
            print(self.max_life)
            print(self.life)
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
        self.movement_cooldown -= 1 / FPS
        if self.movement_cooldown <= 0:
            cpu_pos = (display.get_width() / 2, display.get_height() / 2)
            if cpu_pos[0] > self.rect.centerx:
                self.rect.x += self.movement_speed
            else:
                self.rect.x -= self.movement_speed
            if cpu_pos[1] > self.rect.centery:
                self.rect.y += self.movement_speed * 0.5625
            else:
                self.rect.y -= self.movement_speed * 0.5625
            self.movement_cooldown = 0.1


class Scanner(Sprite):
    direction = 1
    mov_speed = 26
    mov_speed_save = mov_speed
    collision = 0

    cooldown = 0

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(scanner, (10, DISPLAY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
    def update(self):
        self.movement()
        if self.collision > 0:
            self.image = self.image = pygame.transform.scale(scanner_coll, (10, DISPLAY_HEIGHT))
            self.mov_speed = self.mov_speed_save / 8
            self.collision -= 1/FPS
        else:
            if self.cooldown <= 0:
                self.image = pygame.transform.scale(scanner, (10, DISPLAY_HEIGHT))
                self.mov_speed = self.mov_speed_save

        if self.cooldown > 0:
            self.cooldown -= 1/FPS
            self.mov_speed = 0

        for enemy in Virus_Group:
            if self.rect.colliderect(enemy.rect) and self.cooldown <= 0:
                self.damage_effect(enemy)
                enemy.life -= (click_damage * 3) / FPS
                self.collision = 0.05

    def random_color(self):
        return (randint(100, 255), randint(100, 255), randint(100, 255))

    def random_width(self):
        return (randint(3, 9))

    def damage_effect(self, enemy):
        thunder((self.rect.centerx, enemy.rect.centery + randint(10 ,100)), enemy.rect.center, self.random_color(), 6)
        thunder((self.rect.centerx, enemy.rect.centery), enemy.rect.center, (255, 255, 0), 6)
        thunder((self.rect.centerx, enemy.rect.centery - randint(10, 100)), enemy.rect.center, self.random_color(), 6 )

    def movement(self):
        if self.direction == 1:
            self.rect.x += self.mov_speed
            if self.rect.x > DISPLAY_WIDTH:
                self.direction = 0
                self.cooldown = 1
        else:
            self.rect.x -= self.mov_speed
            if self.rect.x <= 0:
                self.direction = 1
                self.cooldown = 1

# CRIAÇÃO DE GRUPOS
# Os grupos possibilitam a agrupamento de vários sprites em um único local
# facilitando no processo de desenhar os sprites e chamar o seu metodo update


cpu = CPU(0.2)

Cpu_Group = GroupSingle()
Cpu_Group.add(cpu)

Scanner_Group = Group()

Virus_Group = Group()

Worms_Group = Group()

Item_Group = Group()

Game_state = Game_State()

# BUTTON GROUPS

# MAIN MENU BUTTONS
Button_Group = Group()
Button_Group.add(Button(0, DISPLAY_HEIGHT - 360, btn_start, 0.8, 'main game'))
Button_Group.add(Button(25, DISPLAY_HEIGHT - 240, btn_shop, 0.8, 'shop'))
Button_Group.add(Button(50, DISPLAY_HEIGHT - 120, btn_exit, 0.8, 'exit'))
Button_Group.add(Button(DISPLAY_WIDTH - 350, DISPLAY_HEIGHT - 240, btn_htplay, 0.8, 'how to play'))
Button_Group.add(Button(DISPLAY_WIDTH - 450, DISPLAY_HEIGHT - 120, btn_credits, 0.8, 'exit'))

# PAUSE BUTTONS
Pause_Group = Group()
Pause_Group.add(Button(0, DISPLAY_HEIGHT - 130, btn_resume, 0.8, 'resume'))
Pause_Group.add(Button(DISPLAY_WIDTH / 2 - 200, DISPLAY_HEIGHT - 130, btn_reset, 0.8, 'reset'))
Pause_Group.add(Button(DISPLAY_WIDTH - 370, DISPLAY_HEIGHT - 130, btn_main, 0.8, 'main menu'))

# HOW TO PLAY BUTTONS
HTPlay_Group = Group()
HTPlay_Group.add(Button(0, DISPLAY_HEIGHT - 130, btn_back, 0.8, 'main menu'))

# SHOP BUTTONS
Shop_Group = Group()
Shop_Group.add(Button(0, DISPLAY_HEIGHT - 130, btn_back, 0.8, 'main menu'))

# Modelos de Inimigo
# ORDEM VIDA, GAP DE VIDA, MOV SPEED, MOV COOLDOWN, SCORE BASE, IMAGEM, ESCALA, TIPO
Virus_Model = [2, 1500, 15, 0.2, 30, virus_image, 0.5, None]
Fast_Virus_Model = [2, 3000, 25, 0.2, 80, fast_virus, 0.40, None]
Worms_Model = [8, 5000, 30, 0, 2000, worm_virus, 0.9, 'Worm']
Worms_Child_Model = [1.5, 1000000, 12, 0.2, 10, worm_virus, 0.30, None]

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

    pygame.draw.line(display, color, entity, between_pos, size)
    pygame.draw.line(display, color, between_pos, target, int(size/1.2))


# LAÇO PRINCIPAL DO JOGO
while isRunning:
    # Por tick chama o método state_manager que analise o estado atual do jogo e roda
    # um laço de repetição específico, cada laço representa um estado do jogo
    # como, tela inicial, loja, jogo
    Game_state.state_manager()

    # Verificação do estado do jogo para alterar o volume da música
    if Game_state.game_state == 'main game':
        pygame.mixer.music.set_volume(0.0)
    elif Game_state.game_state == 'main menu':
        pygame.mixer.music.set_volume(0.0)
    else:
        pygame.mixer.music.set_volume(0.0)

    # Verifica a posição e o click do mouse
    pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if len(Virus_Group) > 0:
            thunder(pos, Virus_Group.sprites()[0].rect.center, (255, 255, 0), 6)
            Virus_Group.sprites()[0].life -= Virus_Group.sprites()[0].max_life / 4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (Game_state.game_state == 'main game' or Game_state.game_state == 'pause'):
                if Game_state.game_state == 'pause' and cpu.HP > 0:
                    Game_state.game_state = 'main game'
                else:
                    Game_state.game_state = 'pause'
            if event.key == pygame.K_SPACE and Game_state.game_state == 'main game':
                #Item_Group.add(Item(True))
                ...

    pygame.display.update()
    clock.tick(60)
