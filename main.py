
import pygame
import json
from pathlib import Path
import math 
pygame.init()

screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()

#define game variables
tile_size = 50
player_size = 50
FPS = 30
dt = clock.tick(FPS) / 25
player_speed = 4
jump_vel = 11
enemy_speed = 1.5
enemy_size = 50
canonball_speed_x = 2
canonball_speed_y = 0
gravity = 1
Game_over = 0
go_back = 0
go_forward = 0
main_menu = True
edit_allowed = True
start_from_edit_allowed = True
level = 0
max_levels = 3
checkpoint_x = 51
checkpoint_y = screen_height - 51
checkpoint_level = 0
coin_counter = 0
death_counter = 0
time_counter = 0
frame_counter = 0
pygame.font.init()
my_font = pygame.font.SysFont('arial', 30)
my_font_small = pygame.font.SysFont('arial', 20)

#load images

restart_img_ = pygame.image.load('restart_button.png')
restart_img = pygame.transform.scale(restart_img_, (200, 100))
darken_img_ = pygame.image.load('darken.png')
darken_img = pygame.transform.scale(darken_img_, (screen_width, screen_height))
start_img_ = pygame.image.load('start_button.png')
start_img = pygame.transform.scale(start_img_, (200, 100))
quit_img_ = pygame.image.load('quit_button.png')
quit_img = pygame.transform.scale(quit_img_, (100, 50))
you_win_img_ = pygame.image.load('you_win.png')
you_win_img = pygame.transform.scale(you_win_img_, (300, 200))
yellow_img_ = pygame.image.load('yellow.png')
yellow_img = pygame.transform.scale(yellow_img_, (screen_width, screen_height))
edit_img_ = pygame.image.load('edit.png')
edit_img = pygame.transform.scale(edit_img_, (100, 50))
coin_counter_img_ = pygame.image.load('coin_counter.png')
coin_counter_img = pygame.transform.scale(coin_counter_img_, (120, 40))
main_menu_img_ = pygame.image.load('main_menu.png')
main_menu_img = pygame.transform.scale(main_menu_img_, (70, 50))
start_from_edited_img_ = pygame.image.load('start_from_edited.png')
start_from_edited_img = pygame.transform.scale(start_from_edited_img_,(100, 50))

dead_enemy_group_rect = []


#function to reset level
def reset_level(level, coin_counter):
  Player.reset(player, checkpoint_x, checkpoint_y)
  enemy_group.empty()
  spike_group.empty()
  exit_left_group.empty()
  exit_right_group.empty()
  checkpoint_group.empty()
  dead_enemy_group.empty()
  dead_enemy_group_rect.clear()
  coin_group.empty()
  door_group.empty()
  key_group.empty()
  canon_group.empty()
  canonball_group.empty()
  coin_counter = 0

  data = open(f'level{level}_data.json')
  world_data = json.load(data)
  World = world(world_data)
  exit_left = Exit_left(-tile_size, 0)
  exit_left_group.add(exit_left)
  exit_right = Exit_right(screen_width, 0)
  exit_right_group.add(exit_right)

  return World, coin_counter


def go_forward_level(level):
  Player.reset(player, 1, player.get_player_y())
  enemy_group.empty()
  spike_group.empty()
  exit_left_group.empty()
  exit_right_group.empty()
  checkpoint_group.empty()
  dead_enemy_group.empty()
  dead_enemy_group_rect.clear()
  coin_group.empty()
  door_group.empty()
  key_group.empty()
  canon_group.empty()
  canonball_group.empty()
  
  data = open(f'level{level}_data.json')
  world_data = json.load(data)
  World = world(world_data)
  exit_left = Exit_left(-tile_size, 0)
  exit_left_group.add(exit_left)
  exit_right = Exit_right(screen_width, 0)
  exit_right_group.add(exit_right)
  return World


