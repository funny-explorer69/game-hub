import numpy as np
import pygame
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from game_files.screen import display
from collections import deque

class game2(display):
    def __init__(self):
        super().__init__()
        self.board = np.zeros((20, 30), dtype = bool)
        self.board.flat[np.random.choice(self.board.size,100,replace= False)] = True
        self.is_running = True
        self.is_revealed = np.zeros((20,30), dtype = bool)
        self.value_board = np.zeros((20,30))
        self.calculate()
        self.pth = Path(__file__).parent.parent.parent
        self.pictures = []
        for i in range(9):
            self.pictures.append(pygame.image.load(f"{self.pth}/pictures/minesweeper/{i}.png"))

        
    def game_run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x_idx,y_idx = 0,0 # has to be changed later
                    if 0 < x_idx < 20 and 0 < y_idx < 30: 
                        if self.reveal(x_idx,y_idx):
                            self.reveal_bombs()
                            # lost
                        elif np.sum(self.is_revealed) == 500: #all except mines are revealed
                            # win
                            pass
                            
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
                            if i+ni < 0 or j+nj < 0 or i+ni > 19 or j+nj > 29: # xhwcking the entire board
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
                        self.value_board[i,j] += self.board[i+ni,j+nj]

    def reveal_bombs(self):
        for i in range(20):
            for j in range(30):
                if self.board[i,j] == 1:
                    self.screen.blit(bomb_image,(i*2+1,j*2+1))# these has to be changed later on
                elif self.is_revealed[i,j]:
                    self.screen.blit(self.pictures[self.value_board[i,j]],(i*2+1,j*2+1))# these too should be changed

