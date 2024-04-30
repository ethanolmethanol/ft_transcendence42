ENABLED=0
DISABLED=1
GIVEN_UP = 2

class Player:
	def __init__(self, owner_name, username):
		self.owner_name = owner_name
		self.username = username
		self.score = 0
		self.status = ENABLED

	def reset(self):
		self.score = 0
