import pygame
import sys
import numpy as np
import math
import time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from game_files.screen import display

class game1(display):
    def __init__(self):
        super().__init__()
        self.bullets = np.empty((50,4),dtype=np.float32)
        self.bullets.fill(-1)
        self.obstacles = np.empty((10,5),dtype=np.float32)
        self.obstacles.fill(-1)
        self.is_running = True
        self.player_pos = (640.0,600.0)
        self.old_player_pos = self.player_pos
        self.new_x = 640.0
        self.new_y = 600.0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.acc_x = 1
        self.acc_y = 2
        self.e = 0.5
        self.no_of_bullets = 0
        self.no_of_obstacles = 0
        self.obstacle_spawn_rate = 1/120
        

    def shoot(self,mouse_pos):
        if self.no_of_bullets >= len(self.bullets):
            return
        mx,my = mouse_pos
        dx = mx - self.player_pos[0]
        dy = my - self.player_pos[1]
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            return
        bullet_speed = 20
        vx = dx * bullet_speed / length
        vy = dy * bullet_speed / length
        idx = self.no_of_bullets
        self.bullets[idx] = np.array([self.player_pos[0],self.player_pos[1],vx,vy],dtype=np.float32)
        self.no_of_bullets += 1
        self.speed_x -= vx/5
        self.speed_y -= vy/8

    def got_hit(self,i):
        obstacle = self.obstacles[i]
        if np.all(obstacle == -1):
            return False
        x1,y1 = self.old_player_pos
        x2,y2 = self.new_x,self.new_y
        x3,y3 = obstacle[0],obstacle[1]

        dx = x2 - x1
        dy = y2 - y1
        seg_len_sq = dx*dx + dy*dy

        if seg_len_sq == 0:
            dist = ((x3-x1)**2 + (y3-y1)**2)**0.5
            return dist < 13

        t = ((x3-x1)*dx + (y3-y1)*dy)/seg_len_sq
        t = max(0,min(1,t))

        closest_x = x1 + t*dx
        closest_y = y1 + t*dy

        dist = (x3-closest_x)**2 + (y3-closest_y)**2

        if dist < 169:
            self.player_pos = (closest_x,closest_y)
            return True
        return False

    def bullet_hit(self,i,j):
        obstacle = self.obstacles[i]
        bullet = self.bullets[j]

        if np.all(obstacle == -1) or np.all(bullet == -1):
            return False

        ox1,oy1 = obstacle[0],obstacle       [1]

        ox2 = ox1 + obstacle[2]
        oy2 = oy1 + obstacle[3]
        bx1,by1 = bullet[0],bullet[1]

        bx2 = bx1 + bullet[2]
        by2 = by1 + bullet[3]
        
        rx1 = bx1 - ox1
        ry1 = by1 - oy1

        rx2 = bx2 - ox2
        ry2 = by2 - oy2

        dx = rx2 - rx1
        dy = ry2 - ry1

        seg_len_sq = dx*dx + dy*dy
        if seg_len_sq == 0:
            dist = (rx1*rx1 + ry1*ry1)**0.5
            if dist <= 12:
                self.obstacles[i] = -1
                self.bullets[j] = -1
                return True
            return False
        t = -(rx1*dx + ry1*dy)/seg_len_sq
        t = max(0,min(1,t))

        closest_x = rx1 + t*dx
        closest_y = ry1 + t*dy
        dist = closest_x*closest_x + closest_y*closest_y
        if dist <= 144:
            self.obstacles[i] = -1
            self.bullets[j] = -1
            return True
        return False
    def game_run(self):
        clock = pygame.time.Clock()
        while self.is_running:
            t = time.perf_counter_ns()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        self.shoot(mouse_pos)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.speed_x -= 3
                self.speed_x = max(self.speed_x,-20)

            if keys[pygame.K_d]:
                self.speed_x += 3
                self.speed_x = min(self.speed_x,20)

            if keys[pygame.K_SPACE]:

                if self.player_pos[1] >= 600:
                    self.speed_y = -30

            if self.speed_x > 0:
                self.speed_x -= self.acc_x
                if self.speed_x < 0:
                    self.speed_x = 0
            elif self.speed_x < 0:
                self.speed_x += self.acc_x
                if self.speed_x > 0:
                    self.speed_x = 0
            self.speed_y += self.acc_y
            self.old_player_pos = self.player_pos

            self.new_x = self.player_pos[0] + self.speed_x
            self.new_y = self.player_pos[1] + self.speed_y

            if self.new_y >= 600:
                self.new_y = 600
                self.speed_y *= -self.e

            if self.new_x >= 1270:
                self.new_x = 1270
                self.speed_x *= -self.e

            elif self.new_x <= 10:
                self.new_x = 10
                self.speed_x *= -self.e

            self.player_pos = (self.new_x,self.new_y)

            for obstacle in self.obstacles:
                if np.all(obstacle == -1):
                    continue
                ox,oy = obstacle[0],obstacle[1]
                future_x = self.player_pos[0] + self.speed_x*3
                future_y = self.player_pos[1] + self.speed_y*3

                dx = future_x - ox
                dy = future_y - oy

                length = (dx**2 + dy**2)**0.5
                if length != 0:
                    speed = obstacle[4]
                    obstacle[2] = dx*speed/length
                    obstacle[3] = dy*speed/length

                obstacle[0] += obstacle[2]
                obstacle[1] += obstacle[3]

            if self.no_of_obstacles < len(self.obstacles):
                if np.random.rand() <= self.obstacle_spawn_rate:
                    side = np.random.randint(0,3)
                    if side == 0:
                        x = 0
                        y = np.random.randint(0,600)
                    elif side == 1:
                        x = 1280
                        y = np.random.randint(0,600)
                    elif side == 2:
                        x = np.random.randint(0,1280)
                        y = 0

                    speed = 1 + 3 * (np.random.rand() ** 2)
                    self.obstacles[self.no_of_obstacles] = np.array([x,y,0,0,speed],dtype=np.float32)
                    self.no_of_obstacles += 1

            for idx in range(len(self.bullets)):
                bullet = self.bullets[idx]
                if np.all(bullet == -1):
                    continue

                bullet[0] += bullet[2]
                bullet[1] += bullet[3]

                if not (10 <= bullet[0] <= 1270 and 10 <= bullet[1] <= 610):
                    self.bullets[idx] = -1
                    continue

            for i in range(len(self.obstacles)):
                for j in range(len(self.bullets)):
                    self.bullet_hit(i,j)

            for i in range(len(self.obstacles)):
                if self.got_hit(i):
                    rect = pygame.Rect(0,0,1280,720)
                    overlay = pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
                    overlay.fill((0,0,0,120))
                    self.screen.blit(overlay,rect)
                    font = pygame.font.Font(None,150)
                    text = font.render("Game Over",True,(255,255,255))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text,text_rect)
                    pygame.display.update()
                    pygame.time.delay(3000)
                    while True:
                        mouse_pos = pygame.mouse.get_pos()
                        rect1 = pygame.Rect(390,130,500,220)
                        rect2 = pygame.Rect(390,370,500,220)
                        color1 = (40,40,40) if rect1.collidepoint(mouse_pos) else (0,0,0)
                        color2 = (40,40,40) if rect2.collidepoint(mouse_pos) else (0,0,0)
                        self.screen.fill((255,255,255))

                        pygame.draw.rect(self.screen,color1,rect1,border_radius=20)
                        pygame.draw.rect(self.screen,color2,rect2,border_radius=20)

                        text1 = font.render("Back",True,(255,255,255))
                        text2 = font.render("Try again",True,(255,255,255))

                        text_rect1 = text1.get_rect(center=rect1.center)
                        text_rect2 = text2.get_rect(center=rect2.center)

                        self.screen.blit(text1,text_rect1)
                        self.screen.blit(text2,text_rect2)

                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if rect1.collidepoint(mouse_pos):
                                    return False
                                if rect2.collidepoint(mouse_pos):
                                    return True
                                clock.tick(60)
                                        
                    
            mask = self.obstacles[:,0] != -1
            count = np.sum(mask)
            self.obstacles[:count] = self.obstacles[mask]
            self.obstacles[count:] = -1
            self.no_of_obstacles = count

            mask = self.bullets[:,0] != -1
            count = np.sum(mask)

            self.bullets[:count] = self.bullets[mask]
            self.bullets[count:] = -1

            self.no_of_bullets = count

            self.screen.fill((255,255,255))
            pygame.draw.line(self.screen,(0,255,0),(0,610),(1280,610),2)
            pygame.draw.circle(self.screen,(255,0,0),(int(self.player_pos[0]),int(self.player_pos[1])),10)
            mouse_pos = pygame.mouse.get_pos()

            dx = mouse_pos[0] - self.player_pos[0]
            dy = mouse_pos[1] - self.player_pos[1]
            length = (dx**2 + dy**2)**0.5

            if length != 0:
                dx *= 20/length
                dy *= 20/length
                pygame.draw.line(self.screen,(0,0,0),(self.new_x + dx/2 , self.new_y + dy/2),(self.new_x + dx , self.new_y + dy) , 3)

            for bullet in self.bullets:
                if np.all(bullet == -1):
                    continue
                pygame.draw.circle(self.screen,(0,0,0),(int(bullet[0]),int(bullet[1])),4)

            for obstacle in self.obstacles:
                if np.all(obstacle == -1):
                    continue
                pygame.draw.circle(self.screen,(255,0,0),(int(obstacle[0]),int(obstacle[1])),5)

            pygame.display.update()       
            clock.tick(60)
            

