import pygame, sys, time, random,os
from pygame.locals import *
import tkinter as tk
pygame.init()

FPS = 120
fpsClock = pygame.time.Clock()

#Cửa sổ game
screen_size=(1280,720)
screen=pygame.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_caption("Car Bet")
icon=pygame.image.load(r'MainGame\Image\car2.png')
pygame.display.set_icon(icon)
#Thêm background
bg=pygame.transform.scale(pygame.image.load(r'MainGame\Image\background.png'),screen_size)
end_bg=1100
start_bg=200
#Load ảnh xe
car_pic2=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car2.png'),(150,150))
car_pic1=pygame.transform.scale(pygame.image.load(r'MainGame\Image\car2.png'),(150,150))
item_pic=pygame.image.load(r'MainGame\Image\item.png')
#Màu
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
#Tham số
#tiền tạm thời
current_money = 20000
#thay đổi kích thưóc màn hình
def screen_resize(new_screen_size):
    screen = pygame.display.set_mode(new_screen_size,pygame.RESIZABLE)
#Set font
font = pygame.font.SysFont("Arial", 50, bold=True, italic=False)
new_font = pygame.font.SysFont("Arial", 30, bold=True, italic=False)
#Hàm
#Vẽ chữ
def draw_text(text, font, color, surface, x, y):
    text_rect.center = (x,y)
    surface.blit(text_obj, text_rect)        
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
def run_game(player_pic,com1_pic,com2_pic,com3_pic,com4_pic,buff_speed,better_start,player_name,user):
    #Khởi tạo xe 
    player=Car(player_pic,2,buff_speed,better_start)
    com1=Car(com1_pic,1)
    com2=Car(com2_pic,3)
    com3=Car(com3_pic,4)
    com4=Car(com4_pic,5)
    # tên màu tên xe
    player.name = player_name
    com1.name = 'com'
    com2.name ='com'
    com3.name ='com'
    com4.name ='com'
    player.color = ((255,255,0))
    com1.color=((0,0,0))
    com2.color=((0,0,0))
    com3.color=((0,0,0))
    com4.color=((0,0,0))
    #Khởi tạo biến item
    item1=Item()
    item2=Item()
def run_game(player_pic,com1_pic,com2_pic,com3_pic,com4_pic,buff_speed,better_st
    bg_x=0
    rank=1
    ranked=False
    check_rank = True
    #Vòng lặp game
    start=False
    while running:
	@@ -248,8 +288,13 @@ def run_game(player_pic,com1_pic,com2_pic,com3_pic,com4_pic,buff_speed,better_st
            draw_text(str(com2.rank),font,white,screen,end_bg+100,com2.y)
            draw_text(str(com3.rank),font,white,screen,end_bg+100,com3.y)
            draw_text(str(com4.rank),font,white,screen,end_bg+100,com4.y)
            # bảng xếp hạng
            check_rank = ranked_rs(r'Image\item.png',screen_size[0]/2,4*screen_size[1]/5,player,com1,com2,com3,com4,user)

        pygame.display.update()
        #thoát ra menu
        if check_rank == False:
            break
    return player_rank

#Khởi tạo nút
def shopping():
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
                    buy_buff_speed.img=item_pic
                if buy_better_start.is_in(spot[0],spot[1]):
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    better_start=True
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
#Sảnh chờ




def main_menu(username):
    #USER
    current_user = User(username)
    current_user.create_player_history()
    #Khởi tạo nút
    profile_bt = Buttons(200,100,item_pic,20,20)
    start_bt=Buttons(200,100,item_pic,540,570)
    shop_bt=Buttons(100,100,item_pic,50,570)
    buff=(False,False)
    temp_bt = Buttons(100,100,item_pic,980,570)
    player_name=''
    #Vòng lặp
    running_menu=True
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
                    run_game(car_pic2,car_pic2,car_pic2,car_pic2,car_pic2,buff[0],buff[1],player_name,current_user)
                    running_menu=True
                if shop_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    #đổi lại hình dạng chuột ban đầu sau khi click
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    buff=shopping()
                    running_menu=True
                if profile_bt.is_in(spot[0],spot[1]):
                    running_menu=False
                    pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)
                    profile_display(current_user)
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
def ranked_rs(image,width,height,player,com1,com2,com3,com4,user):
    rank_img = pygame.transform.scale(pygame.image.load(image),(width,height))
    rank_rect = rank_img.get_rect(topleft=(screen_size[0]/4,screen_size[1]/10))
    running_rank = True
    home_bt = Buttons(screen_size[0]/16,screen_size[1]/8,item_pic,screen_size[0]/4,9*screen_size[1]/10)
    save_bt = Buttons(screen_size[0]/16,screen_size[1]/8,item_pic,3*screen_size[0]/4,9*screen_size[1]/10)
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
''' Hàm hiển thị số tiền hiện lại (nút góc trái phía trên)'''
def profile_display(user):
    run = True
    return_bt = Buttons(screen_size[0]/24,screen_size[0]/24,item_pic,23*screen_size[0]/24,screen_size[1]-screen_size[0]/24)
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
