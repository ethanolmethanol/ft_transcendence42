ENABLED=0
DISABLED=1

class Player:
	def __init__(self, username):
		self.username = username
		self.score = 0
		self.status = ENABLED
