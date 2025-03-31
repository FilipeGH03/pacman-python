import pygame
import math
import random
import time
import heapq


#Configs Basicas 
pygame.init()
w = 1480
h = 1080
window = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 15
font = pygame.font.Font(None, 36)
colors = {
    "random": pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "blue": pygame.color.Color(0, 0, 255),
    "red": pygame.color.Color(255, 0, 0),
    "green": pygame.color.Color(0, 255, 0),
    "yellow": pygame.color.Color(255, 255, 0),
    "black": pygame.color.Color(0, 0, 0),
    "white": pygame.color.Color(255, 255, 255),
    "purple": pygame.color.Color(128, 0, 128),
    "orange": pygame.color.Color(255, 165, 0),
    "gray": pygame.color.Color(128, 128, 128),
    "pink": pygame.color.Color(255, 192, 203),
    "brown": pygame.color.Color(139, 69, 19),
    "turquoise": pygame.color.Color(0, 206, 209),
    "beige": pygame.color.Color(245, 245, 220),
    "gold": pygame.color.Color(255, 215, 0),
    "silver": pygame.color.Color(192, 192, 192),
    "cyan": pygame.color.Color(0, 255, 255),
    "magenta": pygame.color.Color(255, 0, 255),
    "coral": pygame.color.Color(255, 127, 80),
    "indigo": pygame.color.Color(75, 0, 130),
    "violet": pygame.color.Color(238, 130, 238)
}
#funções

def reset_game():
    global pac, phantom, foods, pac, spawn, movement_direction
    pac = PacMan(20, 23)
    spawn = Wall(11, 19, 0, 0)
    movement_direction = 100
    foods = [Food(i, j) for i, row in enumerate(table) for j, position in enumerate(row) if all((position not in wall.pos) for wall in walls) and (i, j) not in excluded_positions]
    phantom = [Ghost(11, 19, 0)]

