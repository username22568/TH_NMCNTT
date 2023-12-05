import pygame, sys, time, random, os
import tkinter as tk
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
FPS = 120
fpsClock = pygame.time.Clock()

#Cửa sổ game
screen_size=(1280,720)

#Thêm background
bg=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg3.jpg'),screen_size)
road=pygame.transform.scale(pygame.image.load(r'MainGame\Image\road.jpg'),(1280,400))
start_road=pygame.transform.scale(pygame.image.load(r'MainGame\Image\start_road.jpg'),(1280,400))
finish_road=pygame.transform.scale(pygame.image.load(r'MainGame\Image\finish_road.jpg'),(1280,400))
end_bg=1000
start_bg=200
#Maps
map1=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg1.jpg'),(1280,720))
map2=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg2.jpg'),(1280,720))
map3=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg3.jpg'),(1280,720))
map4=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg4.jpg'),(1280,720))
map5=pygame.transform.scale(pygame.image.load(r'MainGame\Image\bg5.jpg'),(1280,720))
pick_map1=pygame.transform.scale(pygame.image.load(r'MainGame\Image\pick_bg1.jpg'),(400,300))
pick_map2=pygame.transform.scale(pygame.image.load(r'MainGame\Image\pick_bg2.jpg'),(400,300))
pick_map3=pygame.transform.scale(pygame.image.load(r'MainGame\Image\pick_bg3.jpg'),(400,300))
pick_map4=pygame.transform.scale(pygame.image.load(r'MainGame\Image\pick_bg4.jpg'),(400,300))
pick_map5=pygame.transform.scale(pygame.image.load(r'MainGame\Image\pick_bg5.jpg'),(400,300))
maps=[map1,map2,map3,map4,map5]
pick_maps=[pick_map1,pick_map2,pick_map3,pick_map4,pick_map5]

#Load ảnh xe
car_pic2=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car.jpg'),(150,150))
car_pic1=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car.jpg'),(150,150))
item_pic=pygame.image.load(r'MainGame\Image\item.png')
#Thêm âm thanh
flash_sound=pygame.mixer.Sound(r'MainGame\Sound\Effect\flash.mp3')
back_sound=pygame.mixer.Sound(r'MainGame\Sound\Effect\back.mp3')
tele_sound=pygame.mixer.Sound(r'MainGame\Sound\Effect\teleport.mp3')
#Nhạc

#Màu
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
#Tham số
current_money=20000
#Set font
font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)
new_font = pygame.font.SysFont("Arial", 30, bold=True, italic=False)
name_font=pygame.font.SysFont("Calibri Light", 30, bold=False, italic=False)
#Hàm
#Vẽ chữ
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x,y)
    surface.blit(text_obj, text_rect)      
def screen_resize(new_screen_size):
    screen = pygame.display.set_mode(new_screen_size,pygame.RESIZABLE)  
#Class
class User():
    def __init__(self,username):
        self.money = current_money
        self.htr_in = 1
        self.hrt = ''
        self.username=username
        #Tạo đường dẫn
        self.path='MainGame/'+self.username+'_history'
    def create_player_history(self):#tạo một lần duy nhất cho 1 user
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)
    def history_saved(self,screen):
        self.image_file = self.path + '/history'+str(self.htr_in)+'.png'
        pygame.image.save(screen,self.image_file)
        self.htr_in +=1
    def money_update(self,player):
        if player.rank == 1:
            self.money += 5000
        if player.rank == 2:
            self.money += 2000
        else:
            self.money -= 1000
    def money_change(self,dif):
        self.money+=dif
class Car():
    name=''
    color=(0,0,0)
    def __init__(self,screen,image,lane,buff_speed=False,better_start=False):
        self.image=image
        self.y=280+(lane-1)*80
        self.buff_speed=buff_speed
        self.better_start=better_start
        self.screen=screen
    def draw(self,x,rank):
        self.x=x
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.screen.blit(self.image,self.rect)
        self.rank=rank
    def is_in(self,x,y):
        if self.x>=x-50 and self.x<=x+50 and self.y==y:
            return True
    def finish(self):
        if self.x>=end_bg:
            return True
    def check_ranked(self):
        if self.finish() and self.rank==0:
            return True
        if self.rank>0:
            return False