def go_back_level(level):
  Player.reset(player, screen_width - (tile_size + 1), player.get_player_y())
  enemy_group.empty()
  spike_group.empty()
  exit_left_group.empty()
  exit_right_group.empty()
  checkpoint_group.empty()
  dead_enemy_group.empty()
  dead_enemy_group_rect.clear()
  coin_group.empty()
  door_group.empty()
  key_group.empty()
  canon_group.empty()
  canonball_group.empty()
  
  data = open(f'level{level}_data.json')
  world_data = json.load(data)
  World = world(world_data)
  exit_left = Exit_left(-tile_size, 0)
  exit_left_group.add(exit_left)
  exit_right = Exit_right(screen_width, 0)
  exit_right_group.add(exit_right)
  return World


class button():

  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.clicked = False

  def draw(self):
    action = False
    pos = pygame.mouse.get_pos()

    if self.rect.collidepoint(pos
                             ) and pygame.mouse.get_pressed()[0] and not self.clicked:
        action = True
        self.clicked = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    screen.blit(self.image, self.rect)

    return action


class Player():

  def __init__(self, x, y):
    self.reset(x, y)

  def update(self, Game_over, go_back, go_forward, checkpoint_x, checkpoint_y,
             checkpoint_level, level, coin_counter):
    gravity = True
    dx = 0
    dy = 0
    walk_cooldown = 2
    if Game_over == 0:
      #get keypresses
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT]:
        dx -= player_speed * dt
        self.counter += 1
        self.direction = -1
      if key[pygame.K_RIGHT]:
        dx += player_speed * dt
        self.counter += 1
        self.direction = 1
      if key[pygame.K_SPACE] and not self.jumped:
        self.jumped = True
        self.vel_y = -jump_vel * dt
        self.jump_counter += 1
      if self.jumped:
        self.image = self.image_jump
      if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[
          pygame.K_SPACE] and not self.jumped:
        self.counter = 0
        self.index = 0
        if self.direction == 1:
          self.image = self.images_right[self.index]
        if self.direction == -1:
          self.image = self.images_left[self.index]

      #handle animation
      if self.counter > walk_cooldown and not self.jumped:
        self.counter = 0
        self.index += 1
        if self.index >= len(self.images_right):
          self.index = 0
        if self.direction == 1:
          self.image = self.images_right[self.index]
        if self.direction == -1:
          self.image = self.images_left[self.index]

      #gravity
      self.vel_y += gravity
      if self.vel_y > 15:
        self.vel_y = 15
      dy += self.vel_y

      #check for collision
      for tile in World.tile_list:
        #check for collision in x direction
        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
                               self.height):
          dx = 0
        #check for collision in y direction
        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                               self.height):
          gravity = False
          #check if below the ground i.e. jumping
          if self.vel_y < 0:
            dy = tile[1].bottom - self.rect.top
            self.vel_y = 0
          #check if above the ground i.e. falling
          elif self.vel_y >= 0:
            dy = tile[1].top - self.rect.bottom
            self.jumped = False
            self.jump_counter = 0

      #chekc for collision with enemy
      if pygame.sprite.spritecollide(self, enemy_group, False):
        Game_over = -1

      #check for collision with dead enemy
      #make seperate list
      for enemy_dead in dead_enemy_group_rect:
        if enemy_dead.colliderect(self.rect.x + dx, self.rect.y, self.width,
                                  self.height):
          dx = 0
      #check for collision in y direction
        if enemy_dead.colliderect(self.rect.x, self.rect.y + dy, self.width,
                                  self.height):
          #check if below the ground i.e. jumping
          if self.vel_y < 0:
            dy = enemy_dead.bottom - player.rect.top
            self.vel_y = 0
        #check if above the ground i.e. falling
          elif self.vel_y >= 0:
            dy = enemy_dead.top - player.rect.bottom
            self.jumped = False
            self.jump_counter = 0

      #chekc for collision with spikes
      if pygame.sprite.spritecollide(self, spike_group, False):
        Game_over = -1

      #check for collison with coin
      if pygame.sprite.spritecollide(self, coin_group, False):
        coin_counter += 1
        for coin in coin_group:
          Coin.update(coin)
      #check for collision with checkpoint

      if pygame.sprite.spritecollide(self, checkpoint_group, False):
        for checkpoint in checkpoint_group:
          checkpoint.image = pygame.image.load('checkpoint-frame-0.png')
          checkpoint.image = pygame.transform.scale(checkpoint.image,
                                                    (tile_size, tile_size))

        checkpoint_x = self.rect.x
        checkpoint_y = self.rect.y
        checkpoint_level = level
        checkpoint_group.update()
      #check for collision with exit
      if pygame.sprite.spritecollide(self, exit_left_group, False):
        go_back = 1

      if pygame.sprite.spritecollide(self, exit_right_group, False):
        go_forward = 1

      #check collision with door
      if pygame.sprite.spritecollide(
          self, door_group, False) and not pygame.sprite.spritecollide(
              self, held_key_group, False):
        dx = -1

      #check for collision with canonball
      for ball in canonball_group:
        if pygame.sprite.spritecollide(self, canonball_group, False):
          ball.image = pygame.image.load('explosion-frame-1.png')
          Game_over = -1  
      
      #if player goes below screen

      if self.rect.y > screen_height:
        Game_over = -1

      #update player coordinates
      self.rect.x += dx
      self.rect.y += dy

    elif Game_over == -1:
      img = self.dead_image
      self.image = pygame.transform.scale(img,
                                          (0.85 * player_size, player_size))

    #draw player
    screen.blit(self.image, self.rect)

    return (Game_over, go_back, go_forward, checkpoint_x, checkpoint_y, checkpoint_level
            ,level, coin_counter)

  def get_player_y(self):
    return self.rect.y

  def reset(self, x, y):
    self.images_right = []
    self.images_left = []
    self.index = 0
    self.counter = 0
    self.image_land = pygame.image.load('player-land.png')
    self.image_jump = pygame.image.load('player-jump.png')
    self.image_jump = pygame.transform.scale(self.image_jump,
                                             (0.8 * player_size, player_size))
    for num in range(0, 3):
      img_right = pygame.image.load(f'player-frame-{num}.png')
      img_right = pygame.transform.scale(img_right,
                                         (0.8 * player_size, player_size))
      img_left = pygame.transform.flip(img_right, True, False)
      self.images_right.append(img_right)
      self.images_left.append(img_left)
    dead_image = pygame.image.load('player-dead.png')
    self.dead_image = pygame.transform.scale(dead_image,
       (0.8 * player_size, player_size))
    self.image = self.images_right[self.index]
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.vel_y = 0
    self.jumped = False
    self.direction = 0
    self.jump_counter = 0


