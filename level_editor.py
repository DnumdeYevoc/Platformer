import pygame
import json
from pathlib import Path
pygame.init()

screen_width = 1000
screen_height = 550

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

pygame.display.set_caption('level_editor')

max_levels = 1


#varibles
tile_size = 50
level = 0



#load images
next_img_ = pygame.image.load('next.png')
next_img = pygame.transform.scale(next_img_,(100, 50))
back_img_ = pygame.image.load('back.png')
back_img = pygame.transform.scale(back_img_,(100, 50))
save_img_ = pygame.image.load('save.png')
save_img = pygame.transform.scale(save_img_,(100, 50))
spike_img_ = pygame.image.load('spike.png')
spike_img = pygame.transform.scale(spike_img_,(tile_size, tile_size))
checkpoint_img_ = pygame.image.load('checkpoint-frame-1.png')
checkpoint_img = pygame.transform.scale(checkpoint_img_,(tile_size, tile_size))
enemy_img_ = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img_,(tile_size, tile_size))
coin_img_ = pygame.image.load('coin-frame-0.png')
coin_img = pygame.transform.scale(coin_img_,(tile_size//2, tile_size//2))
door_img_ = pygame.image.load('door-frame-0.png')
door_img = pygame.transform.scale(door_img_,(tile_size//2, tile_size//2))
key_img_ = pygame.image.load('key.png')
key_img = pygame.transform.scale(key_img_,(40, 17))
add_img_ = pygame.image.load('add.png')
add_img = pygame.transform.scale(add_img_,(100, 50))
delete_img_ = pygame.image.load('delete.png')
delete_img = pygame.transform.scale(delete_img_,(100, 50))
canon_img_ =  pygame.image.load('canon-frame-0.png')
canon_img = pygame.transform.scale(canon_img_,(75,75))


blank_level = Path('blank_level.json')

def write_json(data, filename):
  with open(filename, 'w') as f:
    json.dump(data, f)
 
class button ():
  def __init__(self,x,y,image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.clicked = False

  def draw(self):
    action = False
    pos = pygame.mouse.get_pos()

    if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.clicked:
        self.clicked = True
        action = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    screen.blit(self.image, self.rect)

    return action
class world():

  def __init__(self, data):
    
    self.reset(data)
  def reset(self, data):
    self.tile_list = []
    self.tile_rect_list = []
    self.clicked = False
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
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 3:
          img = pygame.transform.scale(enemy_img, (0.8*tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 2:
          img = pygame.transform.scale(spike_img, (tile_size, 0.5*tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size + tile_size //2
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 4:
          img = pygame.transform.scale(checkpoint_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 5: 
          img = pygame.transform.scale(coin_img, (tile_size//2, tile_size//2))
          img_rect = img.get_rect()
          img_rect.x = (col_count * tile_size)+ tile_size //4
          img_rect.y = (row_count * tile_size)+ tile_size // 4
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 6:
          img = pygame.transform.scale(door_img, (tile_size, tile_size))
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size
          img_rect.y = row_count * tile_size
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 7:
          img = key_img
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size +5
          img_rect.y = row_count * tile_size +15
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        if tile == 8:
          img = canon_img
          img_rect = img.get_rect()
          img_rect.x = col_count * tile_size - 9
          img_rect.y = row_count * tile_size - 25
          type = int(tile)
          Tile = (img, img_rect, type)
          self.tile_list.append(Tile)
        col_count += 1
      row_count += 1
      
    
    #change if clicked
    
    if pygame.mouse.get_pressed()[0] == 0 :
      self.clicked = False
    if pygame.mouse.get_pressed()[0] and not self.clicked and level >2:
      self.clicked = True
      r_count = 0
      for row in data_:
        c_count = 0
        for tile in row:
          tile_rect = pygame.Rect(c_count * tile_size, r_count * tile_size, tile_size, tile_size)
          
          if tile_rect.collidepoint(pygame.mouse.get_pos()):
            if tile < 8:
              row[c_count] += 1
              pygame.time.delay(100)
            else:
              row[c_count] = 0
              pygame.time.delay(100)
            
          c_count += 1
        r_count +=1
        
        
        data_source.write_text(json.dumps(data_),encoding='utf-8')
    
    

  def draw(self):
    for tile in World.tile_list:
      screen.blit(tile[0], tile[1])

#create buttons
next_button = button(screen_width - 100, screen_height - 50, next_img)
back_button = button(0, screen_height - 50, back_img)
save_button = button(screen_width// 2 - 200 , screen_height - 50, save_img)
add_button = button(screen_width - 100, screen_height - 50, add_img)
delete_button = button(screen_width//2 + 100, screen_height - 50, delete_img)

pygame.mouse.set_pos(250, screen_height)

counter = 0

run = True
pygame.time.delay(10)
while run:
  if Path(f'level{max_levels + 1}_data.json').exists():
    max_levels += 1
  clock.tick(60)
  screen.fill((202, 228, 241))
  button_bar = pygame.Surface((screen_width, 50))
  button_bar.fill((120, 110, 100))
  screen.blit(button_bar, (0, screen_height - 50))
  data_source = Path(f'level{level}_data.json')
  data_ = json.loads(data_source.read_text(encoding='utf-8'))
  data = open(f'level{level}_data.json')
  world_data =  json.load(data)
  
  World = world(world_data)
  
  World.draw()
  
  if next_button.draw():
    if level < max_levels:
      level += 1
      World.reset(world_data)
    else: 
      level = max_levels
      World.reset(world_data)
      
  if back_button.draw():
    if level > 0:
      level -= 1
      World.reset(world_data)
    else: 
      level = 0
      World.reset(world_data)

  if level == max_levels:
    if level > 3:
      if delete_button.draw():
        path = Path(f'level{level}_data.json')
        path.unlink()
        level -= 1
        max_levels -= 1
    if add_button.draw():
      counter +=1
      if counter == 2:
        max_levels += 1
        with open(blank_level, 'r') as file:
          data = json.load(file)
          write_json(data, f'level{level+1}_data.json')
        World.reset(world_data)
        counter = 0
  
  if save_button.draw():
    run = False
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  pygame.display.update()
with open("main.py") as f:
  exec(f.read())
pygame.quit()