class Item():
    image=item_pic
    exist=False
    def __init__(self):
        pass
    def draw(self,x,y,screen):
        self.screen=screen
        self.rect=self.image.get_rect(center=(x,y))
        self.screen.blit(self.image,self.rect)
    def affect(self,x):
        self.type=random.randint(0,4)
        if self.type==0 or self.type==2:
            x-=100
            pygame.mixer.Channel(4).play(back_sound)
        elif self.type==1 or self.type==3:
            x+=100
            pygame.mixer.Channel(5).play(flash_sound)
        else:
            pass
            pygame.mixer.Channel(6).play(tele_sound)
        return x
    
class Buttons():
    def __init__(self,height,width,image,x,y,screen):
        self.height=height
        self.width=width
        self.img=pygame.transform.scale(image,(height,width))
        self.x=x
        self.y=y
        self.rect=self.img.get_rect()
        self.screen=screen
    def draw(self):
        self.rect.topleft=(self.x,self.y)
        self.screen.blit(self.img,self.rect)
    def is_in(self,x,y):
        if x>self.x and x<self.x+self.height and y>self.y and y<self.y+self.width:
            return True



#Vào đua
def run_game(map_index,player_pic,com1_pic,com2_pic,com3_pic,com4_pic,buff_speed,better_start,user,player_name,screen):
    #Khởi tạo xe 
    player=Car(screen,player_pic,2,buff_speed,better_start)
    com1=Car(screen,com1_pic,1)
    com2=Car(screen,com2_pic,3)
    com3=Car(screen,com3_pic,4)
    com4=Car(screen,com4_pic,5)
    player.name = player_name
    com1.name = 'com'
    com2.name ='com'
    com3.name ='com'
    com4.name ='com'
    bg=maps[map_index]
    #Khởi tạo biến item
    item1=Item()
    item2=Item()
    enough_item=False
    num_item=0
    #Các tham số
    if player.better_start:
        player_x=start_bg+100
    else:
        player_x=start_bg
    if player.buff_speed:
        max_speed=25
    else:
        max_speed=20
    max_com=20
    com1_x=start_bg
    com2_x=start_bg
    com3_x=start_bg
    com4_x=start_bg
    player_rank=0
    com1_rank=0
    com2_rank=0
    com3_rank=0
    com4_rank=0
    running=True
    bg_x=0
    road_x=0
    rank=1
    ranked=False
    check_rank = True
    road_finish=False
    road_time=0    
    #Vòng lặp game
    start=False
    while running:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                start=True
        screen.blit(bg,(bg_x,0))
        #Vẽ đường
        if road_time==0:
            screen.blit(start_road,(road_x,240))
            screen.blit(road,(road_x+1280,240))
        elif road_time>=10:
            screen.blit(finish_road,(road_x,240))
        else:
            screen.blit(road,(road_x,240))
            screen.blit(road,(road_x+1280,240))
        road_speed=5
        #Vẽ xe
        player.draw(player_x,player_rank)
        com1.draw(com1_x,com1_rank)
        com2.draw(com2_x,com2_rank)
        com3.draw(com3_x,com3_rank)
        com4.draw(com4_x,com4_rank)
        #Cho đường chạy
        if start:
            if not(road_finish):
                road_x-=road_speed
                if road_x<-1280:
                    road_x=0
                    road_time+=1
                if road_time==10:
                    road_finish=True
            else:
                road_speed=0
                    
        #Cập nhật toạ độ cho xe
            if player_x<0:
                player_x=0
            if com1_x<0:
                com1_x=0
            if com2_x<0:
                com2_x=0
            if com3_x<0:
                com3_x=0
            if com4_x<0:
                com4_x=0
            #Nếu đường đã chạy hết
            if road_finish:
                if not(player.finish()):
                    player_x+=random.randint(0,max_speed)
                    if player_x>1100:
                        player_x=1100
                if not(com1.finish()):
                    com1_x+=random.randint(0,max_com)
                    if com1_x>1100:
                        com1_x=1100
                if not(com2.finish()):
                    com2_x+=random.randint(0,max_com)
                    if com2_x>1100:
                        com2_x=1100
                if not(com3.finish()):
                    com3_x+=random.randint(0,max_com)
                    if com3_x>1100:
                        com3_x=1100
                if not(com4.finish()):
                    com4_x+=random.randint(0,max_com)
                    if com4_x>1100:
                        com4_x=1100
            
            #Đưa item vào
            if not(enough_item): #Nếu chưa đủ 2 item đang xuất hiện
                #Nếu item 1 chưa xuất hiện
                if not(item1.exist):
                    lane_item1=random.randint(1,5)
                    item1_y=280+(lane_item1-1)*80
                    item1_x=random.randint(600,1000)
                    if item1_x<end_bg:
                        item1.exist=True
                        num_item+=1
                #Vẽ item 1
                if item1.exist:
                    item1.draw(item1_x,item1_y,screen)
                    item1_x-=road_speed
                    if item1_x<0:
                        item1.exist=False
                        num_item-=1
                    #Xử lý nếu xe chạm vào item
                    if player.is_in(item1_x,item1_y):
                        player_x=item1.affect(player_x)
                        num_item-=1
                        item1.exist=False
                    if com1.is_in(item1_x,item1_y):
                        com1_x=item1.affect(com1_x)
                        num_item-=1
                        item1.exist=False
                    if com2.is_in(item1_x,item1_y):
                        com2_x=item1.affect(com2_x)
                        num_item-=1
                        item1.exist=False
                    if com3.is_in(item1_x,item1_y):
                        com3_x=item1.affect(com3_x)
                        num_item-=1
                        item1.exist=False
                    if com4.is_in(item1_x,item1_y):
                        com4_x=item1.affect(com4_x)
                        num_item-=1
                        item1.exist=False
                #Tương tự với item 2
                if not(item2.exist):
                    lane_item2=random.randint(1,5)
                    item2_y=280+(lane_item2-1)*80
                    item2_x=random.randint(600,1000)
                    if item2_x<end_bg and item2_y!=item1_y:
                        item2.exist=True
                        num_item+=1
                if item2.exist:
                    item2.draw(item2_x,item2_y,screen)
                    item2_x-=road_speed
                    if item2_x<0:
                        item2.exist=False
                        num_item-=1

                    if player.is_in(item2_x-50,item2_y):
                        player_x=item2.affect(player_x)
                        num_item-=1
                        item2.exist=False
                    if com1.is_in(item2_x-50,item2_y):
                        com1_x=item2.affect(com1_x)
                        num_item-=1
                        item2.exist=False
                    if com2.is_in(item2_x-50,item2_y):
                        com2_x=item2.affect(com2_x)
                        num_item-=1
                        item2.exist=False
                    if com3.is_in(item2_x-50,item2_y):
                        com3_x=item2.affect(com3_x)
                        num_item-=1
                        item2.exist=False
                    if com4.is_in(item2_x-50,item2_y):
                        com4_x=item2.affect(com4_x)
                        num_item-=1
                        item2.exist=False
                #Nếu đã đủ 2 item -> không thêm item nữa
                if num_item>2:
                    enough_item=True
                else:
                    enough_item=False
        #Xếp hạng
            if player.check_ranked():
                player_rank=rank
                rank+=1
            if com1.check_ranked():
                com1_rank=rank
                rank+=1
            if com2.check_ranked():
                com2_rank=rank
                rank+=1
            if com3.check_ranked():
                com3_rank=rank
                rank+=1
            if com4.check_ranked():
                com4_rank=rank
                rank+=1
            #Kết thúc
            if (player.finish() and com1.finish() and com2.finish() and com3.finish() and com4.finish()) and road_finish:
                start=False
                ranked=True
            # bảng xếp hạng
        if ranked:
            check_rank = ranked_rs(r'MainGame\Image\item.png',screen_size[0]/2,4*screen_size[1]/5,player,com1,com2,com3,com4,user,screen)

        pygame.display.update()
        #thoát ra menu
        if check_rank ==False:
            break
    return player_rank
