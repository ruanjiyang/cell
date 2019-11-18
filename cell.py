from PIL import Image, ImageDraw, ImageFont
import random

width = 1024
height = 1024
image = Image.new('RGBA', (width, height), 'white')
imageDraw = ImageDraw.Draw(image)
cell_Qty = 0  # 细胞的总数量
cells = []  # 细胞的全体集合
friend_distance = 20  # 关联细胞的坐标距离。  建议设置在 cell_size*cell_space_rate/1.5


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
    cell_size = 4
    cell_space_rate = 30
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
        del self

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
        imageDraw.ellipse((self.position[0], self.position[1], self.position[0] +
                           self.cell_size*2, self.position[1]+self.cell_size*2), fill=(255,0,0))

    def draw_mother(self):
        if len(self.mother) > 0:
            for mother in self.mother:
                # imageDraw.ellipse((mother.position[0], mother.position[1], mother.position[0] +
                #                    mother.cell_size*2, mother.position[1]+mother.cell_size*2), fill='red')
                imageDraw.line(
                    (self.position[0], self.position[1], mother.position[0], mother.position[1]), fill='blue', width=2)

    def draw_friend(self):
        if len(self.friend) > 0:
            for friend in self.friend:
                # imageDraw.ellipse((friend.position[0], friend.position[1], friend.position[0] +
                #                    friend.cell_size*2, friend.position[1]+friend.cell_size*2), fill='red')
                imageDraw.line(
                    (self.position[0], self.position[1], friend.position[0], friend.position[1]), fill='yellow', width=2)

    def draw_son(self):
        if len(self.son) > 0:
            for son in self.son:
                # imageDraw.ellipse((son.position[0], son.position[1], son.position[0] +
                #                    son.cell_size*2, son.position[1]+son.cell_size*2), fill='red')
                imageDraw.line(
                    (self.position[0], self.position[1], son.position[0], son.position[1]), fill='blue', width=2)


def split_all_cells(mother):
    mother.split()
    for son in mother.son[:-1]:
        split_all_cells(son)


def draw_cell_net(cellToDraw):
    for oneCell in cellToDraw:
        oneCell.draw_me()
        oneCell.draw_mother()
        # oneCell.draw_son()
        oneCell.draw_friend()

    words = 'Total cells Qty:'+str(len(cellToDraw))
    setFont = ImageFont.truetype(font="C:\Windows\Fonts\Arial.ttf", size=30)
    imageDraw.text((50, 50), words, font=setFont, fill='black')


def cell_distance(cell1, cell2):
    return (((cell1.position[0]-cell2.position[0])**2+(cell1.position[1]-cell2.position[1])**2)**0.5)


###############################################################
a = CELL() #元细胞，细胞祖先。

for i in range(10):
    split_all_cells(a)

for cell in cells:
    cell.find_friends()

endCells=[]  #找出所有没有儿子的末端细胞
for cell in cells:
    if len(cell.son)==0:
        endCells.append(cell)



for i in range(600):  #让最后n个细胞批量死亡。
    cells[-1].dead()

# # for cell in cells:  #让编号为n的 细胞死亡
# #     if cell.cell_number==10:
# #         cell.dead()

# # for cell in cells:  #让hp<=0的 细胞死亡
# #     if cell.hp<=0:
# #         cell.dead()

# for cell in cells:  #让无朋友的所有细胞死亡
#     if len(cell.friend)<=0:
#         cell.dead()


draw_cell_net(cells)

image.show()

