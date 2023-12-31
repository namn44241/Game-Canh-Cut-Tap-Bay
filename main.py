import pygame
import spritesheet
#tăng hiệu suất game nhờ việc cắt hình to thành nhiều hình bé thay vì dùng nhiều hình bé
pygame.init()
from sys import exit
clock = pygame.time.Clock() #Đặt FPS

#Tieu de va icon
pygame.display.set_caption('Cánh cụt tập bayyyyy')
icon = pygame.image.load(r'assets\icon\icongame.png')
pygame.display.set_icon(icon)

#Cua so game
display_screen = pygame.display.set_mode((1400, 700))

#Load hinh anh
bg = pygame.image.load(r'assets\background\background1.png')
bg1 = pygame.image.load(r'assets\background\background2.png')
bg2 = pygame.image.load(r'assets\background\background3.png')
obstacle = pygame.image.load(r'assets\obstacle\obstacle.png')
char = pygame.image.load(r'assets\player\runpy_1.png')
win_bg = pygame.image.load(r'assets\background\wingame.jpg')

#Load am thanh
over_sound = pygame.mixer.Sound(r'assets\audio\die.mp3')
bg_sound = pygame.mixer.Sound(r'assets\audio\All I Want for Christmas is a Super Nintendo.mp3')
jump_sound = pygame.mixer.Sound(r'assets\audio\click.mp3')
win_sound = pygame.mixer.Sound(r'assets\audio\endgame-credit.mp3')

#Load font chữ
custom_font = pygame.font.Font(r"assets\font\TP Born Pink.ttf", 50)

sprite_sheet = spritesheet.SpriteSheet(char)

#Khoi tao
score, high_score = 0, 0
bg_x, bg_y = 0, 0
obs_x, obs_y = 1400, 570
char_x, char_y = 300, 570 
x_move = 15
y_move = 10
jump = False
bg_sound.set_volume(0.0)
over_sound.set_volume(0.0)
jump_sound.set_volume(0.0)

#Khoi tao chuyen dong cua nhan vat
animation_list = []    #6 chuyển động
#hỗ trợ lưu frame hoạt hình sắp tới
#cắt chuỗi ảnh nv lớn thành 6 ảnh nhỏ, mỗi frame chạy 1 ảnh ấy (spritesheet)
last_update = pygame.time.get_ticks()
animation_cooldown = 150
#xem mỗi lần chạy xong 6 ảnh nhỏ trên hết bao nhiêu thời gian
frame = 0

for x in range(6):
    animation_list.append(sprite_sheet.get_image(x, 84, 84, 1.0, (0,0,0)))
    
#Ktra xem co con song hay khong
isAlive = True
#Kiem tra xem da win hay chua
isWin = False

#Ham xu ly va cham
def ktravacham():
    if char_box.colliderect(obs_box):
        bg_sound.stop()
        over_sound.play()
        return False
    return True

#Ham tinh diem
def display_Score():
    if isWin == False:
        if isAlive :
            #2 nhiệm vụ: định dang (render) + in ra màn hình (blit)
            score_text = custom_font.render(f'Score: {int(score)}', False, (1, 1, 1))
            display_screen.blit(score_text, (0, 0))
            highscore_text = custom_font.render(f'High Score: {int(high_score)}', True, (1, 1, 1))
            display_screen.blit(highscore_text, (1075, 0))
        else:
            score_text = custom_font.render(f'Score: {int(score)}', True, (1, 1, 1))
            display_screen.blit(score_text, (600, 150))
            highscore_text = custom_font.render(f'High Score: {int(high_score)}', True, (1, 1, 1))
            display_screen.blit(highscore_text, (570, 100))
            gameover_text = custom_font.render(f'GAME OVER', True, 'Green')
            display_screen.blit(gameover_text, (600, 300))


#Ham xuat hien khi win game
def win():
    display_screen.blit(win_bg, (0, 0))
    win_Text = custom_font.render(f'YOU LOSE', True, 'White')
    display_screen.blit(win_Text, (600, 300))
    bg_sound.stop()
    win_sound.play()


#Vong lap xu li game
gameRunning = True
while gameRunning:
    clock.tick(60)
    #fps của game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and isAlive:
                #k space là phím space
                    jump = True
                    jump_sound.play()
            if event.key == pygame.K_SPACE and isAlive == False:
                start_time = pygame.time.get_ticks()
                isAlive = True
    if isWin == False:
        if isAlive:
            bg_sound.play(loops= -1)
            #loops = -1 tức âm thanh lặp lại vô hạn
            #Background
            bg_box = display_screen.blit(bg, (bg_x, bg_y))
            #Background chuyen dong
            bg2_box = display_screen.blit(bg, (bg_x + 1400, bg_y))
            bg_x -= 5
            if bg_x == -1400:
                bg_x = 0
            #Chuong ngai vat
            obs_box = display_screen.blit(obstacle, (obs_x, obs_y))
            #Chuong ngai vat chuyen dong
            obs_x -= x_move
            if obs_x <= 0:
                obs_x = 1400
            #Nhat vat game
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                #khó hiểu kk
                frame += 1
                last_update = current_time
            if frame >= len(animation_list):
                frame = 0
            char_box = display_screen.blit(animation_list[frame], (char_x, char_y))
            #Nhan vat nhay
            if char_y >= 380 and jump:
                char_y -= y_move
            else:
                jump = False
            if char_y < 570 and jump == False:
                char_y += y_move
            score += 0.02
            if high_score < score:
                high_score = score
            isAlive = ktravacham()
            display_Score()
            if score >= 5 and score < 15:
                x_move = 20
            if score >= 15 and score < 30:
                x_move = 25
                bg = bg1
            if score >= 30 and score < 32:
                x_move = 30
                bg = bg2
            if score >= 32:
                isWin = True
                win()
        else:
            #Restart game
            obs_x, obs_y = 1400, 570
            char_x, char_y = 300, 570
            bg_box = display_screen.blit(bg, (bg_x, bg_y))
            obs_box = display_screen.blit(obstacle, (obs_x, obs_y))
            char_box = display_screen.blit(animation_list[frame], (char_x, char_y))
            score = 0
            x_move = 15
            display_Score()
            bg = pygame.image.load(r'assets\background\background1.png')
            # cần phải định dạng lại game sau khi restart - nhìn thừa nhưng không thể bỏ
            
    pygame.display.update()