def shopping(screen,user):
    #Khởi tạo nút
    buy_buff_speed=Buttons(200,100,car_pic1,340,360,screen)
    buy_better_start=Buttons(200,100,car_pic1,740,360,screen)
    quit_bt=Buttons(200,100,item_pic,540,570,screen)
    #Tham số
    buff_speed=False
    better_start=False
    #Vòng lặp
    running_shop=True
    while running_shop:
        spot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if buy_buff_speed.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    buff_speed=True
                    user.money_change(-2000)
                    buy_buff_speed.img=item_pic
                if buy_better_start.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    better_start=True
                    user.money_change(-2000)
                    buy_better_start.img=item_pic
                if quit_bt.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    running_shop=False
            if buy_buff_speed.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif buy_better_start.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif quit_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
        screen.fill(black)
        buy_better_start.draw()
        buy_buff_speed.draw()
        quit_bt.draw()
        pygame.display.update()
    return (buff_speed,better_start)
def set_name(screen):
    sname=""
    count = 0
    name=True
    type_name =False
    name_gap = Buttons(19*screen_size[0]/40,screen_size[1]/12,item_pic,screen_size[0]/4,3*screen_size[1]/4,screen)
    accept_bt = Buttons(screen_size[1]/12,screen_size[1]/12,item_pic,29*screen_size[0]/40,3*screen_size[1]/4,screen)
    while name:
        count +=1
        if (count // 150) % 2 == 0:
            name_dis = sname + '_'
        else:
            name_dis = sname
        spot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==MOUSEBUTTONDOWN:
                if accept_bt.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    name = False
                    return sname
                if name_gap.is_in(spot[0],spot[1]):
                    type_name = True
            if type_name == True and event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    sname = sname[:-1]
                elif event.key == K_RETURN:
                    name = False
                    return sname
                else:
                    sname += event.unicode
            if name_gap.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_IBEAM)
            elif accept_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
        screen.fill(black)
        name_gap.draw()
        screen.fill(white,name_gap.rect)
        accept_bt.draw()
        if type_name:
            text_obj = font.render(name_dis,1,black)
            text_rect = text_obj.get_rect(topleft = (screen_size[0]/4,3*screen_size[1]/4))
            screen.blit(text_obj,text_rect)
        else:
            text_obj = font.render('Enter car\'s name here',1,(190,190,190))
            text_rect = text_obj.get_rect(topleft = (screen_size[0]/4,3*screen_size[1]/4))
            screen.blit(text_obj,text_rect)
        pygame.display.flip()
        pygame.display.update()
    