class world():

  def __init__(self, data):
    self.reset(data)

  def reset(self, data):
    self.tile_list = []

    #loadimages
    block_img = pygame.image.load('Block.png')
    #placements

    row_count = 0
    for row in data:
      col_count = 0
      for tile in row:
        if tile == 1:
          img = pygame.transform.scale(block_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          tile = (img, img_rect)
          self.tile_list.append(tile)
        if tile == 2:
          spike = Spike(col_count * tile_size,
                        row_count * tile_size + tile_size * 0.5)
          spike_group.add(spike)
        if tile == 3:
          enemy = Enemy(col_count * tile_size, row_count * tile_size)
          enemy_group.add(enemy)
        if tile == 4:
          checkpoint = Checkpoint(col_count * tile_size, row_count * tile_size)
          checkpoint_group.add(checkpoint)
        if tile == 5:
          coin = Coin(col_count * tile_size, row_count * tile_size)
          coin_group.add(coin)
        if tile == 6:
          door = Door(col_count * tile_size, row_count * tile_size)
          door_group.add(door)
        if tile == 7 and len(held_key_group) == 0:
          key = Key(col_count * tile_size + 5, row_count * tile_size + 15)
          key_group.add(key)
        if tile == 8:
          canon = Canon(col_count * tile_size -9, row_count * tile_size - 25)
          canon_group.add(canon)
        
        col_count += 1
      row_count += 1

  def draw(self):
    for tile in self.tile_list:
      screen.blit(tile[0], tile[1])


class Checkpoint(pygame.sprite.Sprite):

  def __init__(self, x, y):
    self.reset(x, y)

  def update(self):
    if player.rect.colliderect(self.rect.x, self.rect.y, self.width,
                               self.height):
      self.image = pygame.image.load('checkpoint-frame-1.png')
      self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

  def reset(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('checkpoint-frame-0.png')
    self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()


class Enemy(pygame.sprite.Sprite):

  def __init__(self, x, y):
    self.reset(x, y)

  def update(self):
    enemy_x = 0
    enemy_y = 0

    #gravity
    self.vel_y += gravity
    if self.vel_y > 15:
      self.vel_y = 15
    enemy_y += self.vel_y
    #move x
    if self.rect.x > player.rect.x:
      enemy_x = -1 * enemy_speed * dt
    elif self.rect.x < player.rect.x:
      enemy_x = 1 * enemy_speed * dt
    #collision x
    for tile in World.tile_list:
      if tile[1].colliderect(self.rect.x + enemy_x, self.rect.y, self.width,
                             self.height):
        enemy_x = 0
    #collision y
      if tile[1].colliderect(self.rect.x, self.rect.y + enemy_y, self.width,
                             self.height):
        enemy_y = tile[1].top - self.rect.bottom
    #collision with spikes
    if pygame.sprite.spritecollide(self, spike_group, False):
      self.image = pygame.image.load('enemy-dead.png')
      self.image = pygame.transform.scale(
          self.image, (0.75 * enemy_size, 0.9 * enemy_size))
      self.remove(enemy_group)
      self.add(dead_enemy_group)
      dead_enemy_group_rect.append(self.rect)

    
    self.rect.x +=  enemy_x
    self.rect.y += enemy_y

  def reset(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('enemy.png')
    self.image = pygame.transform.scale(self.image,
                                        (0.8 * enemy_size, enemy_size))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.move_direction = -1
    self.vel_y = 0


class Spike(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('spike.png')
    self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()


class Exit_left(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('exit-frame-0.png')
    self.image = pygame.transform.scale(img,
                                        (tile_size, tile_size * screen_height))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()


class Exit_right(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('exit-frame-0.png')
    self.image = pygame.transform.scale(img,
                                        (tile_size, tile_size * screen_height))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()


class Coin(pygame.sprite.Sprite):

  def __init__(self, x, y):
    self.frame = 0
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load(f'coin-frame-{self.frame}.png')
    self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
    self.rect = self.image.get_rect()
    self.rect.x = x + tile_size // 4
    self.rect.y = y + tile_size // 4
    self.width = self.image.get_width()
    self.height = self.image.get_height()

  def update(self):
    if player.rect.colliderect(self.rect.x, self.rect.y, self.width,
                               self.height):
      self.kill()

  def animate(self):
    coin_animation = [
        0,0,0,0,1,1,1,1,2,2,2,2,3,3, 3,2,2,2,2,1,1,1,1,0
    ]
    self.frame += 1
    if self.frame >= len(coin_animation):
      self.frame = 0
    img = pygame.image.load(f'coin-frame-{coin_animation[self.frame]}.png')
    self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))


class Door(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('door-frame-0.png')
    self.image = pygame.transform.scale(img, (tile_size, tile_size))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.tile = (self.image, self.rect)

  def open(self):
    self.image = pygame.image.load('door-frame-1.png')


class Key(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('key.png')
    self.image = pygame.transform.scale(img, (40, 17))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()

  def update(self):
    if player.rect.colliderect(self.rect.x, self.rect.y, self.width,
                               self.height):
      key_group.remove(self)
      held_key_group.add(self)
    if self in held_key_group:
      self.rect.x = player.rect.x + player.width // 2
      self.rect.y = player.rect.y + player.height // 2
    for door in door_group:
      if door.rect.colliderect(self.rect):
        door.open()

class Canon(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('canon-frame-0.png')
    self.image = pygame.transform.scale(img, (75,75))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.tile = (self.image, self.rect)
    self.cooldown = 100
  def update(self):
    self.cooldown -= 1
    if self.cooldown == 0:
      if self.rect.y + 75 > player.rect.y:
        canonball = Canonball(self.rect.x+ self.width//2 - 10, self.rect.y +self.height - 20)
        canonball_group.add(canonball)
        self.cooldown= 100
      else:
        self.cooldown = 1
class Canonball(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('canonball.png')
    self.image = pygame.transform.scale(img, (20,20))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.tile = (self.image, self.rect)
    self.frame = 0
    
  def explode(self):
    explosion_animation = [0,1,2,3,4,5,6]
    self.frame += 1
    if self.frame >= len(explosion_animation):
      self.kill()
      frame = 0
    else:
      img = pygame.image.load(f'explosion-frame-{explosion_animation[self.frame]}.png')
      self.image = pygame.transform.scale(img,(21,21))
        
  def update(self):
    #figure out what direction the ball is from the player
    #player coordinates - ball coordinates = slope = multpleior of speed_X and _y
    distance = math.sqrt((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
    angle =math.acos((player.rect.y- self.rect.y)/distance)
    speed= 1
    canonball_speed_x = math.cos(angle)/ speed
    canonball_speed_y = math.sin(angle)/speed

    
    for ball in canonball_group:
      moving= True
      canonball_x = 0
      canonball_y = 0
      if ball.rect.x > player.rect.x + 25:
        canonball_x = -1 * canonball_speed_x * dt
      elif ball.rect.x < player.rect.x +25:
        canonball_x = 1 * canonball_speed_x* dt
      #move x
      if ball.rect.y > player.rect.y +25:
        canonball_y = -2 * canonball_speed_y * dt
      elif ball.rect.y < player.rect.y +25:
        canonball_y = 2 * canonball_speed_y* dt
  
  
      #check for collision
      #x collision
      
      for tile in World.tile_list:
        if tile[1].colliderect(ball.rect.x + canonball_x, ball.rect.y, ball.width, ball.height):
          canonball_x = 0
          ball.remove(canonball_group)
          ball.add(explosion_group)
          
      #y collision
        if tile[1].colliderect(ball.rect.x, ball.rect.y + canonball_y, ball.width, ball.height):
          canonball_y = 0
          moving = False
          ball.remove(canonball_group)
          ball.add(explosion_group)
          
    #update coordinates
      if moving:
        ball.rect.x += canonball_x
        ball.rect.y += canonball_y
    for ball in explosion_group:
      ball.explode()
        
#create groups
enemy_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
checkpoint_group = pygame.sprite.Group()
exit_left_group = pygame.sprite.Group()
exit_right_group = pygame.sprite.Group()
dead_enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
held_key_group = pygame.sprite.Group()
canon_group = pygame.sprite.Group()
canonball_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

player = Player(checkpoint_x, checkpoint_y)


#load in level and create world
data = open(f'level{level}_data.json')
world_data = json.load(data)

World = world(world_data)

exit_left = Exit_left(-tile_size, 0)
exit_left_group.add(exit_left)
exit_right = Exit_right(screen_width, 0)
exit_right_group.add(exit_right)

#create buttons
restart_button = button(screen_width // 2 - 100, screen_height // 2,
                        restart_img)

start_button = button(screen_width // 2 - 100, screen_height // 2, start_img)
quit_button = button(screen_width // 2 - 50, screen_height // 2 + 100,
                     quit_img)
you_win_buttom = button(screen_width//2 - 150, screen_height // 2 - 142 ,
                        you_win_img)

edit_button = button(screen_width // 2 - 100, screen_height // 2 + 150,
                     edit_img)

main_menu_button = button(screen_width - 70, screen_height - 50, main_menu_img)
start_from_edited_button = button(screen_width //2, screen_height - 100, start_from_edited_img)

run = True
while run:

  clock.tick(FPS)
  #backgrounds
  
  if level < 2:
    bg_img = pygame.image.load(f'background-{level}.png')
  else:
    bg_img = pygame.image.load('background-0.png')
  bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    
  screen.blit(bg_img, (0, 0))
  if main_menu:
    if start_button.draw():
      level= 0
      checkpoint_x = 51
      checkpoint_y = screen_height - 52
      checkpoint_level = 0
      main_menu = False
      
    if quit_button.draw():
      run = False
      
    if start_from_edit_allowed:
      if start_from_edited_button.draw():
        path = Path(f'level{max_levels+1}_data.json')
        if path.exists():
          level = max_levels + 1
          checkpoint_level = max_levels + 1
          checkpoint_x = 51
          checkpoint_y = screen_height - 51
          main_menu = False
          Game_over = 0
          World, coin_counter = reset_level(level, coin_counter)
         
          
    if edit_allowed:
      if edit_button.draw():
        run = False
        with open("level_editor.py") as f:
          exec(f.read())
    else:
      pass

  else:
    world.draw(World)

    if Game_over == 0:

      enemy_group.update()
      canon_group.update()
      canonball_group.update()
      frame_counter += 1 
      if frame_counter > FPS:
        time_counter +=1
        frame_counter = 0
      
    held_key_group.draw(screen)
    key_group.draw(screen)
    explosion_group.draw(screen)
    canonball_group.draw(screen)
    canon_group.draw(screen)

    dead_enemy_group.draw(screen)
    enemy_group.draw(screen)
    spike_group.draw(screen)
    checkpoint_group.draw(screen)

    coin_group.draw(screen)

    exit_left_group.draw(screen)
    exit_right_group.draw(screen)

    key_group.update()
    held_key_group.update()

    explosion_group.update()
    
    (Game_over,go_back,go_forward,checkpoint_x,checkpoint_y,checkpoint_level,level,
     coin_counter) = player.update(
        Game_over, go_back, go_forward, checkpoint_x, checkpoint_y,
        checkpoint_level, level, coin_counter)

    door_group.draw(screen)
    #key delete
    
    
    #buttons
    if main_menu_button.draw():
      main_menu = True
    #coin animation and text
    for coin in coin_group:
      coin.animate()
    text_surface = my_font.render(f'{coin_counter}', False, (0, 0, 0))
    screen.blit(coin_counter_img,
                (screen_width - 200, screen_height - tile_size + 7))
    screen.blit(text_surface,
                (screen_width - 105, screen_height - tile_size + 8))

    #if player dies
    if Game_over == -1:
      
      screen.blit(darken_img, (0, 0))
      
      held_key_group.empty()
      if restart_button.draw():
        level = checkpoint_level
        death_counter += 1
        world_data = []
        World, coin_counter = reset_level(level, coin_counter)
        Game_over = 0
        

    #if player has completed the level
    if go_forward == 1:
      level += 1
      #reset game and go to next level
      if level <= max_levels:
        world_data = []
        World = go_forward_level(level)
        go_forward = 0
      else:
        #win game
        Game_over = 1
        screen.blit(yellow_img, (0, 0))
        
        stats_img = pygame.image.load('stats.png')
        stats_img = pygame.transform.scale(stats_img, (screen_height - 300, screen_height-330))
        screen.blit(stats_img,
          (screen_width // 2 - 100, 320))
        coin_count_text = my_font_small.render(f'{coin_counter}', False, (0, 0, 0))
        screen.blit(coin_count_text, (screen_width // 2 + 25, screen_height // 2 + 144))
        death_count_text = my_font_small.render(f'{death_counter}', False, (0, 0, 0))
        screen.blit(death_count_text, (screen_width // 2 + 25, screen_height // 2 + 116))
        time_count_text = my_font_small.render(f'{time_counter}', False, (0, 0, 0))
        screen.blit(time_count_text, (screen_width // 2 + 20, screen_height // 2 + 170))
        
        
        if you_win_buttom.draw():
          level = 0
          world_data = []
          World = reset_level(level, coin_counter)
          main_menu = True
          go_forward = 0
          edit_allowed = True
          start_from_edit_allowed = True
    if go_back == 1:
      level -= 1
      #reset game and go to next level
      if level >= 0:
        world_data = []
        World = go_back_level(level)
        go_back = 0
      else:
        #reset game
        level = 0
        world_data = []
        World = go_back_level(level)
        main_menu = True
        go_back = 0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()
