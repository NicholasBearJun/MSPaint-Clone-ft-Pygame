import pygame
import random

#https://www.geeksforgeeks.org/how-to-create-ms-paint-clone-with-python-and-pygame/
# Direct canvas
'''
screen = pygame.display.set_mode((900, 700))

pygame.display.set_caption("Pygame MSPaint Clone")

draw_on = False
last_pos = (0,0)

radius = 5

def roundline(canvas, colour, start, end, radius = 1):
    Xaxis = end[0] - start[0]
    Yaxis = end[1] - start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist):
        x = int(start[0] + float(i)/dist*Xaxis)
        y = int(start[1]+float(i)/dist*Yaxis)
        pygame.draw.circle(canvas, colour, (x,y), radius)


try:
    while True:
        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            raise StopIteration
        
        if e.type == pygame.MOUSEBUTTONDOWN:
            colour = (random.randrange(256), random.randrange(256), random.randrange(256))
            pygame.draw.circle(screen, colour, e.pos, radius)
            draw_on = True

        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        
        if e.type == pygame.MOUSEMOTION:
            if draw_on == True:
                pygame.draw.circle(screen,colour, e.pos, radius)
                roundline(screen, colour, e.pos, last_pos, radius)

            last_pos = e.pos
        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()
'''

#Canvas Application
pygame.init()

win_x = 500
win_y = 500

# for smoother lines
pen_down = False
last_pos = (0,0)

win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Pygame MS Paint Clone")

class drawing(object):

    def __init__(self):
        self.colour = (0,0,0)
        self.width = 10
        self.height = 10
        self.radius = 10
        self.tick = 0
        self.time = 0

    # THE ERROR IS THAT the last position doesn't update after not clicking

    def draw(self, win, start, end):
        #attempt to smooth lines
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
        
            pygame.draw.circle(win, self.colour, (x, y), self.radius)
            if self.colour == (255,255,255):
                pygame.draw.circle(win,self.colour, (x, y), 20)
    

    def click(self, win, list, list2):
        global last_pos
        pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed() == (1,0,0) and pos[0] < 400:
            if pos[1] > 25:
                pen_down = True
                if pen_down == True:
                    self.draw(win, pos, tuple(map(sum, zip(last_pos, (1,1))))) #Purposefully displace
                #last_pos = pos



        elif pygame.mouse.get_pressed() == (1,0,0):

            for button in list:
                if pos[0] > button.x and pos[0] < button.x + button.width:
                    if pos[1] > button.y and pos[1] < button.y + button.height:
                        self.colour = button.colour2

            for button in list2:
                if pos[0] > button.x and pos[0] < button.x + button.width:
                    if pos[1] > button.y and pos[1] < button.y + button.height:
                        if self.tick == 0:
                            if button.action == 1:
                                win.fill((255, 255, 255))
                                #self.tick += 1
                            if button.action == 2 and self.radius > 4:
                                self.radius -= 1
                                #self.tick += 1
                                pygame.draw.rect(
                                    win, (255, 255, 255), (410, 308, 80, 35))
 
                            if button.action == 3 and self.radius < 20:
                                self.radius += 1
                                #self.tick += 1
                                pygame.draw.rect(
                                    win, (255, 255, 255), (410, 308, 80, 35))
                            
                        

class button(object):
    def __init__(self, x, y, width, height, colour, colour2, outline=0, action=0, text=''):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.outline = outline
        self.colour2 = colour2
        self.action = action
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), self.outline)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, self.colour2)
        pygame.draw.rect(win, (255, 255, 255), (410, 446, 80, 35))

        win.blit(text, (int(self.x + self.width/2 - text.get_width()/2), int(self.y + self.height/2 - text.get_height()/2)))

def drawHeader(win):
    pygame.draw.rect(win, (175, 171, 171), (0,0,500,25))
    pygame.draw.rect(win, (0,0,0), (0,0,400,25), 2)
    pygame.draw.rect(win, (0,0,0), (400,0,100,25), 2)

    font = pygame.font.SysFont('comicsans', 30)

    canvasText = font.render('Canvas', 1, (0,0,0))
    win.blit(canvasText, (int(200 - canvasText.get_width()/2), int(26/2 - canvasText.get_height() / 2)+2))
        
    toolsText = font.render('Tools', 1, (0,0,0))
    win.blit(canvasText, (int(450 - toolsText.get_width()/2), int(26/2 - toolsText.get_height() / 2+2)))

def draw(win):
    player1.click(win, Buttons_colour, Buttons_other)

    pygame.draw.rect(win, (0,0,0), (400, 1, 100, 500),2)

    pygame.draw.rect(win, (255,255,255),(400, 0, 100, 500),)
    pygame.draw.rect(win, (0,0,0),(0,0,400,500),2)

    drawHeader(win)

    for button in Buttons_colour:
        button.draw(win)
    for button in Buttons_other:
        button.draw(win)

    pygame.display.update()

def main_loop():
    run=True
    global last_pos
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False

            if pen_down == False:
                # Make tracking of mouse position even if not "pen_down"
                if event.type == pygame.MOUSEMOTION:
                    last_pos = event.pos


        draw(win)

    
        if 0 < player1.tick < 40:
            player1.tick += 1
        else:
            player1.tick = 0

        if 0 < player1.time < 4001:
            player1.time += 1
        elif 4000< player1.time < 4004:
            #gameOver()
            player1.time = 4009
        else:
            player1.time = 0
            player1.play = False
        

    pygame.quit()

player1 = drawing()

win.fill((255,255,255))
pos = (0,0)

redButton = button(453, 30, 40, 40, (255, 0, 0), (255, 0, 0))
blueButton = button(407, 30, 40, 40, (0, 0, 255), (0, 0, 255))
greenButton = button(407, 76, 40, 40, (0, 255, 0), (0, 255, 0))
orangeButton = button(453, 76, 40, 40, (255, 192, 0), (255, 192, 0))
yellowButton = button(407, 122, 40, 40, (255, 255, 0), (255, 255, 0))
purpleButton = button(453, 122, 40, 40, (112, 48, 160), (112, 48, 160))
blackButton = button(407, 168, 40, 40, (0, 0, 0), (0, 0, 0))
whiteButton = button(453, 168, 40, 40, (0, 0, 0), (255, 255, 255), 1)
 
clrButton = button(407, 214, 86, 40, (201, 201, 201), (0, 0, 0), 0, 1, 'Clear')
 
smallerButton = button(407, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 2, '-')
biggerButton = button(453, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 3, '+')
sizeDisplay = button(407, 306, 86, 40, (0, 0, 0), (0, 0, 0), 1, 4, 'Size')

Buttons_colour = [redButton, blueButton, greenButton, orangeButton,
                 yellowButton, purpleButton, blackButton, whiteButton]
Buttons_other = [clrButton, smallerButton, biggerButton,
                 sizeDisplay]
 
main_loop()
 
list = pygame.font.get_fonts()
print(list)