def pick_map(buff_speed,buff_start,current_user,player_name,char,screen):
    pick_bt=Buttons(200,100,item_pic,540,570,screen)
    next_bt=Buttons(100,100,item_pic,980,340,screen)
    back_bt=Buttons(100,100,item_pic,200,340,screen)
    index=0
    run_map=True
    while run_map:
        spot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==MOUSEBUTTONDOWN:
                if pick_bt.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    run_map=False
                    run_game(index,car_pic2,car_pic2,car_pic2,car_pic2,car_pic2,buff_speed,buff_start,current_user,player_name,screen)
                if next_bt.is_in(spot[0],spot[1]):
                    index+=1
                    if index>4:
                        index=0
                if back_bt.is_in(spot[0],spot[1]):
                    index-=1
                    if index<0:
                        index=4
            if pick_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif next_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif back_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
        pick_bt.draw()
        next_bt.draw()
        back_bt.draw()
        screen.blit(pick_maps[index],(440,210))
        pygame.display.update()

def pick_char(screen):
    pick1=Buttons(200,200,item_pic,280,160,screen)
    pick2=Buttons(200,200,item_pic,540,160,screen)
    pick3=Buttons(200,200,item_pic,800,160,screen)
    pick4=Buttons(200,200,item_pic,410,400,screen)
    pick5=Buttons(200,200,item_pic,670,400,screen)
    return_bt=Buttons(150,150,item_pic,0,0,screen)
    accept=0
    index=0
    run_map=True
    while run_map:
        spot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==MOUSEBUTTONDOWN:
                if accept==0:
                    if pick1.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        index=1
                        accept+=1
                    if pick2.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        index=2
                        accept+=1
                    if pick3.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        index=3
                        accept+=1
                    if pick4.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        index=4
                        accept+=1
                    if pick5.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        index=5
                        accept+=1
                elif accept==1:
                    if pick1.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        return 5*(index-1)
                    if pick2.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        return 5*(index-1)+1
                    if pick3.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        return 5*(index-1)+2
                    if pick4.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        return 5*(index-1)+3
                    if pick5.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        return 5*(index-1)+4
                    if return_bt.is_in(spot[0],spot[1]):
                        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                        accept-=1
                        index=0
            if pick1.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif pick2.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif pick3.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif pick4.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif pick5.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
        if index==0:
            pick1.img=item_pic
            pick2.img=item_pic
            pick3.img=item_pic
            pick4.img=item_pic
            pick5.img=item_pic
        if index==1:
            pick1.img=car_pic1
            pick2.img=car_pic1
            pick3.img=car_pic1
            pick4.img=car_pic1
            pick5.img=car_pic1
        if index==2:
            pick1.img=car_pic1
            pick2.img=car_pic1
            pick3.img=car_pic1
            pick4.img=car_pic1
            pick5.img=car_pic1
        if index==3:
            pick1.img=car_pic1
            pick2.img=car_pic1
            pick3.img=car_pic1
            pick4.img=car_pic1
            pick5.img=car_pic1
        if index==4:
            pick1.img=car_pic1
            pick2.img=car_pic1
            pick3.img=car_pic1
            pick4.img=car_pic1
            pick5.img=car_pic1
        if index==5:
            pick1.img=car_pic1
            pick2.img=car_pic1
            pick3.img=car_pic1
            pick4.img=car_pic1
            pick5.img=car_pic1
        screen.fill(black)
        pick1.draw()
        pick2.draw()
        pick3.draw()
        pick4.draw()
        pick5.draw()
        if accept==1:
            return_bt.draw()
        pygame.display.update()

