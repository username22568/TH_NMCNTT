import pygame, sys, time, random
from pygame.locals import *
pygame.init()

FPS = 120
fpsClock = pygame.time.Clock()

#Cửa sổ game
screen_size=(1280,720)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Car Bet")
icon=pygame.image.load(r'MainGame\Image\car2.png')
pygame.display.set_icon(icon)
#Thêm background
bg=pygame.transform.scale(pygame.image.load(r'MainGame\Image\background.png'),screen_size)
end_bg=1100
start_bg=200
#Load ảnh xe
car_pic2=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car2.png'),(150,150))
car_pic1=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car1.png'),(150,150))
item_pic=pygame.image.load(r'MainGame\Image\item.png')
#Màu
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
#Tham số

#Set font
font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)

#Hàm
#Vẽ chữ
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x,y)
    surface.blit(text_obj, text_rect)        
#Class
class Car():
    def __init__(self,image,lane,buff_speed=False,better_start=False):
        self.image=image
        self.y=100+(lane-1)*140
        self.buff_speed=buff_speed
        self.better_start=better_start
    def draw(self,x,rank):
        self.x=x
        self.rect=self.image.get_rect(center=(self.x,self.y))
        screen.blit(self.image,self.rect)
        self.rank=rank
    def is_in(self,x,y):
        if self.x==x and self.y==y:
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
    def draw(self,x,y):
        self.rect=self.image.get_rect(center=(x,y))
        screen.blit(self.image,self.rect)
    def affect(self,x):
        self.type=random.randint(0,5)
        if self.type==0 or self.type==2:
            x-=100
        elif self.type==1 or self.type==3:
            x+=100
        else:
            x=end_bg
        return x
class Buttons():
    def __init__(self,height,width,image,x,y):
        self.height=height
        self.width=width
        self.img=pygame.transform.scale(image,(height,width))
        self.x=x
        self.y=y
        self.rect=self.img.get_rect()
    def draw(self):
        self.rect.topleft=(self.x,self.y)
        screen.blit(self.img,self.rect)
    def is_in(self,x,y):
        if x>self.x and x<self.x+self.height and y>self.y and y<self.y+self.width:
            return True
#Vào đua
def run_game(player_pic,com1_pic,com2_pic,com3_pic,com4_pic,buff_speed,better_start):
    #Khởi tạo xe 
    player=Car(player_pic,2,buff_speed,better_start)
    com1=Car(com1_pic,1)
    com2=Car(com2_pic,3)
    com3=Car(com3_pic,4)
    com4=Car(com4_pic,5)
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
        max_speed=2
    else:
        max_speed=1
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
    rank=1
    ranked=False
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
        #Vẽ xe
        player.draw(player_x,player_rank)
        com1.draw(com1_x,com1_rank)
        com2.draw(com2_x,com2_rank)
        com3.draw(com3_x,com3_rank)
        com4.draw(com4_x,com4_rank)
        if start:
        #Cập nhật toạ độ cho xe
            if not(player.finish()):
                player_x+=random.randint(0,max_speed)
            if not(com1.finish()):
                com1_x+=random.randint(0,1)
            if not(com2.finish()):
                com2_x+=random.randint(0,1)
            if not(com3.finish()):
                com3_x+=random.randint(0,1)
            if not(com4.finish()):
                com4_x+=random.randint(0,1)
            #Đưa item vào
            if not(enough_item): #Nếu chưa đủ 2 item đang xuất hiện
                #Nếu item 1 chưa xuất hiện
                if not(item1.exist):
                    lane_item1=random.randint(1,5)
                    item1_y=100+(lane_item1-1)*140
                    item1_x=random.randint(min([player_x+100,com4_x+100,com3_x+100,com2_x+100,com1_x+100]),min([player_x+100,com4_x+100,com3_x+100,com2_x+100,com1_x+100])+100)
                    if item1_x<end_bg:
                        item1.exist=True
                        num_item+=1
                #Vẽ item 1
                if item1.exist:
                    item1.draw(item1_x,item1_y)
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
                    item2_y=100+(lane_item2-1)*140
                    item2_x=random.randint(min([player_x+100,com4_x+100,com3_x+100,com2_x+100,com1_x+100]),min([player_x+100,com4_x+100,com3_x+100,com2_x+100,com1_x+100])+100)
                    if item2_x<end_bg and item2_y!=item1_y:
                        item2.exist=True
                        num_item+=1
                if item2.exist:
                    item2.draw(item2_x,item2_y)
                    if player.is_in(item2_x,item2_y):
                        player_x=item2.affect(player_x)
                        num_item-=1
                        item2.exist=False
                    if com1.is_in(item2_x,item2_y):
                        com1_x=item2.affect(com1_x)
                        num_item-=1
                        item2.exist=False
                    if com2.is_in(item2_x,item2_y):
                        com2_x=item2.affect(com2_x)
                        num_item-=1
                        item2.exist=False
                    if com3.is_in(item2_x,item2_y):
                        com3_x=item2.affect(com3_x)
                        num_item-=1
                        item2.exist=False
                    if com4.is_in(item2_x,item2_y):
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
            if (player.finish() and com1.finish() and com2.finish() and com3.finish() and com4.finish()):
                start=False
                ranked=True
    #In kết quả
        if ranked:
            draw_text(str(player.rank),font,white,screen,end_bg+100,player.y)
            draw_text(str(com1.rank),font,white,screen,end_bg+100,com1.y)
            draw_text(str(com2.rank),font,white,screen,end_bg+100,com2.y)
            draw_text(str(com3.rank),font,white,screen,end_bg+100,com3.y)
            draw_text(str(com4.rank),font,white,screen,end_bg+100,com4.y)

        pygame.display.update()
    return player_rank
def shopping():
    #Khởi tạo nút
    buy_buff_speed=Buttons(200,100,car_pic1,340,360)
    buy_better_start=Buttons(200,100,car_pic1,740,360)
    quit_bt=Buttons(200,100,item_pic,540,570)
    #Tham số
    buff_speed=False
    better_start=False
    #Vòng lặp
    running_shop=True
    while running_shop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                spot=event.pos
                if buy_buff_speed.is_in(spot[0],spot[1]):
                    buff_speed=True
                    buy_buff_speed.img=item_pic
                if buy_better_start.is_in(spot[0],spot[1]):
                    better_start=True
                    buy_better_start.img=item_pic
                if quit_bt.is_in(spot[0],spot[1]):
                    running_shop=False
        screen.fill(black)
        buy_better_start.draw()
        buy_buff_speed.draw()
        quit_bt.draw()
        pygame.display.update()
    return (buff_speed,better_start)
#Sảnh chờ
def main_menu():
    #Khởi tạo nút
    start_bt=Buttons(200,100,item_pic,540,570)
    shop_bt=Buttons(100,100,item_pic,50,570)
    buff=(False,False)
    #Vòng lặp
    running_menu=True
    while running_menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                spot=event.pos
                #Xử lý thao tác trên các nút
                if start_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    run_game(car_pic2,car_pic2,car_pic2,car_pic2,car_pic2,buff[0],buff[1])
                    running_menu=True
                if shop_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    buff=shopping()
                    running_menu=True
        screen.fill(black)
        #Vẽ nút
        shop_bt.draw()
        start_bt.draw()
        pygame.display.update()
main_menu()