def gameOver():
    while True:
        window.fill(colors["black"])
        window.blit(font.render("Game Over", True, colors["white"]), (w // 2 - 100, h // 2 - 50))
        window.blit(font.render("Pressione ESC para sair.", True, colors["white"]), (w // 2 - 180, h // 2 + 50))
        window.blit(font.render("Pressione ENTER para reiniciar.", True, colors["white"]), (w // 2 - 180, h // 2 + 80))
        window.blit(font.render(f"Sua pontuação foi: {pac.points}", True, colors["white"]), (w // 2 - 180, h // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_RETURN:
                    reset_game()
                    return
                    


def check_collision(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

#classes jogo

class Wall:
    def __init__(self,y,x, a, l):
        self.pos = [table[y][x]]
        self.x = x
        self.y = y
        if l < 80: 
            self.l = 40
        else:
            for i in range(x+1,l//40+x):
                self.pos.append(table[y][i])
        if a < 80: 
            self.a = 40
        else:
            for i in range(y+1,a//40+y):
                self.pos.append(table[i][x])
    def drawWall(self,c):
        for i in self.pos:
            pygame.draw.rect(window, colors[c], (*i, 40, 40))

class PacMan:
    def __init__(self,y,x):
        self.x, self.y = table[y][x]
        self.images = [pygame.transform.scale(pygame.image.load("pacman1.png"), (40,40)), pygame.transform.scale(pygame.image.load("pacman2.png"), (40,40))]
        self.img = 0
        self.ang = 0
        self.points = 0
    def right(self):
        self.x += 40
        self.ang = 0
        for i in walls:
            if (self.x, self.y) in i.pos:
                pass
                self.x -= 40
    def left(self):
        self.x -= 40
        self.ang = 180
        for i in walls:
            if (self.x, self.y) in i.pos:
                pass
                self.x += 40 
    def down(self):
        self.y += 40
        self.ang = -90
        for i in walls:
            if (self.x, self.y) in i.pos:
                pass  
                self.y -= 40
    def up(self):
        self.y -= 40
        self.ang = 90  
        for i in walls:
            if (self.x, self.y) in i.pos:
                pass
                self.y += 40
    def eat(self):
        for i in foods:
            if i.x == self.x and i.y == self.y:
                self.points += 1
                i.x = 10000
    def drawPacMan(self):
        self.img = self.img % 2
        window.blit(pygame.transform.rotate(self.images[self.img],self.ang), (self.x, self.y))
        self.img += 1  
    
class Food:
    def __init__(self,y,x):     
        self.pos = table[y][x]
        self.x = table[y][x][0] 
        self.y = table[y][x][1]
    def drawFood(self,c):
        pygame.draw.circle(window, colors[c], (self.x + 20,self.y + 20), 8)

class Ghost:
    def __init__(self,y,x,id):
        self.x, self.y = table[y][x]
        self.image = [pygame.transform.scale(pygame.image.load("./ghost1.png"), (40, 40)),pygame.transform.scale(pygame.image.load("./ghost2.png"), (40, 40)),pygame.transform.scale(pygame.image.load("./ghost3.png"), (40, 40))]    
        self.id = id
    # def ghostMove(self, pacMan):
    #     self.p = 0
    #     if (self.x,self.y) in [table[11][19],table[11][20],table[11][21]]:
    #         self.x += 40
    #     else:
    #         if self.x == pacMan.x:
    #             self.p = 1
    #             if pacMan.y > self.y:
    #                 self.y += 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.y -= 40
    #                         self.p = 0
    #             else:
    #                 self.y -= 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.y += 40
    #                         self.p = 0
    #         if self.y == pacMan.y:
    #             self.p = 1
    #             if pacMan.x > self.x:
    #                 self.x += 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.x -= 40
    #                         self.p = 0
    #             else:
    #                 self.x -= 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.x += 40
    #                         self.p = 0
    #         else:
    #             if random.randint(1,4) == 1 and self.p == 0:
    #                 self.x += 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.x -= 40
    #                         self.ghostMove(pacMan)
    #             elif random.randint(1,4) == 2 and self.p == 0:
    #                 self.x -= 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.x += 40
    #                         self.ghostMove(pacMan)
    #             elif random.randint(1,4) == 3 and self.p == 0:
    #                 self.y -= 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.y += 40
    #                         self.ghostMove(pacMan)
    #             elif random.randint(1,4) == 4 and self.p == 0:
    #                 self.y += 40
    #                 for i in walls:
    #                     if (self.x, self.y) in i.pos:
    #                         self.y -= 40
    #                         self.ghostMove(pacMan)
    def find_path(self, pacMan):
        start = (self.x, self.y)
        goal = (pacMan.x, pacMan.y)

        # Função heurística para estimar o custo restante
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Implementação do algoritmo A*
        def a_star_search(start, goal):
            frontier = [(0, start)]
            came_from = {start: None}
            cost_so_far = {start: 0}

            while frontier:
                current_cost, current = heapq.heappop(frontier)

                if current == goal:
                    path = []
                    while current is not None:
                        path.append(current)
                        current = came_from[current]
                    return path[::-1]

                for next in self.get_neighbors(current):
                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        heapq.heappush(frontier, (priority, next))
                        came_from[next] = current

            return None

        path = a_star_search(start, goal)
        if path and len(path) > 1:
            # Retorna a direção do primeiro movimento no caminho
            next_position = path[1]
            if next_position[0] > self.x:
                return "right"
            elif next_position[0] < self.x:
                return "left"
            elif next_position[1] > self.y:
                return "down"
            elif next_position[1] < self.y:
                return "up"

        return None

    def get_neighbors(self, position):
        x, y = position
        neighbors = [(x + 40, y), (x - 40, y), (x, y + 40), (x, y - 40)]
        return [neighbor for neighbor in neighbors if not self.check_collision(neighbor)]

    def check_collision(self, position):
        for wall in walls:
            if position in wall.pos:
                return True
        return False
    def drawGhost(self):
        if self.image is not None:
            window.blit(self.image[self.id], (self.x, self.y))
        
        
#Variaveis relacionadas ao jogo 

table = [[(j*40, i*40) for j in range(39)] for i in range(23)]
#def __init__(self,y,x, a, l):
walls = [Wall(0,0,880,0),Wall(0,0,0,1560),Wall(0,38,880,0),Wall(21,1,0,1520),Wall(19,3, 0,1320), Wall(2,3, 0,1320), 
         Wall(9,17,200,200), Wall(13,17,0,200),Wall(10,21,0,0),Wall(12,21,0,0), Wall(11,2,0,520), Wall(11,24,0,520), 
         Wall(4,3,560,0), Wall(4,35,560,0), 
         Wall(13,33,200,0),Wall(13,31,200,0),Wall(13,29,200,0),Wall(13,27,200,0), Wall(13,25,200,0),
         Wall(13,5,200,0),Wall(13,7,200,0),Wall(13,9,200,0),Wall(13,11,200,0), Wall(13,13,200,0),
         Wall(4,5,0,440),Wall(8,5,0,440),Wall(6,7,0,280), Wall(4,23,0,440),Wall(8,23,0,440),Wall(6,25,0,280),
         Wall(13,15,120,0),Wall(13,23,120,0),Wall(15,16,0,280)
         ]
phantom = [Ghost(11,19,0)] #,Ghost(11,19,1),Ghost(11,19,2)]
foods = []
excluded_positions = {(10, 18), (10, 19), (10, 20), (11, 18), (11, 19), (11, 20), (11, 21), (12, 18), (12, 19), (12, 20)}
for i, row in enumerate(table):
    for j, position in enumerate(row):
        # Verifica se não há uma parede na posição
        if all((position not in wall.pos) for wall in walls) and (i, j) not in excluded_positions:
            foods.append(Food(i, j))
pac = PacMan(20,23)
spawn = Wall(11,19,0,0)
movement_direction = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key in (pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s):
                movement_direction = event.key  
    # for i in phantom:
    #     if (i.x,i.y) == (pac.x,pac.y):
    #         pygame.quit()
    if movement_direction == pygame.K_d: #100
        pac.right()
    elif movement_direction == pygame.K_a: #97
        pac.left()
    elif movement_direction == pygame.K_w: #119
        pac.up()
    elif movement_direction == pygame.K_s: #115
        pac.down()
    window.fill(colors["black"])
    for i in foods:
        i.drawFood("orange")
    for i in walls:
        i.drawWall("gray")
    spawn.drawWall("blue")
    if pac.points == 50:
        phantom.append(Ghost(11,19,1))
    if pac.points == 100:
        phantom.append(Ghost(11,19,2))
    for i in phantom:
        direction = i.find_path(pac)
        if direction:
            if direction == "right":
                i.x += 40
            elif direction == "left":
                i.x -= 40
            elif direction == "down":
                i.y += 40
            elif direction == "up":
                i.y -= 40
        i.drawGhost()
            
    pac.drawPacMan()
    pac.eat()
    window.blit(font.render(f"Pontuação: {pac.points}", True, colors["white"]), (table[21][1]))
    time.sleep(0.15)

    for i in phantom:
        if check_collision((pac.x, pac.y), (i.x, i.y)):
            gameOver()
    pygame.display.flip()
    clock.tick(FPS) 
    

# largura 1520 altura 840