#Sảnh chờ
def main_menu(username):
    current_user = User(username)
    current_user.create_player_history()
    screen=pygame.display.set_mode(screen_size,pygame.RESIZABLE)
    pygame.display.set_caption("Car Bet")
    icon=pygame.image.load(r'MainGame\Image\car.jpg')
    pygame.display.set_icon(icon)
    #Khởi tạo nút
    profile_bt = Buttons(200,100,item_pic,20,20,screen)
    start_bt=Buttons(200,100,item_pic,540,570,screen)
    shop_bt=Buttons(100,100,item_pic,50,570,screen)
    buff=(False,False)
    char=-1
    player_name='2'
    running_menu=True
    #Vòng lặp
    while running_menu:
        #Lấy tọa độ chuột
        spot = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            #Thay đổi kích thước màn hình
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==pygame.MOUSEBUTTONDOWN:
                #Xử lý thao tác trên các nút
                if start_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    char=pick_char(screen)
                    player_name = set_name(screen)
                    if char>=0:
                        pick_map(buff[0],buff[1],current_user,player_name,char,screen)
                    running_menu=True
                if shop_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    #đổi lại hình dạng chuột ban đầu sau khi click
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    buff=shopping(screen,current_user)
                    running_menu=True
                if profile_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    profile_display(current_user,screen)
                    running_menu=True
            #Thay đổi hình dạng chuộtchuột
            if start_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif shop_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif profile_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
        screen.fill(black)
        #Vẽ nút
        profile_bt.draw()
        shop_bt.draw()
        start_bt.draw()
        pygame.display.update()

