import numpy as np
import pygame
import sys
from game import menu
from collections import deque

class game2(menu):
    def __init__(self):
        self.board = np.zeros((20,30))
        self.board.flat[np.random.choice(self.board.size,100,replace= False)] = 1
        self.is_running = True
        self.is_revealed = np.empty((20,30))
        self.is_revealed.fill(False)
        self.value_board = np.zeroes((20,30))
        self.calculate()
        
    def game_run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x_idx,y_idx = 0,0 # has to be changed later
                    if 0 < x_idx < 20 and 0 < y_idx < 30: 
                        if self.reveal(x_idx,y_idx):
                            self.reveal_bombs()
                            # lost
                        elif np.sum(self.is_revealed) == 500:
                            # win
                            

    def reveal(self,x_idx,y_idx):
        if self.is_revealed(x_idx,y_idx) == False: #if it hasnt been revealed yet then bfs starts
            if self.board[x_idx,y_idx] == 1:
                return True
            else:
                q = deque()
                q.append((x_idx,y_idx))
                while q:
                    temp = q.pop()
                    i,j = temp[0],temp[1]
                    self.is_revealed[i,j] = True
                    if self.value_board[i,j]:
                        continue
                    for ni in [-1,0,1]:
                        for nj in [-1,0,1]:
                            if ni == 0 and nj == 0:
                                continue
                            if i+ni < 0 or j+nj < 0 or i+ni > 19 or j+nj > 29:
                                continue
                            if self.is_revealed[i+ni,j+nj] == True:
                                continue
                            q.append((i+ni,j+nj))
                return False
    def calculate(self):
        for i in range(20):
            for j in range(30):
                if self.board[i,j] == 1:
                    continue
                for ni in [-1,0,1]:
                    for nj in [-1,0,1]:
                        if i+ni < 0 or j+nj < 0 or i+ni > 19 or j+nj > 29 :
                            continue
                        if self.board[i+ni,j+nj]:
                            self.value_board[i,j] += 1
    def reveal_bombs(self):
        pass
    
