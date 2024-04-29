from settings import *


class Player(object):

	""" This class defines the player/agent object and has methods to draw and move them """

	def __init__(self):
		self.x = GAME_WIDTH / 2
		self.y = HEIGHT / 2
		self.width = 90
		self.height = 127
		self.speed = 5
		self.color = None
		self.hitbox = pygame.Rect(self.x, self.y, 90, 127)  

	def draw(self):
		window.blit(PLAYER, (self.x, self.y))
		self.hitbox = pygame.Rect(self.x, self.y, 90, 127)
		#pygame.draw.rect(WINDOW, GREEN, self.hitbox, 2)

		rect_x = self.x + 30
		rect_y = self.y + 65
		rect_size = (29, 27)

		pygame.draw.rect(window, self.color, pygame.Rect(rect_x, rect_y, *rect_size))

	def draw_player_at_neural_net(self, x, y):
		window.blit(PLAYER, (x, y))

		rect_x = x + 30
		rect_y = y + 65
		rect_size = (29, 27)

		pygame.draw.rect(window, self.color, pygame.Rect(rect_x, rect_y, *rect_size))

	def move_up(self):
		if self.y >= 10:
			self.y -= self.speed
			
	def move_down(self):
		if self.y < HEIGHT - 10 - self.height:
			self.y += self.speed

	def move_left(self):
		if self.x > 10:
			self.x -= self.speed
			
	def move_right(self):
		if self.x < GAME_WIDTH - 10 - self.width:
			self.x += self.speed


class Asteroid(object):

	""" This class defines the asteroid object and the function to draw it to the screen"""

	def __init__(self, x, falling=False):
		self.x = x
		self.y = random.uniform(-200, -90)
		self.width = 88
		self.height = 88
		self.speed = 3
		self.hitbox = (self.x + 10, self.y - 5, 80, 80)
		self.falling = falling

	def draw(self):
		window.blit(ASTEROID, (int(self.x + 6), int(self.y - 10)))
		self.hitbox = (self.x + 10, self.y - 5, 80, 80)
		#pygame.draw.rect(WINDOW, GREEN, self.hitbox, 2)


class NeuralNet(object):

	""" Tis class defines all the needed functions to calculate and draw the neural networks of the agents """

	def __init__(self):
		pass

	def get_node_positions(self, height_neural_net_rect, width_neural_net_rect):

		# Calculate space between nodes for centering (vertical)
		total_node_height = 0
		for _ in LAYERS:
			total_node_height += NODES_RADIUS * 2
		total_spacing_height = height_neural_net_rect - total_node_height
		vertical_spacing = total_spacing_height / (sum(LAYERS) - len(LAYERS) + 1)

		# Calculate the positions of the layers for centering (horizontal)
		layer_positions = []
		for i in range(len(LAYERS)):
			position = width_neural_net_rect * (i + 1) / (len(LAYERS) + 1)
			layer_positions.append(position)

		return vertical_spacing, layer_positions
		
	def draw_nodes(self, x_neural_net_rect, y_neural_net_rect, height_neural_net_rect, vertical_spacing, layer_positions):
		
		node_positions = []

		# Draw each layer and store node positions
		for layer_idx, num_nodes in enumerate(LAYERS):
			layer_x = x_neural_net_rect + layer_positions[layer_idx]
			layer_node_positions = []
			
			# Calculate the total height of the nodes and the spaces for this layer
			layer_total_height = num_nodes * (NODES_RADIUS * 2) + (num_nodes - 1) * vertical_spacing
			
			# Adjust starting Y position to ensure this layer is centered vertically
			start_y = y_neural_net_rect + (height_neural_net_rect - layer_total_height) / 2
			
			for node_idx in range(num_nodes):
				node_x = int(layer_x)
				node_y = int(start_y + node_idx * (NODES_RADIUS * 2 + vertical_spacing))
				
				# Draw nodes using pygame.gfxdraw for anti-aliased circles (this makes the circle less pixelated than the default option)
				pygame.gfxdraw.filled_circle(window, node_x, node_y, NODES_RADIUS, BLACK)
				pygame.gfxdraw.aacircle(window, node_x, node_y, NODES_RADIUS, BLACK)
				
				layer_node_positions.append((node_x, node_y))
			
			node_positions.append(layer_node_positions)

		return node_positions

	def draw_weights(self, node_positions, weights):
		
		for layer_idx in range(len(node_positions) - 1):
			for start_idx, start_pos in enumerate(node_positions[layer_idx]):
				for end_idx, end_pos in enumerate(node_positions[layer_idx + 1]):
					# Determine the weight for the current connection
					weight = weights[layer_idx][start_idx][end_idx]
					
					# Choose the line color based on the weights value
					if weight >= 0:
						line_color = POSITIVE_LINE_COLOR
					else:
						line_color = NEGATIVE_LINE_COLOR

					# increase the thickness of the line based on how big the distance of the weight to 0 is
					thickness = int(1 * abs(round(weight,0)))
					
					if thickness == 0:
						# Draw the line with anti-aliasing (this makes the line less pixelated than the default option, but is only available for lines with a thickness of 1)
						pygame.draw.aaline(window, line_color, start_pos, end_pos, 1)
					else:
						pygame.draw.line(window, line_color, start_pos, end_pos, 1 + 2 * thickness)

		
	def draw(self, rect, weights):

		x_neural_net_rect, y_neural_net_rect, width_neural_net_rect, height_neural_net_rect = rect	

		# vertical_spacing, layer_positions = self.get_node_positions(height_neural_net_rect, width_neural_net_rect)
		# print(vertical_spacing, layer_positions)
		# the values calculated here are fixed for the current screen size this is why i replaced the calculation by a variable to reduce the total amount of calculations
		# if the screen size or the size of the neural networks would be changed this would need to be recalculated again

		vertical_spacing = 25.4
		layer_positions = [162.5, 325.0, 487.5]

		node_positions = self.draw_nodes(x_neural_net_rect, y_neural_net_rect, height_neural_net_rect, vertical_spacing, layer_positions)

		self.draw_weights(node_positions, weights)
			
