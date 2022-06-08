import pygame

game_width = 16
game_height = 16
border = 16
top_border = 100
grid_size = 32
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display

spr_emptyGrid = pygame.image.load("data/sprites/empty.png")
spr_flag = pygame.image.load("data/sprites/flag.png")
spr_grid = pygame.image.load("data/sprites/Grid.png")
spr_grid1 = pygame.image.load("data/sprites/grid1.png")
spr_grid2 = pygame.image.load("data/sprites/grid2.png")
spr_grid3 = pygame.image.load("data/sprites/grid3.png")
spr_grid4 = pygame.image.load("data/sprites/grid4.png")
spr_grid5 = pygame.image.load("data/sprites/grid5.png")
spr_grid6 = pygame.image.load("data/sprites/grid6.png")
spr_grid7 = pygame.image.load("data/sprites/grid7.png")
spr_grid8 = pygame.image.load("data/sprites/grid8.png")
spr_grid7 = pygame.image.load("data/sprites/grid7.png")
spr_mine = pygame.image.load("data/sprites/mine.png")
spr_mineClicked = pygame.image.load("data/sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("data/sprites/mineFalse.png")

class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.win = False

        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size,
                                grid_size)
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        elif self.win:
            gameDisplay.blit(spr_flag, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    elif self.flag:
                        gameDisplay.blit(spr_flag, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self, grid, mines, game_width, game_height):
        self.clicked = True
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid(grid, mines, game_width, game_height)
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            self.mineClicked = True
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].clicked = True

    def updateValue(self, grid, game_width, game_height):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1

    def cord(self, grid, mines, game_width, game_height):
        flags = 0
        for x in range(-1, 2):
            if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                for y in range(-1, 2):
                    if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                        if grid[self.yGrid + y][self.xGrid + x].flag:
                            flags += 1

        if flags == self.val:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked and not grid[self.yGrid + y][self.xGrid + x].flag:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid(grid, mines, game_width, game_height)
