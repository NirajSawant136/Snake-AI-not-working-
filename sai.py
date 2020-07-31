import pygame
import os
import time
import random
import neat


BLOCK_SIZE = 300
GRID_SIZE = 20
SIZE = BLOCK_SIZE//GRID_SIZE

SNAKE_X = [x for x in range(17)]
SNAKE_Y = [y for y in range(1, 17)]

print(SNAKE_X, SNAKE_Y)

GREY = (150, 150, 150)
BLACK = (0,0,0)
RED = (250, 50, 50)
ORANGE = (250, 120, 10)

GREEN = (23, 250, 40)
LIGHT_GREEN = (23, 150, 40)

GRID = [(0,0), (0, BLOCK_SIZE), (0, 2*BLOCK_SIZE), (0, 3*BLOCK_SIZE), (0, 4*BLOCK_SIZE),
		(BLOCK_SIZE, 0), (BLOCK_SIZE, BLOCK_SIZE), (BLOCK_SIZE, 2*BLOCK_SIZE), (BLOCK_SIZE, 3*BLOCK_SIZE), (BLOCK_SIZE, 4*BLOCK_SIZE)]

CELLS = [(x//GRID_SIZE, x - (x//GRID_SIZE)*GRID_SIZE) for x in range(GRID_SIZE*GRID_SIZE)]

def drawGrid(world):
	pygame.draw.line(world, GREY, (BLOCK_SIZE, 0), (BLOCK_SIZE, 2*BLOCK_SIZE), 3)
	pygame.draw.line(world, GREY, (2*BLOCK_SIZE, 0), (2*BLOCK_SIZE, 2*BLOCK_SIZE), 3)
	pygame.draw.line(world, GREY, (3*BLOCK_SIZE, 0), (3*BLOCK_SIZE, 2*BLOCK_SIZE), 3)
	pygame.draw.line(world, GREY, (4*BLOCK_SIZE, 0), (4*BLOCK_SIZE, 2*BLOCK_SIZE), 3)
	pygame.draw.line(world, GREY, (0, BLOCK_SIZE), (5*BLOCK_SIZE, BLOCK_SIZE), 3)

	pygame.draw.rect(world, GREY, (0, 0, 5*BLOCK_SIZE, 2*BLOCK_SIZE), 3)
	pygame.display.update()


class Snake:
	MAX_MOVES = 500
	INIT_MOVES = 200
	ADD_MOVES = 100
	def __init__(self,x, y, GRID_POS, world, index):
		self.X = GRID_POS[0]
		self.Y = GRID_POS[1]
		self.body = [(x, y), (x, y+1), (x, y+2)]
		self.WALLS = []
		self.tail = (-1, -1)
		self.moves = self.INIT_MOVES
		self.defineWalls(world)
		self.index = index
		self.draw(world)

	def defineWalls(self, world):
		WALLS1 = [(-1 + self.X, x + self.Y) for x in range(-1, 21)]
		WALLS2 = [(20 + self.X, x + self.Y) for x in range(-1, 21)]
		WALLS3 = [(x + self.X, -1 + self.Y) for x in range(-1, 21)]
		WALLS4 = [(x + self.X, 20 + self.Y) for x in range(-1, 21)]

		self.WALLS = WALLS1 + WALLS2 + WALLS3 + WALLS4

		# print(self.WALLS)
		# for part in self.WALLS:
		# 	pygame.draw.rect(world, RED, ( (part[1] - self.Y)*SIZE + self.Y, (part[0] - self.X)*SIZE + self.X, SIZE, SIZE), 0)

		# pygame.display.update()

	def draw(self, world):
		if self.index < 10:
			for part in self.body:
				pygame.draw.rect(world, RED, (part[1]*SIZE + self.Y, part[0]* SIZE + self.X, SIZE, SIZE), 0)
				pygame.draw.rect(world, BLACK, (part[1]*SIZE + self.Y, part[0]* SIZE + self.X, SIZE, SIZE), 1)

			pygame.draw.rect(world, ORANGE, (self.body[0][1]*SIZE + self.Y, self.body[0][0]* SIZE + self.X, SIZE, SIZE), 0)
			pygame.draw.rect(world, BLACK, (self.body[0][1]*SIZE + self.Y, self.body[0][0]* SIZE + self.X, SIZE, SIZE), 1)

			pygame.draw.rect(world, BLACK, (self.tail[1]*SIZE + self.Y, self.tail[0]* SIZE + self.X, SIZE, SIZE), 0)

			pygame.display.update()

	def collideSelf(self, dirs):
		snake_direction = (self.body[1][0] - self.body[0][0], self.body[1][1] - self.body[0][1])
		

	# Dir = next(x for x, op in enumerate(output) if op == 1)
		Dir = 0
		if dirs == (1, 0, 0):
			Dir = -1
		elif dirs == (0, 1, 0):
			Dir = 0
		elif dirs == (0, 0, 1):
			Dir = 1

		direction = 0

		if snake_direction[0] == 0:
			if snake_direction[1] == 1:
				direction = 3
			elif snake_direction[1] == -1:
				direction = 1

		elif snake_direction[1] == 0:
			if snake_direction[0] == 1:
				direction = 0
			elif snake_direction[0] == -1:
				direction = 2

		dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

		move = dirs[(direction + Dir) % 4]
		head = (self.body[0][0] + move[0], self.body[0][1] + move[1])

		if head in self.body:
			return True

		return False

	def collideWall(self, dirs):
		snake_direction = (self.body[1][0] - self.body[0][0], self.body[1][1] - self.body[0][1])
		

	# Dir = next(x for x, op in enumerate(output) if op == 1)
		Dir = 0
		if dirs == (1, 0, 0):
			Dir = -1
		elif dirs == (0, 1, 0):
			Dir = 0
		elif dirs == (0, 0, 1):
			Dir = 1

		direction = 0

		if snake_direction[0] == 0:
			if snake_direction[1] == 1:
				direction = 3
			elif snake_direction[1] == -1:
				direction = 1

		elif snake_direction[1] == 0:
			if snake_direction[0] == 1:
				direction = 0
			elif snake_direction[0] == -1:
				direction = 2

		dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

		move = dirs[(direction + Dir) % 4]
		head = (self.body[0][0] + move[0] + self.X, self.body[0][1] + move[1] + self.Y)

		# print(head)

		if head in self.WALLS:
			return True
		
		return False


	def move(self, output):
		snake_direction = (self.body[1][0] - self.body[0][0], self.body[1][1] - self.body[0][1])
		# print(snake_direction)

		# Dir = next(x for x, op in enumerate(output) if op == 1)

		if output == (1, 0, 0):
			Dir = -1
		elif output == (0, 1, 0):
			Dir = 0
		elif output == (0, 0, 1):
			Dir = 1

		# print(Dir)

		direction = 0

		if snake_direction[0] == 0:
			if snake_direction[1] == 1:
				direction = 3
			elif snake_direction[1] == -1:
				direction = 1

		elif snake_direction[1] == 0:
			if snake_direction[0] == 1:
				direction = 0
			elif snake_direction[0] == -1:
				direction = 2

		dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

		# print((direction - Dir))

		move = dirs[(direction + Dir) % 4]

		self.tail = self.body[len(self.body) - 1]

		for i in range(len(self.body)-1, 0, -1):
			self.body[i] = self.body[i-1]

		self.body[0] = (self.body[0][0] + move[0], self.body[0][1] + move[1])

		self.moves -= 1

	def grow(self):
		tail = self.body[len(self.body) - 1]

		self.body.append(tail)

		self.moves += self.ADD_MOVES

		if self.moves > self.MAX_MOVES:
			self.moves = self.MAX_MOVES


class Food:
	def __init__(self, snake):
		self.snake = snake.body
		self.x = 0
		self.y = 0
		self.X = snake.X
		self.Y = snake.Y
		self.distance = 0
		self.prX = -1
		self.prY = -1
		self.setPos(snake)
		self.setDist(snake)

	def setPos(self, snake):
		self.snake = snake.body

		possibilities = list(set(CELLS) - set(self.snake))

		position = random.choice(possibilities)

		self.prX = self.x
		self.prY = self.y

		self.x = position[0] 
		self.y = position[1] 

	def draw(self, world):
		pygame.draw.rect(world, LIGHT_GREEN, (self.y*SIZE + self.Y, self.x* SIZE + self.X, SIZE, SIZE), 0)
		pygame.draw.rect(world, GREEN, (self.y*SIZE + self.Y, self.x* SIZE + self.X, SIZE, SIZE), 2)

		pygame.draw.rect(world, BLACK, (self.prY*SIZE + self.Y, self.prX* SIZE + self.X, SIZE, SIZE), 0)
		pygame.draw.rect(world, BLACK, (self.prY*SIZE + self.Y, self.prX* SIZE + self.X, SIZE, SIZE), 2)

		pygame.display.update()

	def setDist(self, snake):
		self.snake = snake.body

		distance = ((self.snake[0][0] - self.x)**2 + (self.snake[0][1] - self.y)**2)**0.5

		self.distance = distance

def isClear(snake, Dir):
	snake_direction = (snake.body[1][0] - snake.body[0][0], snake.body[1][1] - snake.body[0][1])
		

	# Dir = next(x for x, op in enumerate(output) if op == 1)

	if Dir == -1:
		Dirs = (1, 0, 0)
	elif Dir == 0:
		Dirs = (0, 1, 0)
	elif Dir == 1:
		Dirs = (0, 0, 1)

	# direction = 0

	# if snake_direction[0] == 0:
	# 	if snake_direction[1] == 1:
	# 		direction = 3
	# 	elif snake_direction[1] == -1:
	# 		direction = 1

	# elif snake_direction[1] == 0:
	# 	if snake_direction[0] == 1:
	# 		direction = 0
	# 	elif snake_direction[0] == -1:
	# 		direction = 2

	# dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

	# move = dirs[(direction + Dir) % 4]
	# head = (snake.body[0][0] + move[0], snake.body[0][1] + move[1])

	if snake.collideSelf(Dirs) or snake.collideWall(Dirs):
		return 0

	return 1

def whereIsFood(snake, food):
	snake_direction = (snake.body[1][0] - snake.body[0][0], snake.body[1][1] - snake.body[0][1])
		

	# Dir = next(x for x, op in enumerate(output) if op == 1)

	# if Dir == 0:
	# 	Dir = -1
	# elif Dir == 1:
	# 	Dir = 0
	# elif Dir == 2:
	# 	Dir = 1
	left = -1
	forward = 0
	right = 1

	direction = 0

	if snake_direction[0] == 0:
		if snake_direction[1] == 1:
			direction = 3
		elif snake_direction[1] == -1:
			direction = 1

	elif snake_direction[1] == 0:
		if snake_direction[0] == 1:
			direction = 0
		elif snake_direction[0] == -1:
			direction = 2

	dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

	Left = dirs[(direction + left) % 4]
	Right = dirs[(direction + right) % 4]
	Forward = dirs[(direction + forward) % 4]

	head = snake.body[0]
	headLeft = (head[0] + Left[0], head[1] + Left[1])
	headRight = (head[0] + Right[0], head[1] + Right[1])
	headForward = (head[0] + Forward[0], head[1] + Forward[1])

	distLeft = ((headLeft[0] - food.x)**2 + (headLeft[1] - food.y)**2)**0.5
	distRight = ((headRight[0] - food.x)**2 + (headRight[1] - food.y)**2)**0.5
	distForward = ((headForward[0] - food.x)**2 + (headForward[1] - food.y)**2)**0.5

	minDist = min(distLeft, distRight, distForward)

	# print(head)
	# print()
	# print(headLeft)
	# print(headRight)
	# print(headForward)

	Foods = []
	if minDist == distLeft:
		Foods = [1, 0, 0]

	elif minDist == distRight:
		Foods = [0, 0, 1]

	elif minDist == distForward:
		Foods = [0, 1, 0]

	return Foods

def finalDirection(snake, maxOutput):
	if maxOutput == 0:
		Dir = -1
	elif maxOutput == 1:
		Dir = 0

	elif maxOutput == 2:
		Dir = 1

	snake_direction = (snake.body[1][0] - snake.body[0][0], snake.body[1][1] - snake.body[0][1])
		

	# Dir = next(x for x, op in enumerate(output) if op == 1)

	# if Dir == 0:
	# 	Dir = -1
	# elif Dir == 1:
	# 	Dir = 0
	# elif Dir == 2:
	# 	Dir = 1

	direction = 0

	if snake_direction[0] == 0:
		if snake_direction[1] == 1:
			direction = 3
		elif snake_direction[1] == -1:
			direction = 1

	elif snake_direction[1] == 0:
		if snake_direction[0] == 1:
			direction = 0
		elif snake_direction[0] == -1:
			direction = 2

	dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

	move = dirs[(direction + Dir) % 4]
	head = (snake.body[0][0] + move[0], snake.body[0][1] + move[1])

	return head


# world = pygame.display.set_mode((5*BLOCK_SIZE, 2*BLOCK_SIZE))


# drawGrid(world)
# snake = Snake(4, 10, GRID[6], world)
# snake.draw(world)
# snake.move((1, 0, 0))
# print(snake.body)
# time.sleep(1.2)

# food = Food(snake)
# food.draw(world)
# print(food.distance)

# world.fill(BLACK)
# drawGrid(world)
# snake.draw(world)

# while not snake.collideWall((0, 1, 0)):
# 	time.sleep(1.2)
# 	snake.move((0, 1, 0))
# 	world.fill(BLACK)
# 	drawGrid(world)
# 	snake.draw(world)
	

# inputs = whereIsFood(snake, food)
# inputs.append(isClear(snake, -1))
# inputs.append(isClear(snake, 0))
# inputs.append(isClear(snake, 1))

# print(inputs)

# run = True
# while run:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			run = False
# 			pygame.quit()

def eval_genomes(genomes, config):
	world = pygame.display.set_mode((5*BLOCK_SIZE, 2*BLOCK_SIZE))
	drawGrid(world)

	nets = []
	ge = []
	snakes = []
	foods = []

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		g.fitness = 0
		ge.append(g)

	for i in range(77):
		snakes.append(Snake(random.choice(SNAKE_X), random.choice(SNAKE_Y), GRID[i % 10], world, i))

	for snake in snakes:
		foods.append(Food(snake))

	for x, food in enumerate(foods):
		if x < 10:
			food.draw(world)
	# time.sleep(1.3)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

		for x, snake in enumerate(snakes):
			# time.sleep(0.0005)

			inputs = whereIsFood(snake, food)
			inputs.append(isClear(snake, -1))
			inputs.append(isClear(snake, 0))
			inputs.append(isClear(snake, 1))
			# inputs.append(foods[x].x)
			# inputs.append(foods[x].y)

			# print(x, end=" | ")
			output = nets[x].activate(inputs)
			# if output == [0.0, 0.0, 0.0]:
			# 	print("O", end=" | ")

			OP = (int(10*output[0]), int(10*output[1]), int(10*output[2]))

			# print(OP, end="|")
			# print(x, output, end = " || ")

			# Choice = []
			# if output == [0.0, 0.0, 0.0]:
			# 	print("messed up!", end=" ,, ")
			# 	if isClear(snake, -1) == 1:
			# 		Choice.append(0)

			# 	if isClear(snake, 0) == 1:
			# 		Choice.append(1)

			# 	if isClear(snake, 1) == 1:
			# 		Choice.append(2)

			# 	if len(Choice) > 0:
			# 		maxOutput = random.choice(Choice)
			# 	else:
			# 		maxOutput = random.choice((0, 1, 2))

			# else:
			# 	maxOutput = next(x for x, op in enumerate(output) if op == max(output))

			maxOutput = next(x for x, op in enumerate(output) if op == max(output))

			if maxOutput == 0:
				output = (1, 0, 0)

			elif maxOutput == 1:
				output = (0, 1, 0)

			elif maxOutput == 2:
				output = (0, 0, 1)

			headed = finalDirection(snake, maxOutput)

			rem = []
			if snake.collideWall(output) or snake.collideSelf(output):
				ge[x].fitness -= 10
				rem.append(snake)
				# nets.pop(x)
				# ge.pop(x)
				# foods.pop(x)
				# snakes.pop(x)

			else:
				snake.move(output)
				snake.draw(world)
				drawGrid(world)

				# ge[x].fitness += 0.1

				if foods[x].distance >= ((snake.body[0][0] - foods[x].x)**2 + (snake.body[0][1] - foods[x].y)**2)**0.5:
					# print(foods[x].distance ,((snake.body[0][0] - foods[x].x)**2 + (snake.body[0][1] - foods[x].y)**2)**0.5)
					ge[x].fitness += 1

				else:
					ge[x].fitness -= 1.5

				foods[x].setDist(snake)

				if (foods[x].x, foods[x].y) == snake.body[0]:
					ge[x].fitness += 100
					snake.grow()
					foods[x].setPos(snake)
					if x < 10:
						foods[x].draw(world)

				if snake.moves <= 0:
					rem.append(snake)
					ge[x].fitness -= 10
					# nets.pop(x)
					# ge.pop(x)
					# foods.pop(x)
					# snakes.pop(x)
		

		for snake in rem:
			x = snakes.index(snake)
			nets.pop(x)
			ge.pop(x)
			foods.pop(x)
			snakes.remove(snake)

		if len(snakes) == 0:
			run = False
			break


def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
						neat.DefaultSpeciesSet, neat.DefaultStagnation,
						config_path)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(eval_genomes)

	print("Best fitness -> {}".format(winner))


if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-FeedForward.txt")
	run(config_path)
