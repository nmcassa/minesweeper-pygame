import pygame, sys, random
from pygame.locals import *
from grid import *
from grid import Grid
pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 16  # Change this to increase size
game_height = 16  # Change this to increase size
numMine = 40  # Number of mines
grid_size = 32  # Size of grid (WARNING: make sure to change the images dimension as well)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window
spr_grid = pygame.image.load("data/sprites/Grid.png")
spr_grid1 = pygame.image.load("data/sprites/grid1.png")
spr_grid2 = pygame.image.load("data/sprites/grid2.png")
spr_grid3 = pygame.image.load("data/sprites/grid3.png")

font_small = pygame.font.Font('data/fonts/font.otf', 32)

pygame.display.set_caption('Scuffed Minesweeper')

# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines
gameState = "Playing"  # Game state

def drawText(txt, s, yOff=0):
    screen_text = font_small.render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)

def check_collision(ax, ay, bx, by):
    p = 32 #sprite size
    return (ax + p > bx) and (ax < bx + p) and (ay + p > by) and (ay < by + p)

def main():
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    rx = display_width/2 - border
    ry = border

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue(grid, game_width, game_height)

    gameState = "Playing"
    
    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
                pygame.quit()
                sys.exit()
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.MOUSEBUTTONUP:
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
                    if check_collision(mx, my, rx, ry):
                        gameState = "Exit"
                        main()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        main()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    mx = pygame.mouse.get_pos()[0]
                    my = pygame.mouse.get_pos()[1]
                    if check_collision(mx, my, rx, ry):
                        gameState = "Exit"
                        main()
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # Toggle flag off
                                    if j.flag:
                                        continue
                                    if j.val != 0 and j.clicked:
                                        #cording
                                        j.cord(grid, mines, game_width, game_height)
                                    # If player left clicked of the grid
                                    j.revealGrid(grid, mines, game_width, game_height)
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            for i in grid:
                for j in i:
                    if not j.flag and j.val == -1:
                        j.win = True

        # Draw time
        s = str(t // 15)
        screen_text = font_small.render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border + 25, border))
        # Draw mine left
        screen_text = font_small.render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 30, border))
        # Restart key
        gameDisplay.blit(spr_grid, (rx, ry))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps

main()
pygame.quit()
quit()

if __name__ == "__main__":
    main()
