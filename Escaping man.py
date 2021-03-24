from tkinter import *
import random    #### если он не нужен, лучше его не импортировать
import time
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Escaping man")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.text = self.canvas.create_text(500,500, text = 'saa')
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="stickman/background.gif")
        w = self.bg.width()
        h = self.bg.height() 
        for x in range (0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h, image=self.bg, anchor="nw")
        self.sprites = []
        self.running = True
        l = Label()
    def mainloop(self):
        while 1:
            if self.running ==True:
                for sprite in self.sprites:
                    sprite.move()
               
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
class Coords:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def within_x(co1, co2):
        if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
            return True
        else:
            return False
        
    def within_y(co1, co2):
        if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
           or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
           or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
           or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
            return True
        else:
            return False
    def collided_left(co1, co2):
        if Coords.within_y(co1, co2):
            if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:    # до этого здесь была такая же проверка что и сверху
                return True                              #скорее всего вы просто опечатались
        return False                                  #проверьте по кинге ещё раз, увидите

    def collided_right(co1, co2):
        if Coords.within_y(co1, co2):
            if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
                return True
        return False
    def collided_top(co1, co2):
        if Coords.within_x(co1, co2):
            if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
                return True
        return False
    def collided_bottom(y: int, co1, co2):
        if Coords.within_x(co1, co2):
            y_calc = co1.y2 + y
            if y_calc >= co2.y1 and y_calc <= co2.y2:
                return True
        return False

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates
    
class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprite(Sprite):

    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="stickman/figure-L1.gif"),
            PhotoImage(file="stickman/figure-L2.gif"),
            PhotoImage(file="stickman/figure-L3.gif"),
        ]
        self.images_right = [
            PhotoImage(file="stickman/figure-R1.gif"),
            PhotoImage(file="stickman/figure-R2.gif"),
            PhotoImage(file="stickman/figure-R3.gif"),
        ]
        self.images_door = [
            PhotoImage(file='stickman/door1.gif'),
            PhotoImage(file='stickman/door2.gif')
        ]

        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        self.co = None
        
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)
        self.ara = DoorSprite(g, PhotoImage(file="stickman/door1.gif"), 45, 30, 40, 35,1)
        g.sprites.append(self.ara)
    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2   
    def turn_right(self, evt):
        if self.y == 0: 
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 1


    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])      
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])       
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

#получение позиции фигурки
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1] 
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

#Перемещение фигурки по экрану
    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20: 
                self.y = 4 
        if self.y > 0:
            self.jump_count -= 1

#вызываем функцию coords, которая возвращает позицию фигурки на экране, и сохраняем эту позицию в переменной co. 
        self.co = self.coords()

        print(self.co.x1,self.co.x2, self.co.y1, self.co.y2)
#создаем следующие 5 переменных, они нам нужны чтобы проверять фигурку на столкновения с каждой из 4 сторон падения
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        
#проверяем столкнулась ли фигурка с верхней или нижней границей холста
        if self.y > 0 and self.co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and self.co.y1 <=0:
            self.y = 0
            top = False
            
#проверяем столкнулась ли фигурка с левой или правой границей холста
        if self.x > 0 and self.co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False 
        elif self.x < 0 and self.co.x1 <= 0:
            self.x = 0
            left = False

#столкновение с другими спрайтами
        #door1 = DoorSprite(g, PhotoImage(file="stickman/door1.gif"), 45, 30, 40, 35)
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and Coords.collided_top(self.co, sprite_co):  ###обратите внимание как я обращаюсь к методу collided_top
                self.y = -self.y                                           #обязательно прописываем до него название класса
                top = False                                                ##иначе не будет найден метод

#столкновение нижней стороной   
#данный код служит для обработки столкновения фигурки нижней стороной с каким либо из спрайтов



            if bottom and self.y > 0 and Coords.collided_bottom(self.y, self.co, sprite_co):   ##то же самое здесь
                self.y = sprite_co.y1 - self.co.y2
                if self.y < 0: #####так же эта проверка стояла не в теле предыдущего if
                    self.y = 0  ##она должна стоять именно в теле предыдщего if, так один зависит от другого
                bottom = False
                top = False

#код след. проверки для обрабокти ситуции, когда фигурка находиться на платформе и может выбежать за её край
        
            if bottom and falling and self.y == 0 and self.co.y2 < self.game.canvas_height and Coords.collided_bottom(1, self.co, sprite_co):
                falling = False

#столкновения слева и справа с другими объектами

            if left and self.x < 0 and Coords.collided_left(self.co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.game.running = False
            if right and self.x > 0 and Coords.collided_right(self.co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.game.running = False


        if (self.co.x1 == 64.0 and self.co.x2 == 91.0 and self.co.y1 == 30.0 and self.co.y2==60.0):
            self.game.canvas.itemconfig(self.image, image='')
            g.canvas.create_text(250,250,text = 'Вы победили', fill = 'blue', font = ("Times", 65))

        if falling and bottom and self.y == 0 and self.co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)
class DoorSprite(Sprite):
    def __init__(self,game,photo_image,x,y,width,height, count = 0, change = False):
        Sprite.__init__(self,game)
        self.images_door = [
            PhotoImage(file='stickman/door1.gif'),
            PhotoImage(file='stickman/door2.gif')
        ]

        self.image = game.canvas.create_image(x, y, image=self.images_door[0+count], anchor='nw')
        self.photo_image = photo_image
        self.coordinates = Coords(x,y, x + (width/2), y + height)
        self.endgame=True


g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), 0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), 150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), 300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="stickman/platform1.gif"), 300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), 175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), 50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), 170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="stickman/platform2.gif"), 45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file="stickman/platform3.gif"), 170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="stickman/platform3.gif"), 230, 200, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()
#Класс Game будет главным управляющим классом игры, а объекты класса Coords используем для хранения позиций графических объектов (платформ и человечка)
