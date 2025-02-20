import os
import random
import math
import pygame
import sys
from os import listdir
from os.path import isfile,join
pygame.init() #intilize the pygame

pygame.display.set_caption("Platform 3.0")#sets the caption at the top of the window

BG_COLOR=(128,128,128)#set back ground color
WIDTH,HEIGHT=800,600 #define width and heigtht of our screen 
FPS=60#frames per secomd
PLAYER_VEL=7#how fast the pl move10
tile_size=50

#setting up pygame window
window=pygame.display.set_mode((WIDTH,HEIGHT))
#to image in left or right.....x direction, y direction...true: false
def flip(sprites):
    return [pygame.transform.flip(sprite,True,False) for sprite in sprites]
#load different spite sheet for our charater
def load_sprite_sheets(width,height,direction=False):
    path="Character"
    images=[f for f in listdir(path) if isfile(join(path, f))]#load all images(sprites)
    all_sprites={}

    for image in images:
        sprite_sheet=pygame.image.load(join(path,image)).convert_alpha()#convert alpha gives transparent image.....load individual sprites
        sprites=[]
        for i in range (sprite_sheet.get_width()//width):
            surface=pygame.Surface((width,height),pygame.SRCALPHA, 32)#SRCALPHA loads  transparent image and 32 is the depth loading individual images
            rect=pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet,(0,0),rect)#blit means draw
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png","")+"_right"]=sprites
            all_sprites[image.replace(".png","")+"_left"]=flip(sprites)
        else:
            all_sprites[image.replace(".png","")]=sprites
            
    return all_sprites

'''def get_block(size):
    path=join("Terrain","Terrain.png")
    image=pygame.image.load(path).convert_alpha()
    surface=pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect=pygame.Rect(96,0,size,size)#change xmy for different block
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale(surface,(50,50))'''
        
class Player(pygame.sprite.Sprite):
    color=(128,0,128)
    GRAVITY=1
    SPRITES=load_sprite_sheets(32,32,True)
    ANIMATION_DELAY=1
    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
       #x and y denote how fast players are moving in x and y frame 
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        #self.direction='center'
        self.direction='right'
        self.animation_count=0
        self.fall_count=0
        self.jump_count=0
        
    def jump(self):
        self.y_vel=-self.GRAVITY*8#8 is speed  of jump
        self.animation_count=0
        self.jump_count+=1
        if self.jump_count==1:
            self.fall_count=0   
        
       
    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
    
    def move_left(self,vel):
        self.x_vel=-vel
        if self.direction!='left':
            self.direction='left'
            self.animation_count=0
        
    def move_right(self,vel):
        self.x_vel=vel
        if self.direction!='right':
            self.direction='right'
            self.animation_count=0
    
    def loop(self,fps):#called once every frame...move character in correct direction....every thing our charater needs to do constantly
        self.move(self.x_vel,self.y_vel)
        #
        self.y_vel+=min(1,(self.fall_count/fps)*self.GRAVITY)#Gravty is defined here
        self.fall_count+=1
        self.update_sprite()
        
   
    def landed(self):
        self.fall_count=0#setting gravity to zero
        self.y_vel=0
        self.jump_count=0

    def hit_head(self):
        self.count=0
        self.y_vel+=-1
        
    def update_sprite(self):
        sprite_sheet="idle"#default sprite sheet
        if self.y_vel<0:
            if self.jump_count==1:
                spite_sheet="jump"
            elif self.jump_count==2:
                sprite_sheet="double_jump"
        elif self.y_vel> self.GRAVITY*2:
            sprite_sheet="fall"
        elif self.x_vel !=0:
            sprite_sheet="run"
        
        sprite_sheet_name=sprite_sheet+"_"+self.direction
        sprites=self.SPRITES[sprite_sheet_name]
        sprite_index=self.animation_count//self.ANIMATION_DELAY%len(sprites)
        self.sprite=sprites[sprite_index]
        self.animation_count+=1
        self.update()
        
        
    def update(self):
        self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask=pygame.mask.from_surface(self.sprite)
        
        
        
    def draw(self,win,offset_x):#make rectangle
        win.blit(self.sprite,(self.rect.x-offset_x,self.rect.y))
            #pygame.draw.rect(win,self.color,self.rect)
