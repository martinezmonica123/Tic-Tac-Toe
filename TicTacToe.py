#######################################################################

#	1. Overview: 
#	     This TicTacToe implementation keeps a record of all the moves made by both  
#	     computer and the human players. By doing so the computer is able to block winning moves 
#        and make its own winning moves whenever possible. When not possible moves are made based on
#        slots more likely to generate winning sequences. (Mainly center, corner, then edge locations.)
#   2. Specifications: 
#        This program should:
#		  - allow for a human player
#		  - play against a computer player
#		  - have some user interface 
#		  - never lose and win whenever possible
#	3. Design: 
#        The program is separated into 3 different classes: Player, Board, and TicTacToe; Text-based UI.
#	4. To run: 
#        $ python tictactoe.py
#
#	
#######################################################################
#######################################################################

import random

class Player():
	
	'''
		Tracks of token and movement data.
	'''
	
	def __init__(self, token=None):
		self.token      = token
		self.curr_move  = ''
		self.past_moves = { '1': False, '2': False, '3': False, 
						    '4': False, '5': False, '6': False,
							'7': False, '8': False, '9': False  }	

###########################################################

class Board():
	
	'''
		3x3 matrix representation of a tic-tac-toe board.
		Contains data on winning sequences and specific board location groupings.
	'''
	
	def __init__(self):
		self.board       = [['1','2','3'],['4','5','6'],['7','8','9']]
		self.edges       = ['2','4','6','8']
		self.corners     = ['1','3','7','9']	
		self.center      = ['5']

		self.win_combinations = [['1','4','7'], ['2','5','8'], ['3','6','9'], 
								 ['1','2','3'], ['4','5','6'], ['7','8','9'], 
								 ['1','5','9'], ['3','5','7']]

	def print_board(self):	
		'''
			Pretty prints TicTacToe board.
		'''
		line = '	| '
		print('	-------------')
		for row in self.board:	
			for item in row:
				line += str(item) + ' | '
			print(line)
			print('	-------------')
			line = '	| '
		print('\n')

	def update_board(self, move, token):
		'''
			Takes a player token and board index and updates the TicTacToe Game board accordingly.
		'''
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == move:
					self.board[i][j] = token
		self.print_board()

	def is_available(self, move):
		'''
			Takes a board index (player move) and determines whether the position is available. 
				If it is it updates the board and marks the locations as unavailable.
		'''
		if move in self.center:
			index = self.center.index(move)
			del self.center[index]
			return True
		
		elif move in self.edges:
			index = self.edges.index(move)
			del self.edges[index]
			return True
		
		elif move in self.corners:
			index = self.corners.index(move)
			del self.corners[index]
			return True
		return False

###########################################################

class TicTacToe():
	
	'''
		TicTacToe representation contains game specific data and 
			implements the previous Player and Board classes.
	'''
	
	def __init__(self):
		self.over     = False
		self.winner   = 'None'
		self.full     = False
		self.first    = ''
		
		self.board    = Board()
		self.user     = Player()
		self.computer = Player()

	def set_game_tokens(self):
		'''
			Takes user input and sets the character-token for each player accordingly.
		'''
		valid_token = False
		while not valid_token:
			user_token = raw_input("   Choose your token: 'x' or 'o'? ")
			if user_token == 'x' or user_token == 'o':
				valid_token = True
			else:
				print("	Not a valid token.")

		if user_token == 'x':
			comp_token  = 'o'
		else: 
			comp_token = 'x'

		print ('\n	Your token: %s ' % (user_token))
		print ("	The computer's token: %s \n" % (comp_token))

		game.user.token = user_token
		game.computer.token = comp_token

	def who_goes_first(self):
		'''
			Determines which player goes first. Increases the chances of the computer going first.
		'''
		self.first  = random.choice([self.computer.token, self.user.token, self.computer.token])
		print ('%s goes first. \n' % (self.first))	
	
	def game_status(self):
		'''
			Determines whether the current game state has a winning sequence or has a full game board.
			Sets the game attriubutes accordingly.
		'''
		if self.user.token and self.computer.token:
			if self.row_win(self.computer.token) or self.col_win(self.computer.token) or self.diag_win(self.computer.token):
				self.over = True
				self.winner = 'Computer'
			
			elif self.row_win(self.user.token) or self.col_win(self.user.token) or self.diag_win(self.user.token):
				self.over = True
				self.winner = 'User'
			
			elif self.is_full():
				self.full = True
				self.over = True
				self.winner = 'Tie'
	
	def results(self):
		'''
			Outputs the results of a finished game.
		'''
		if self.winner == 'Tie':
			print ("\n 	It's a Tie. ")
		else:
			print ('\n 	%s Wins!!! \n\n' % (self.winner))

### Game_Status: Helper Functions
	def row_win(self, token):		
		'''
			Helper Function: Determines whether the game board contains a row win.
		'''
		winner = [token]*3
		for row in self.board.board:
			if row == winner:
				return True
		return False

	def col_win(self, token):
		'''
			Helper Function: Determines whether the game board contains a column win.
		'''
		length = len(self.board.board)
		
		for col in range(length):
			if all([self.board.board[row][col] == token for row in range(length)]):
				return True
		return False

	def diag_win(self, token):
		'''
			Helper Function: Determines whether the game board contains a diagonal win.
		'''	
		if self.board.board[0][0] == token and self.board.board[1][1] == token and self.board.board[2][2] == token:
			return True
		if self.board.board[0][2] == token and self.board.board[1][1] == token and self.board.board[2][0] == token:
			return True
		return False

	def is_full(self):
		'''
			Helper Function: Determines whether the game board is full -- tie.
		'''
		if not self.board.corners and not self.board.center and not self.board.edges:
			self.full = True
			return True
		self.full = False
		return False
	
