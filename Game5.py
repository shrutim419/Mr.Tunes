import pygame
import sys
from pygame import mixer

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()
pygame.display.set_caption("Mr. Tunes")
WIDTH,HEIGHT=830,550 #define width and heigtht of our screen 
FPS=60#frames per secomd
PLAYER_VEL=5#how fast the pl move10
#define game variables
tile_size=50
score=0
scroll_thresh=100#distance the player can get before the screen starts to scroll
bg_scroll=0
screen_scroll=0
offset=0
main_menu=True
count=0
i=0
game_over = 0 
#setting up pygame window
window=pygame.display.set_mode((WIDTH,HEIGHT))
#loading images
game_bg=pygame.image.load("game_bg.jpg")
game_bg=pygame.transform.scale(game_bg,(830,550))
bg_img=pygame.image.load("wall7.png")
bg_img=pygame.transform.scale(bg_img,(2500,550))
restart_img=pygame.image.load("button_restart1.png")
restart_img=pygame.transform.scale(restart_img,(120,50))
start_img=pygame.image.load("button_start4.png")
start_img=pygame.transform.scale(start_img,(120,50))
exit_img=pygame.image.load("button_exit1.png")
exit_img=pygame.transform.scale(exit_img,(120,50))
music_image=pygame.image.load("tune12.webp")
music_image=pygame.transform.scale(music_image,(40,40))
welcome_img=pygame.image.load("welcome47.png")
welocme_img=pygame.transform.scale(welcome_img,(210,150))
#defining fonts
font_score=pygame.font.SysFont('Bauhaus 93',30)

#dfining colors
white=(255,255,255)



#load sound
pygame.mixer.music.load('music/music2.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1,0.0,5000)
coin_fx=pygame.mixer.Sound('music/coin.wav')
coin_fx.set_volume(0.8)
jump_fx=pygame.mixer.Sound('music/jump.wav')
jump_fx.set_volume(0.8)
game_over_fx=pygame.mixer.Sound('music/game_over.wav')
game_over_fx.set_volume(1)
win_fx=pygame.mixer.Sound('music/clapping2.wav')
win_fx.set_volume(0.8)

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    window.blit(img,(x,y))
    

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False
        
    def draw(self):
        action=False
        #get mouse position
        pos=pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        #checking if mouse is over that button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:#0:left 1:centre 2:right
                action=True
                self.clicked=True
                
        if pygame.mouse.get_pressed()[0]==0:#if not clicked then 0
            self.clicked=False
                
        #draw button
        window.blit(self.image,self.rect)
        return action
        
class Player:
    
    def __init__(self, x, y):
        self.reset(x,y)
        
        
    def update(self,game_over):
        dx = 0
        dy = 0
        global i
        #self.count=0
        screen_scroll=0
        walk_cooldown = 5
        if (game_over==0):
    		#get keypresses
            key = pygame.key.get_pressed()
            if ((key[pygame.K_UP] or key[pygame.K_w]) and (self.jumped == False) and (self.in_air==False)):
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if (key[pygame.K_UP] or key[pygame.K_w] == False):
                self.jumped = False
            if (key[pygame.K_LEFT] or key[pygame.K_a]):
                dx -= 5
                self.counter += 1
                self.direction = -1
            if (key[pygame.K_RIGHT] or key[pygame.K_d]):
                dx += 5
                self.counter += 1
                self.direction = 1
            if ((key[pygame.K_LEFT]or key[pygame.K_a]) == False and (key[pygame.K_RIGHT] or key[pygame.K_d])== False):
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if (key[pygame.K_t]):
                player.change_height(30, 50)
    
            if(key[pygame.K_s] or key[pygame.K_DOWN]):
                player.change_height(50, 90)
                
            
    
    		#handle animation
            if self.counter > walk_cooldown:
                self.counter = 0	
                self.index += 1#relooping
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
    
    
    		#add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
    		#check for collision
            self.in_air=True
            
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
            
            
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
    			#check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
    				#check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
    				#check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jump_count=0
                        self.in_air=False
            #check for collision with enemies
            if pygame.sprite.spritecollide(self,blob_group,False):
                game_over_fx.play()
                game_over=-1
                
            if pygame.sprite.spritecollide(self,spike_group,False):
                game_over_fx.play()
                game_over=-1
            
            if score==15 and pygame.sprite.spritecollide(self,exit_group,False):
                win_fx.play()
                game_over=1 


    		#update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            


                # Update the player's position
            if (self.rect.right > WIDTH - scroll_thresh) or (self.rect.left < WIDTH - scroll_thresh):
                self.rect.x -= dx
                screen_scroll = -dx
            for blob in blob_group:
                blob.rect.x += screen_scroll
            for spike in spike_group:
                spike.rect.x += screen_scroll
            for coin in coin_group:
                coin.rect.x += screen_scroll
            for ext in exit_group:
                ext.rect.x += screen_scroll
                 
 
        if game_over==-1:
             self.image=self.dead_image
             if self.rect.y>250:
                 self.rect.y-=5
             
             
        if self.rect.bottom > HEIGHT:
                game_over_fx.play()
                self.rect.bottom = HEIGHT
                game_over=-1
                dy = 0
		#draw player onto screen
        window.blit(self.image, self.rect)
        
        return game_over,screen_scroll
    
    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.jump_count=0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (50, 90))
            img_left = pygame.transform.flip(img_right, True, False)  # flip(img,x,y)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image=pygame.image.load("ghost.png")
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1  # 1:right -1:left
        self.in_air=True


    def change_height(self,x,y):
        for num in range(1, 5):
            self.images_right=[]
            self.images_left=[]
            for num in range(1, 5):
                img_right = pygame.image.load(f'guy{num}.png')
                img_right = pygame.transform.scale(img_right, (x ,y))
                img_left = pygame.transform.flip(img_right, True, False)  # flip(img,x,y)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.width = self.image.get_width()
            self.height = self.image.get_height()


