from copy import deepcopy
import time

class eight_puzzle():

	def __init__(self, level=0, mov = "S"): #'S' for start, 'L' for left, 'D' for down etc
		""" 
		Initialization function for eight_puzzle nodes
		"""
		self.data = [[0,0,0],[0,0,0],[0,0,0]]
		self.goal = [[0,0,0],[0,0,0],[0,0,0]]
		self.mov = mov
		self.level = level
		self.gval = 0 #gn
		self.fval = None	# gn + hn
		self.blankPos = None

	def __eq__(self,other):
		""" 
		Function to check if this puzzle's state equals another
		"""

		if other == None:
			return False

		if isinstance(other,eight_puzzle) !=True:
			raise TypeError
		for i in range(3):
			for j in range(3):
				if self.data[i][j] != other.data[i][j]:
					return False
		
		return True

	def fill_input(self,nums_list):
		"""
		Function to initialize start and goal states for node
		For this assignment, first 9 numbers in list are the #s in the initial state
		And, the remainder 9 are #s in the goal state
		"""
		count = 0
		for i in range(3):
			for j in range(3):
				self.data[i][j]= int(nums_list[count])
				self.goal[i][j] = int(nums_list[count+9])
				count+=1

	def puzzle_print(self):
		"""
		Function to print this puzzle's state
		"""
		for i in range(3):
			x = ""
			for j in range(3):
				x += str(self.data[i][j])+" "
			print(x)
		print('')
	
	def calc_mann_dist(self):
		"""
		Function to calculate manhattan distance of tiles from their goal pos
		"""
		mann_distance= 0
		for i in range(3):
			for j in range(3):
				if self.data[i][j] != self.goal[i][j] and self.data[i][j]!= 0:
					for k in range(3):
						for l in range(3):
							if self.data[i][j]== self.goal[k][l]:
								mann_distance += abs(i-k)
								mann_distance+= abs(j-l)
		return mann_distance # subtracting the blank space from the calculation, i.e 0

	def calc_NSS(self):
		"""
		Function to calculate Nilson's Sequence Score
		"""
		pn = self.calc_mann_dist()
		sn = 0

		if self.data[1][1]!= self.goal[1][1]: # Middle tiles check
			sn+=1
		edges = [[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0],[0,0]]
		for ind,i in enumerate(edges): 
			x = self.data[i[0]][i[1]]
			if ind ==8: # if 2nd row first column (right before start pos, i.e, 1st row 1st column)
				y= self.data[0][0]
			else:
				y = self.data[edges[ind+1][0]][edges[ind+1][1]]
			if x!= self.goal[1][1]: # middle tile's already taken care of
				y1 = 0
				for ind2,j in enumerate(edges):
					if self.goal[j[0]][j[1]] == x:
						if ind2 == 8: # last item (i.e before top left corner)
							y1 = self.goal[0][0]
						else:
							y1 = self.goal[edges[ind2+1][0]][edges[ind2+1][1]]
				if y1!=y:
					sn+=2
		return pn+(3*(sn-2)) # subtracting blank tile
	
	def calc_fval(self,hn):
		if hn =="Mannhatan Distance":
			self.fval = self.gval + self.calc_mann_dist() # fn = gn + hn
		else: 
			self.fval = self.gval + self.calc_NSS()

	def calc_avail_moves(self):
		"""
		Function to find current blank position
		And to find valid moves for the current blank position
		"""
		move_lst= []
		for i in range(3): # 0, 1, 2
			for j in range(3):
				if self.data[i][j] == 0:
					self.blankPos = [i,j]
					if (i-1) !=-1: # checking if up is a valid move
						move_lst.append(['U', i-1,j])
					if (j-1) !=-1: # checking if left is a valid move
						move_lst.append(['L',i,j-1])
					if (i+1)!= 3: # checking if down is a valid move
						move_lst.append(['D', i+1, j])
					if (j+1)!= 3: # checking if right is a valid move
						move_lst.append(['R', i, j+1])
		return move_lst

	def move(self, i, j, k): # i = row, j = column, k = 'L', 'R', 'U', or 'D'
		"""
		Function to move the blank tile up, down, left or right.
		It is assumed this function won't be called unless it is a valid move
		Returns a new state(edge_puzzle node) rather than changing the current.
		"""
		new_node = deepcopy(self)
		new_node.mov = k
		new_node.level = self.level+1

		# first swap
		x = new_node.data[i][j]
		y= new_node.data[self.blankPos[0]][self.blankPos[1]]
		new_node.data[i][j] = y
		new_node.data[self.blankPos[0]][self.blankPos[1]] = x
		new_node.blankPos = [i,j]

		# then return node to function that called 'move' which will fill in the tree attributes
		return new_node
	
