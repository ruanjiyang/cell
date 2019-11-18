from PIL import Image, ImageDraw, ImageFont
import random
import time
import pygame
import sys
pygame.init()
screen = pygame.display.set_caption('Cells Net Diagram')




width = 800
height = 600


# image = Image.new('RGBA', (width, height), 'white')
# imageDraw = ImageDraw.Draw(image)
cell_Qty = 0  # 细胞的总数量
cells = []  # 细胞的全体集合
friend_distance = 20  # 关联细胞的最大距离。  建议设置在 cell_size*cell_space_rate/1.5


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
            x=self.cell_size*self.cell_space_rate*(random.random()-0.5)*1
            y=self.cell_size*self.cell_space_rate*(random.random()-0.5)*1
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
                # print(_potential_friend.position)
                #print(cell_distance(_potential_friend, self))

    def draw_me(self):
        pygame.draw.circle(screen, [255, 0, 0], [int(self.position[0]), int(
            self.position[1])], self.cell_size, 1)  # (surface color  center radius width )
        # pygame.display.flip()
        # imageDraw.ellipse((self.position[0], self.position[1], self.position[0] +
        #                    self.cell_size*2, self.position[1]+self.cell_size*2), fill=(255,0,0))

    def draw_mother(self):
        if len(self.mother) > 0:
            for mother in self.mother:
                pygame.draw.line(screen, [0, 0, 255], [int(self.position[0]), int(self.position[1])], [int(
                    mother.position[0]), int(mother.position[1])], 1)  # line(surface, color, start_pos, end_pos, width=1)

    def draw_friend(self):
        if len(self.friend) > 0:
            for friend in self.friend:
                pygame.draw.line(screen, [255, 255, 0], [int(self.position[0]), int(self.position[1])], [int(
                    friend.position[0]), int(friend.position[1])], 1)  # line(surface, color, start_pos, end_pos, width=1)

    def draw_son(self):
        if len(self.son) > 0:
            for son in self.son:
                pygame.draw.line(screen, [0, 255, 0], [int(self.position[0]), int(self.position[1])], [int(
                    son.position[0]), int(son.position[1])], 1)  # line(surface, color, start_pos, end_pos, width=1)
    
    def random_move(self,speed):
        x=self.cell_size*self.cell_space_rate*(random.random()-0.5)*speed
        y=self.cell_size*self.cell_space_rate*(random.random()-0.5)*speed
        self.position = [self.position[0] +x, self.position[1]+y]



def split_all_cells(mother):
    mother.split()
    for son in mother.son[:-1]:
        split_all_cells(son)


def draw_cell_net(cellToDraw):
    global screen
    screen = pygame.display.set_mode([width, height])
    screen.fill([255, 255, 255])
    text = pygame.font.SysFont("Aril", 30)
    words = 'Total cells Qty:'+str(len(cellToDraw))
    words_to_display = text.render(words, 0, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for oneCell in cellToDraw:            
            oneCell.draw_me()
            oneCell.draw_friend()
            # oneCell.draw_mother()
            # oneCell.draw_son()
        screen.blit(words_to_display, (50, 50))
        pygame.display.flip()
        #time.sleep(0.2)
        cells_random_move(cells)
        screen.fill([255,255,255])
    # words = 'Total cells Qty:'+str(len(cellToDraw))
    # setFont = ImageFont.truetype(font="C:\Windows\Fonts\Arial.ttf", size=30)
    # imageDraw.text((50, 50), words, font=setFont, fill='black')


def cell_distance(cell1, cell2):
    return (((cell1.position[0]-cell2.position[0])**2+(cell1.position[1]-cell2.position[1])**2)**0.5)

def cells_random_move(cells):
    '''让所有细胞随机移动一次'''
    for cell in cells:
        cell.random_move(0.5)

    for cell in cells:
        '''移动之后，先清楚每个细胞的所有伙伴，然后重新找伙伴'''
        cell.friend.clear()
        cell.find_friends()


###############################################################
a = CELL()  # 元细胞，细胞祖先。

# while True:
#     pass


for i in range(10):  # 分裂 2的n次方。
    split_all_cells(a)



endCells = []  # 找出所有没有儿子的末端细胞
for cell in cells:
    if len(cell.son) == 0:
        endCells.append(cell)


# for i in range(600):  #让最后n个细胞批量死亡。
#     cells[-1].dead()

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
