from PIL import Image, ImageDraw, ImageFont
import random
import turtle as pen
import time

width = 0
height = 0
pen.screensize(1200,1200, "white")
pen.speed('fastest')
pen.Turtle().screen.delay(0)


cell_Qty = 0  # 细胞的总数量
cells = []  # 细胞的全体集合
friend_distance = 80  # 关联细胞的坐标距离。  建议设置在 cell_size*cell_space_rate/1.5

def DrawPixel(x,y,dotsize) :
    x=int(x)
    y=int(y)
    pen.up()		#因为turtle在执行goto()时，
					#会在路径上画出一条直线，
					#所以先把笔抬起来
    pen.goto(x,y)	#turtle到指定坐标像素点
    pen.dot(dotsize,'red')

def DrawLine(x1,y1,x2,y2) :
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    print ("called")
    dx = abs(x2 - x1)
    sx = 1 if(x1<x2) else -1
    dy = abs(y2 - y1)
    sy = 1 if(y1<y2) else -1
    err = dx if(dx>dy) else -dy
    l = dx if(dx>dy) else dy
    for i in range(0,l) :
        DrawPixel(x1,y1,2)
        if x1 == x2 and y1 == y2 :
            break
        e2 = err
        if e2 >= -dx :
            err = err - dy
            x1 = x1 + sx
        if e2 <= dy :
            err = err + dx
            y1 = y1 + sy

# 原文链接：https:#blog.csdn.net/liulimengtianxia/article/details/84033261


class CELL:
    global cells, cell_Qty, width, height
    cell_number = 0
    generation = 0
    mother = []
    son = []
    friend = []
    position = [width/2, height/2]
    input_power = 0
    output_power = 0
    cell_size = 12
    cell_space_rate = 10
    hp = 100  # 生命值，等于0，表示死亡.

    def __init__(self):
        global cell_Qty, cells
        self.cell_number = cell_Qty
        cell_Qty = cell_Qty+1
        cells.append(self)
        #print('新生成细胞，ID为', self.cell_number)

    def mother_add(self, cell):
        self.mother.append(cell)
        #print('细胞', self.cell_number, '添加了一个母细胞', cell.cell_number)
        self.set_generation()  # 在添加一个mother后， 设置代数。

    def mother_del(self, cell):
        self.mother.remove(cell)
        #print('细胞', self.cell_number, '删除了一个母细胞', cell.cell_number)

    def son_add(self, cell):
        self.son.append(cell)
        #print('细胞', self.cell_number, '添加了一个子细胞', cell.cell_number)

    def son_del(self, cell):
        self.son.remove(cell)
        #print('细胞', self.cell_number, '删除了一个子细胞', cell.cell_number)

    def set_postion(self):
        if self.mother == []:
            self.position = [width/2, height/2]
        else:
            if random.random() > 0.5:
                x = self.cell_size*self.cell_space_rate*(random.random())
            else:
                x = -self.cell_size*self.cell_space_rate*(random.random())
            if random.random() > 0.5:
                y = self.cell_size*self.cell_space_rate*(random.random())
            else:
                y = -self.cell_size*self.cell_space_rate*(random.random())
            self.position = [self.mother[0].position[0] +
                             x, self.mother[0].position[1]+y]
        ##print('新生成细胞的坐标是', self.position)

    def split(self):
        son = CELL()
        son.son = []  # 新生成的细胞，为什么一定要先清空一下上下链接呢？
        son.mother = []  # 新生成的细胞，为什么一定要先清空一下上下链接呢？
        son.friend = []
        #print('细胞', self.cell_number, '分裂出了一个子细胞', son.cell_number)
        if son not in self.son:
            self.son_add(son)
        if self not in son.mother:
            son.mother_add(self)
        son.set_postion()

    def dead(self):
        global cells

        for mother in self.mother:
            mother.son.remove(self)

        for son in self.son:
            son.mother.remove(self)

        for friend in self.friend:
            friend.friend.remove(self)

        cells.remove(self)

    def set_input_power(self):
        self.input_power = 0
        for cell in self.mother:
            self.input_power += cell.output_power
        #print('细胞', self.cell_number, '获取能量', self.input_power)

    def set_output_power(self, power):
        self.output_power = power
        #print('细胞', self.cell_number, '产生能量', self.output_power)

    def set_generation(self):
        '''设置第几代的细胞'''
        if self.mother == []:
            self.generation = 0
        else:
            self.generation = self.mother[0].generation+1

    def find_friends(self):
        for _potential_friend in cells:
            if cell_distance(_potential_friend, self) < friend_distance and _potential_friend != self:
                self.friend.append(_potential_friend)
                #print("===", self.position)
                #print(_potential_friend.position)
                #print(cell_distance(_potential_friend, self))

    def draw_me(self):
        global pen
        pen.pensize(30)
        pen.color("blue")
        DrawPixel(self.position[0], self.position[1],5)

    def draw_mother(self):
        if len(self.mother) > 0:
            for mother in self.mother:
                # imageDraw.ellipse((mother.position[0], mother.position[1], mother.position[0] +
                #                    mother.cell_size*2, mother.position[1]+mother.cell_size*2), fill='red')
                DrawLine(self.position[0], self.position[1], mother.position[0], mother.position[1])

    def draw_friend(self):
        if len(self.friend) > 0:
            for friend in self.friend:
                DrawLine(self.position[0], self.position[1], friend.position[0], friend.position[1])

    def draw_son(self):
        if len(self.son) > 0:
            for son in self.son:
                DrawLine(self.position[0], self.position[1], son.position[0], son.position[1])


def split_all_cells(mother):
    mother.split()
    for son in mother.son[:-1]:
        split_all_cells(son)


def draw_cell_tree():
    for oneCell in cells:
        oneCell.draw_me()
        oneCell.draw_mother()
        oneCell.draw_son()
        oneCell.draw_friend()

    words = 'Total cells Qty:'+str(len(cells))
    # setFont = ImageFont.truetype(font="C:\Windows\Fonts\Arial.ttf", size=30)
    # imageDraw.text((50, 50), words, font=setFont, fill='black')


def cell_distance(cell1, cell2):
    return (((cell1.position[0]-cell2.position[0])**2+(cell1.position[1]-cell2.position[1])**2)**0.5)


###############################################################
a = CELL() #元细胞，细胞祖先。

for i in range(4):
    split_all_cells(a)

for cell in cells:
    cell.find_friends()

# for i in range(10):  #让最后n个细胞批量死亡。
#     cells[-1].dead()

# for cell2dead in cells:  #让编号为n的 细胞死亡
#     if cell2dead.cell_number==10:
#         cell2dead.dead()

# for cell in cells:  #让hp<=0的 细胞死亡
#     if cell.hp<=0:
#         cell.dead()

# for cell in cells:  #让无朋友的所有细胞死亡
#     if len(cell.friend)<=0:
#         cell.dead()

draw_cell_tree()

pen.done()