class A_Star_8_Puzzle:

	def __init__(self, start, hn): # eight_puzzle node, 'Mannhatan Distance' or 'Neilson' or whatever. If its not 'Mannhatan Distance' it will do Nilson
		"""
		It is assumed that this function is only initialized with
		eight_puzzle nodes as 'start' and 'goal'
		"""

		self.start = start
		self.nodes_gen = 1
		self.hn = hn
		self.open = {}
		self.closed = {}
		self.solMoves = [] # solution moves
		self. solFvals = [] # solution fvals


	def calc_children(self, node, hn): 
		"""
		Step 4: Function to expand node / generate child nodes
		"""
		# 1. Move n to closed list
		moves = node.calc_avail_moves()
		self.closed[id(node)] = node.fval,node
		del self.open[id(node)]

		# 2. Generate all child nodes and move them to open list
		for i in moves:
			new_node = node.move(i[1],i[2],i[0])
			new_node.calc_fval(hn)

			# 3. Check if new node is in open or closed list
			check_pass = True
			for nodes in self.open:
				if id(new_node) == nodes:
					check_pass = False
			for nodes in self.closed.values():
				if id(new_node) == nodes:
					check_pass = False

			# 4. if not in either copen or closed, 
			if check_pass: 
				self.open[id(new_node)] = new_node.fval, new_node
				self.nodes_gen+=1 # increment # of nodes genrated (i.e new nodes in graph search tree)
	
	def initialize_openList(self): # only called for root node (Move out of class?)
		"""
		Step 1: Place starting node in open list
		"""
		self.start.calc_fval(self.hn)
		self.open[id(self.start)] = self.start.fval, self.start
	
	def start_up(self):
		""" 
		Step 2:	Check if the open list is empty or not,
				if empty return failure
		"""
		if len(self.open) == 0:
			return "FAILURE"
		
		"""
		Step 3: Select the node from the open list which has the smallest
				fn value(fval). If this is the goal node return success
		"""
		lowest_fn = None
		lowest_fn_node = None
		for key in self.open:
			if lowest_fn == None:
				lowest_fn = self.open[key][0]
				lowest_fn_node = self.open[key][1]
			
			if self.open[key][0]< lowest_fn:
				lowest_fn = self.open[key][0]
				lowest_fn_node = self.open[key][1]
		self.solMoves.append(lowest_fn_node.mov)
		self.solFvals.append(lowest_fn)
		#del
		time.sleep(5)
		print('curr lowest:')
		lowest_fn_node.puzzle_print()
		print(self.solMoves)
		print(self.solFvals)
		# up to here
		if lowest_fn_node.data == self.start.goal:
			return "SUCCESS", lowest_fn_node
		
		"""
		Step 4: If goal node not found in step 3, expand the node
		"""

		self.calc_children(lowest_fn_node, self.hn)
		return "ONGOING"

	def play_game(self):
		self.initialize_openList()
		solved = False
		failed = False
		x = []
		while not solved or failed:
			x= self.start_up()
			if x[0]=="SUCCESS":
				solved = True
			if x[0]=="FAILURE":
				failed = True
				print("FAILURE")

		if solved:
			self.start.puzzle_print()
			x[1].puzzle_print()
			print(x[1].level)
			print(self.nodes_gen)
			print(' '.join(map(str,self.solMoves[1:])))
			print(' '.join(map(str,self.solFvals)))
			

def main():
	""" 
	Welcome to 8 Puzzle Game, input a file with 2 puzzle states
	(start and goal) and thus 7 lines
	"""		

	"""
	Running 4 puzzle simulations below
	"""
	start_node = eight_puzzle()
	start_node1 = eight_puzzle()
	start_node2 = eight_puzzle()
	start_node3 = eight_puzzle()

	# input = open('input.txt') # sample output provided on brightspace
	input1 = open('input1.txt') # input 1 provided for project
	input2 = open ('input2.txt') # input 2 provided for project
	input3 = open('input3.txt') # input 3 provided for project

	# nums = input.read().split()
	nums1 = input1.read().split()
	nums2 = input2.read().split()
	nums3 = input3.read().split()

	# input.close()
	input1.close()
	input2.close()
	input3.close()

	# start_node.fill_input(nums)
	start_node1.fill_input(nums1)
	start_node2.fill_input(nums2)
	start_node3.fill_input(nums3)

	""" For below, change 1st arg to any of start nodes above
		Change 2nd arg to 'Mannhatan Distance' or anything else for Nilson
	"""
	puzzle = A_Star_8_Puzzle(start_node2,"Mannhatan Distance") #change 1st parameter with any of start nodes above
	puzzle.play_game()