class Object(pygame.sprite.Sprite):#base class for all objects so that collision would be uniform
    def __init__(self,x,y,width,height,name=None):
        super().__init__()#initialize constructor
        self.rect=pygame.Rect(x,y,width,height)
        self.image=pygame.Surface((width,height),pygame.SRCALPHA)
        self.width=width
        self.height=height
        self.name=name
        
    def draw(self,win,offset_x):
        win.blit(self.image,(self.rect.x-offset_x,self.rect.y))

class Block(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size)#x,y,width,height
        block=get_block(size)
        self.image.blit(block,(0,0))
        self.mask=pygame.mask.from_surface(self.image)




def draw(window,player,objects,offset_x):

    clouds=pygame.image.load("wall5.png")
    window.blit(clouds,(0,0))
    for obj in objects:
        obj.draw(window,offset_x)
        
    player.draw(window,offset_x)
    pygame.display.update()
    
    
def handle_vertical_collision(player,objects,dy):
    collided_objects=[] 
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):#if two objects are colliding 
            if dy>0:
                player.rect.bottom=obj.rect.top#player bottom= object top.....going down
                player.landed()
            elif dy<0:
                player.rect.top=obj.rect.bottom#going up
                player.hit_head()
        collided_objects.append(obj)#so we know what object did we collide
        
def collide(player,objects,dx):
    player.move(dx,0)
    player.update()
    collided_object=None
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            collided_object=obj;
            break
    player.move(-dx,0)
    player.update()
    return collided_object

def handle_move(player,objects):
    keys=pygame.key.get_pressed()
    
    player.x_vel=0#if not player moves in same direction untill set back to zero
    collide_left=collide(player,objects,-PLAYER_VEL*2)
    collide_right=collide(player,objects,PLAYER_VEL*2)
    
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
        
    if self.rect.bottom > HEIGHT:
        self.rect.bottom =HEIGHT
        dy= 0    
    
    handle_vertical_collision(player, objects,player.y_vel)

class World():
    def __init__(self,data):
        self.tile_list = []
        #load images
        dirt_img=pygame.image.load('Terrain2.png')
        row_count=0 
        for row in data:
            col_count=0
            for tile in row:
                if tile==1:
                    img=pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0],tile[1])
            
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 7, 1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 1, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



def main(window):
    clock=pygame.time.Clock()
    def draw_grid():
        	for line in range(0, 20):
        		pygame.draw.line(window, (255, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
        		pygame.draw.line(window, (255, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))
          
    block_size=96
    player=Player(100,100,60,60)#x y width height
    #floor=[Block(i*block_size,HEIGHT-block_size,block_size) 
     #      for i in range(-WIDTH//block_size,(WIDTH*2)//block_size)]#block in left and right
    #place=[Block(i*block_size,200,block_size) for i in range(-15,-5)]#block in left and right
    #objects=[*floor,Block(0,HEIGHT-block_size*2,block_size),Block(block_size*3,HEIGHT-block_size*4,block_size),
     #        Block(block_size*2,HEIGHT-block_size*4,block_size),Block(block_size*-11,HEIGHT-block_size*3,block_size),
     #        Block(block_size*-12,HEIGHT-block_size*3,block_size),Block(block_size*-13,HEIGHT-block_size*3,block_size),
      #       Block(block_size*-14,HEIGHT-block_size*3,block_size)]
    world=World(world_data)
    offset_x=0
    scroll_area_width=200
    run=True
    while run:
        clock.tick(FPS)
        world.draw()
        draw_grid()
        pygame.display.update()
         
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#event of pressing the red X
                run=False
                break
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP and player.jump_count<2:
                    player.jump()
        player.loop(FPS)
        handle_move(player),)#,place)
        draw(window,player,objects,offset_x)#,place)
        
        if((player.rect.right-offset_x>=WIDTH-scroll_area_width and player.x_vel>0) or
           (player.rect.left-offset_x<=scroll_area_width and player.x_vel<0)):#checking if the player has crossed a specific boundry  and checking if player is moving to the right 
            offset_x+=player.x_vel
    pygame.quit()#actually closes the screen
    sys.exit()

    
    
 #so that we call the main function only if we are running the code directly
if __name__=="__main__":
    main(window)
    
    
    