def ranked_rs(image,width,height,player,com1,com2,com3,com4,user,screen):
    rank_img = pygame.transform.scale(pygame.image.load(image),(width,height))
    rank_rect = rank_img.get_rect(topleft=(screen_size[0]/4,screen_size[1]/10))
    running_rank = True
    home_bt = Buttons(screen_size[0]/16,screen_size[1]/8,item_pic,screen_size[0]/4,9*screen_size[1]/10,screen)
    save_bt = Buttons(screen_size[0]/16,screen_size[1]/8,item_pic,3*screen_size[0]/4,9*screen_size[1]/10,screen)
    lt = [player,com1,com2,com3,com4]
    #Cập nhật tiền 
    user.money_update(player)
    # sắp xếp thứ tự xếp hạng
    j=0
    while j < len(lt):
        i=j
        sw=False
        while i < len(lt)-1:
            if lt[i].rank > lt[i+1].rank :
                sw = True
                temp=lt[i]
                lt[i]=lt[i+1]
                lt[i+1]=temp
            i+=1
        if sw == False:
            break
    while running_rank:
        spot=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                new_screen_size = event.dict["size"]
                screen_resize(new_screen_size)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if home_bt.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    running_rank = False
                if save_bt.is_in(spot[0],spot[1]):
                    user.history_saved(screen)
            if home_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            elif save_bt.is_in(spot[0],spot[1]):
                pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
            else :
                pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)


        screen.blit(rank_img,rank_rect)
        #vẽ nút
        home_bt.draw()
        save_bt.draw()
        draw_text('1',new_font,black,screen,screen_size[0]/4+screen_size[0]/40,3*screen_size[1]/20)
        draw_text('2',new_font,black,screen,screen_size[0]/4+screen_size[0]/40,6*screen_size[1]/20)
        draw_text('3',new_font,black,screen,screen_size[0]/4+screen_size[0]/40,9*screen_size[1]/20)
        draw_text('4',new_font,black,screen,screen_size[0]/4+screen_size[0]/40,12*screen_size[1]/20)
        draw_text('5',new_font,black,screen,screen_size[0]/4+screen_size[0]/40,15*screen_size[1]/20)
        draw_text(lt[0].name,new_font,lt[0].color,screen,screen_size[0]/4+screen_size[0]/5,3*screen_size[1]/20)
        draw_text(lt[1].name,new_font,lt[1].color,screen,screen_size[0]/4+screen_size[0]/5,6*screen_size[1]/20)
        draw_text(lt[2].name,new_font,lt[2].color,screen,screen_size[0]/4+screen_size[0]/5,9*screen_size[1]/20)
        draw_text(lt[3].name,new_font,lt[3].color,screen,screen_size[0]/4+screen_size[0]/5,12*screen_size[1]/20)
        draw_text(lt[4].name,new_font,lt[4].color,screen,screen_size[0]/4+screen_size[0]/5,15*screen_size[1]/20)
        pygame.display.flip()
    return False

def profile_display(user,screen):
    run = True
    return_bt = Buttons(screen_size[0]/24,screen_size[0]/24,item_pic,23*screen_size[0]/24,screen_size[1]-screen_size[0]/24,screen)
    while run:
        spot=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if return_bt.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    run = False
        if return_bt.is_in(spot[0],spot[1]):
            pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
    #vẽ màn hình, nút
        screen.fill((0,0,0))
        return_bt.draw()
        draw_text('username:'+user.username,font,white,screen,screen_size[0]/4,screen_size[1]/4)
        draw_text('Money:'+str(user.money),font,white,screen,screen_size[0]/4,screen_size[1]/3)
        pygame.display.flip()

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Kiểm tra thông tin đăng nhập
    if username == "admin" and password == "password":
        # Đăng nhập thành công, chuyển màn hình
        window_login.destroy()  # Đóng màn hình đăng nhập

        # Tạo màn hình mới sau khi đăng nhập thành công
        #truyền tạm biến user lấy username để tạo folder lưu ảnh
        main_menu(username)

        # Thêm các thành phần và chức năng cho màn hình mới ở đây

    else:
        # Đăng nhập không thành công, hiển thị thông báo lỗi
        label_error.config(text="Thông tin đăng nhập không đúng")

# Tạo màn hình đăng nhập
window_login = tk.Tk()

# Thêm các thành phần vào màn hình đăng nhập
label_username = tk.Label(window_login, text="Tên đăng nhập:")
label_username.pack()
entry_username = tk.Entry(window_login)
entry_username.pack()

label_password = tk.Label(window_login, text="Mật khẩu:")
label_password.pack()

entry_password = tk.Entry(window_login, show="*")
entry_password.pack()

button_login = tk.Button(window_login, text="Đăng nhập", command=login)
button_login.pack()

label_error = tk.Label(window_login, text="")
label_error.pack()
# Chạy màn hình đăng nhập
window_login.mainloop()