class World():
    def __init__(self,data):
        self.level_length=len(data[0])
        self.tile_list = []
        #load images
        dirt_img=pygame.image.load('dirt57.png')
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
                if tile==3:
                    blob=Enemy(col_count*tile_size,row_count*tile_size+15)#x,y
                    blob_group.add(blob)
                if tile==6:
                    spike=Spike(col_count*tile_size,row_count*tile_size+(tile_size//2))
                    spike_group.add(spike)
                if tile==7:
                    coin=Coin(col_count*tile_size,row_count*tile_size+(tile_size//2))
                    coin_group.add(coin)
                if tile==8:
                    ext=Exit(col_count*tile_size,row_count*tile_size+10)
                    exit_group.add(ext)
                col_count += 1
            row_count += 1
            
            
    def draw(self,offset_x):
        for tile in self.tile_list:
            tile[1][0]+=offset_x
            window.blit(tile[0],tile[1])#image and position

            
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("blob.png")
        self.rect=self.image.get_rect()
        self.rect.x= x
        self.rect.y= y  
        self.move_direction=1
        self.move_counter=0
        
        
    def update(self):
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if abs(self.move_counter)>70:
            self.move_direction *=-1
            self.move_counter *=-1
            

class Spike(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load("spike1.png")
        self.image=pygame.transform.scale(img,(tile_size,tile_size//2))        
        self.rect=self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        


class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load("tune12.webp")
        self.image=pygame.transform.scale(img,(40,40))        
        self.rect=self.image.get_rect()
        self.rect.center= (x,y)
        
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load("exit.png")
        self.image=pygame.transform.scale(img,(tile_size,int(tile_size*1.5)))        
        self.rect=self.image.get_rect()
        self.rect.center= (x,y)
        
        
    


            
world_data =[
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 1, 0, 0, 0, 7, 3, 0, 0, 0, 0], 
[1, 1, 0, 1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0], 
[1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 7, 8], 
[1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0], 
[1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
[1, 1, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 1, 7, 0, 0, 0, 0, 0, 0 ,7, 0, 0, 0, 7, 1, 0, 0, 0, 0], 
[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0], 
]


blob_group=pygame.sprite.Group()  
spike_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()

world=World(world_data)       

#create button
restart_button=Button(WIDTH//2-180,HEIGHT//2,restart_img)
start_button=Button(WIDTH//2-180,HEIGHT//2,start_img)
exit_button=Button(WIDTH//2+70,HEIGHT//2,exit_img)


clock=pygame.time.Clock()
player = Player(100, HEIGHT - 400)
run=True
while run:
    clock.tick(FPS)
    window.blit(game_bg,(0,0))
    if main_menu==True:
        window.blit(welcome_img,(300,100))
        if exit_button.draw():
            run=False
        
        if start_button.draw():
            main_menu=False
        
    else:
        window.blit(bg_img,(0-bg_scroll,0))
        world.draw(offset)
        if(game_over==0):
            blob_group.update()
            #update score
            #check if a coin has been collected
            if pygame.sprite.spritecollide(player,coin_group, True):
                coin_fx.play()
                score+=1
                
            #window.blit(music_image,(music_symbol_x+offset+3, music_symbol_y))
            draw_text("Score: "+str(score),font_score,white,40,10)
            


        
        spike_group.draw(window,offset)        
        blob_group.draw(window)
        coin_group.draw(window)
        exit_group.draw(window)
        game_over,offset=player.update(game_over)
        bg_scroll-=offset
       
        
        #if player dead
        if game_over==-1:
            draw_text("Game Over !!!!",font_score,(255,0,0),WIDTH//2-90,HEIGHT//2-160)
            pygame.draw.rect(window,white, pygame.Rect(WIDTH//2-90, HEIGHT//2-120, 200, 85),  5)
            draw_text("Your Score: "+str(score),font_score,white,WIDTH//2-90,HEIGHT//2-100)
            
            offset=0
            if restart_button.draw()==True:
                bg_scroll=0
                blob_group.empty()
                coin_group.empty()
                spike_group.empty()
                exit_group.empty()
                del world
                world=World(world_data)
                world.draw(offset)
                player.reset(100,HEIGHT-400)
                game_over=0
                score=0
            if exit_button.draw()==True:
                player.reset(100, HEIGHT - 400)
                main_menu=True
        
        if game_over==1:
            draw_text("You Win !!!!",font_score,(0,255,0),WIDTH//2-90,HEIGHT//2-160)
            pygame.draw.rect(window,white, pygame.Rect(WIDTH//2-90, HEIGHT//2-120, 200, 85),  5)
            draw_text("Your Score: "+str(score),font_score,white,WIDTH//2-90,HEIGHT//2-100)
            
            offset=0
            if restart_button.draw()==True:
                bg_scroll=0
                blob_group.empty()
                coin_group.empty()
                spike_group.empty()
                exit_group.empty()
                del world
                world=World(world_data)
                world.draw(offset)
                player.reset(100,HEIGHT-400)
                game_over=0
                score=0
            if exit_button.draw()==True:
                player.reset(100, HEIGHT - 400)
                main_menu=True
            
    pygame.display.update()

        
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:#event of pressing the red X
            run=False
            break
        
    
        
pygame.quit()#actually closes the screen
sys.exit()