### TTT Moves
	def user_move(self):
		'''
			Validates and updates the game board for user moves.
		'''		
		valid_move = False
		
		while not valid_move:

			move = raw_input("Chose a number on the board: ")
			
			if move in self.board.center or \
			   move in self.board.corners or \
			   move in self.board.edges:
				valid_move = True
			else:
				print("Not a valid move.")
		
		if move in self.board.center:
			temp = self.board.center.index(move)
			del self.board.center[temp]
		
		elif move in self.board.edges:
			temp = self.board.edges.index(move)
			del self.board.edges[temp]
		
		elif move in self.board.corners:
			temp = self.board.corners.index(move)
			del self.board.corners[temp]

		self.user.past_moves[move] = True
		self.user.curr_move = move
		
		self.board.update_board(move, self.user.token)
		
		return move

	def optimized_computer_move(self):

		'''
			Computer Player specific movement function.
				Determines whether there is a winning sequence for the computer player in the current game state.
				If not then determines whether there is a blockable winning sequence.
				If not then makes a random move.
		'''
			
		can_win, move = self.check_if_can_win()
		
		if can_win:
			print('Computer chooses: %s' % (move))
			self.board.update_board(move, self.computer.token)
			return move
		else:
			can_block, move = self.check_if_can_block()
			if can_block:
				print('Computer chooses: %s' % (move))
				self.board.update_board(move, self.computer.token)
				return move
			else:
				self.random_move()

### Computer_Move:  Helper Functions
	def random_move(self):
		'''
			Computer movement function. Generates a seemingly random movement. 
				Function determines whether there are free moves in the center, the corner cases, 
				and then finally the edge cases. The function follows this specific sequence in 
				order to increase the chances of producing a winning sequence for the computer.
		'''
		if self.user.curr_move:
			user_move = int(self.user.curr_move)
		else:
			user_move = self.user.curr_move
		comp_move = None

		if user_move == 5 : # center
			if self.board.corners:
				comp_move = self.board.corners[0]
				del self.board.corners[0]
			elif self.board.edges:
				comp_move = self.board.edges[0]
				del self.board.edges[0]
		else:
			if self.board.center:
				comp_move = '5'
				temp = self.board.center.index('5')
				del self.board.center[temp]
			elif self.board.corners:
				comp_move = self.board.corners[0]
				del self.board.corners[0]
			elif self.board.edges:
				comp_move = self.board.edges[0]
				del self.board.edges[0]

		self.computer.past_moves[comp_move] = True
		self.computer.curr_move = comp_move
		
		print('Computer chooses: %s' % (comp_move))
		self.board.update_board(comp_move, self.computer.token)
		
		return comp_move

	def check_if_can_win(self):
		'''
			Determine whether the computer can make a winning move based on the computer player's 
				past moves dictionary.
		'''
		for a,b,c in self.board.win_combinations:
			if self.computer.past_moves[a] == True and self.computer.past_moves[b] == True:
				if self.board.is_available(c):
					self.computer.past_moves[c] = True
					return (True, c)
			
			elif self.computer.past_moves[a] == True and self.computer.past_moves[c] == True:
				if self.board.is_available(b):
					self.computer.past_moves[b] = True
					return (True, b)
			
			elif self.computer.past_moves[b] == True and self.computer.past_moves[c] == True:
				if self.board.is_available(a):
					self.computer.past_moves[a] = True
					return (True, a)
		return (False, None)

	def check_if_can_block(self):
		'''
			Determine whether the computer can block a winning move based on the human player's
				past moves dictionary.
		'''
		for a,b,c in self.board.win_combinations:
			if self.user.past_moves[a] == True and self.user.past_moves[b] == True:
				if self.board.is_available(c):
					self.user.past_moves[c] = True
					return (True, c)
			
			elif self.user.past_moves[a] == True and self.user.past_moves[c] == True:
				if self.board.is_available(b):
					self.user.past_moves[b] = True
					return (True, b)
			
			elif self.user.past_moves[b] == True and self.user.past_moves[c] == True:
				if self.board.is_available(a):
					self.user.past_moves[a] = True
					return (True, a)
		return (False, None)


###########################################################
###########################################################

if __name__ == "__main__":

	''' 
	Overview of Game Play: 
	
 		1. generate board 
 		2. choose and set player tokens
 		3. determine who goes first
 		4. while there is no win/lose/tie
 		5. make move (comp or user)
 			a. validate move
 		6. update board
 		7. other player make move
 			a. validate move
 		8. check if win/lose/tie
 		9. if not 8 then go to 4 else 
 	   10. show results
	
	'''

	print ("Let's play Tic Tac Toe! \n")

	game = TicTacToe()

	game.board.print_board()

	game.set_game_tokens()
	game.who_goes_first()

	while not (game.over and game.full):
		if game.first == game.user.token:		
			game.user.curr_move = game.user_move()
			
			game.game_status()
			game.is_full()

			if game.full or game.over:
				game.game_status()
				break

			game.optimized_computer_move()
			game.game_status()
			game.is_full()
			
		else:
			game.optimized_computer_move()
			
			game.game_status()
			game.is_full()
			
			if game.full or game.over:
				game.game_status()
				break
				
			game.user_move()	
			game.game_status()
			game.is_full()

	game.results()

