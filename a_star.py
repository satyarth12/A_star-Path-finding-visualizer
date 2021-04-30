import pygame
import math
from queue import PriorityQueue


WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)



'''
For keeping the track of different nodes present in the grid.
1. Where the node is (rows and columns)
2. Width of the node itself
3. Track the node's neighbours
'''
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		#x and y are the starting positions
		self.x = row*width
		self.y = col*width

		self.color = WHITE
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows


	def get_pos(self):
		return self.row, self.col

	#it is like have we already considered or looked at a particular node
	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, WIN):
		pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbours = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #going down a row
			self.neighbours.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #going up a row
			self.neighbours.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #going right a column
			self.neighbours.append(grid[self.row][self.col + 1])

		if self.col < 0 and not grid[self.row][self.col - 1].is_barrier(): #going left a column
			self.neighbours.append(grid[self.row][self.col - 1])


	def __lt__(self, other): #less than
		return False


#we'll use manhattan distance , L distances
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1-x2) + abs(y1-y2)


def show_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()



def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			show_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbours:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:

				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False








'''
We'll need a data structure that can hold up the nodes so that we can manipulate them,
like traversing and using them.
'''
def make_grid(rows, width):
	grid = []
	gap = width // rows #floor division, gap between each rows or width of each cube
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


'''
Drawing grid lines so that we can easily see the nodes
'''
def draw_grid(WIN, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(WIN, GREY, (0, i*gap), (width, i*gap))

		for j in range(rows):
			pygame.draw.line(WIN, GREY, (j*gap, 0), (j*gap, width))



def draw(WIN, grid, rows, width):
	WIN.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(WIN) #draw function in the Node class


	draw_grid(WIN, rows, width)
	pygame.display.update()




'''
Function for figuring out that which spot needs to change color when clicked, based on the mouse position
'''
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y,x = pos

	#getting the mouse position and dividing it with the width of each cube
	row = y // gap
	col = x // gap

	return row, col


def main(WIN, width):
	ROWS = 50
	grid = make_grid(ROWS, width)
	# print(grid[0])
	# for row in grid:
	# 	for spot in row:
	# 		print(spot)

	start = None
	end = None

	run = True
	started = False #whether the algo is started or not

	while  run:
		draw(WIN, grid, ROWS, width)
		for event in pygame.event.get(): #check all the loops that happened, such as mouse clicking
			if event.type == pygame.QUIT:
				run =  False

			if started: #don't allow the user to do anything except quiting, once the algo has started
				continue

			if pygame.mouse.get_pressed()[0]: #clicking left mouse button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != start and spot != end:
					spot.make_barrier()


			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()

				if spot == start:
					start = None
				elif spot == end:
					end = None


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(WIN, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)



	pygame.quit()	



main(WIN, WIDTH)





























