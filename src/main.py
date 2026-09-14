from random import randint
from colorsys import hsv_to_rgb
from math import sin, sqrt, floor

# viz lietas
import viz
import vizshape
import vizcam

PLATFORM_WIDTH = 100
PLATFORM_LENGTH = 100
GAME_TIME = 15 #in seconds
PLAYER_SPEED = 7

ui = [] # teksts uz ekrana

def deleteText():
	for text in ui:
		text.remove()
	ui.clear()
		
# si klase saka aiziet un stop, kas tagad notie
class GameState:
	def __init__(self):
		viz.fov(90)
		viz.go()
		viz.clearcolor(1,0,0)
		viz.mouse.setVisible(viz.OFF)
		viz.callback(viz.KEYDOWN_EVENT, self.handleInput)
		
		self.state = ""
		self.changeState("GAME")
		
	def changeState(self, newState):
		self.state = newState
		if self.state == "START_MENU":
			self.startMenu()
		elif self.state == "GAME":
			# izdzes speles laukumu pirms renderet jauno
			for child in viz.MainScene.getChildren():
				child.remove()
			deleteText()
			self.game = Game(lambda: self.changeState("END"))
			self.game.startGame()
		elif self.state == "END":
			self.endMenu()
		
	def handleInput(self, key):
		if key == viz.KEY_RETURN and (self.state == "START_MENU" or self.state == "END"):
			self.changeState("GAME")
			
		elif self.state == "GAME":
			self.game.handleInput(key)
		
	def startMenu(self):
		title = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.5, 0.9, 0), fontSize=50)
		title.alignment(viz.ALIGN_CENTER_CENTER)

		press = viz.addText('spied ENTER lai turpinatu', parent=viz.SCREEN, pos=(0.5, 0.5, 0), fontSize=50)
		press.alignment(viz.ALIGN_CENTER_CENTER)
		
		ui.extend([title, press])
	
	def endMenu(self):
		end = viz.addText("The game has concluded \n press enter on your keyboard to play again", parent=viz.SCREEN, pos=(0.5, 0.5, 0))
		end.alignment(viz.ALIGN_CENTER_CENTER)
		end.fontSize(54)
		end.color(0, 0, 0)
		
		ui.append(end)

# Note to self - JAPARLIEK GEIM LOOPS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111111!!!!
# jaizbeids ir:
# game loops
# taimeri
class Game:
	def __init__(self, onGameEnd):
		self.onGameEnd = onGameEnd
		
		self.backgroundHue = 0.001
		self.score = 0
		self.timeLeft = GAME_TIME
		
		self.balls = []
		self.player = Player()
	
	def handleInput(self, key):
		if key == 'c':
			self.player.crouch()
	
	def startGame(self):
		# grida
		floor = vizshape.addPlane(size=(PLATFORM_WIDTH, PLATFORM_LENGTH), color=(0, 1, 0))
		floor.setPosition(0, 0, 0)
		
		# Pievieno virziena gaismu, AKA saule
		dir_light = viz.addDirectionalLight(euler=(0, 90, 0))
		dir_light.intensity(1.0)
		
		# game UI
		cau = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.75, 0.9, 0))
		cau.alignment(viz.ALIGN_CENTER_CENTER)
		cau.fontSize(54)
		cau.color(viz.YELLOW)
		
		self.punkti = viz.addText('make the money: 0', parent=viz.SCREEN, pos=(0.25, 0.9, 0))
		self.punkti.alignment(viz.ALIGN_CENTER_CENTER)
		self.punkti.fontSize(54)
		self.punkti.color(viz.YELLOW)
		
		self.laiks = viz.addText(f"time left: {self.timeLeft}", parent=viz.SCREEN, pos=(0.6, 0.7, 0))
		self.laiks.alignment(viz.ALIGN_CENTER_CENTER)
		self.laiks.fontSize(54)
		self.laiks.color(viz.YELLOW)
		
		ui.extend([cau, self.punkti, self.laiks])

		for i in range(100):
			ball = Ball()
			self.balls.append(ball)
			
		# the callback functions responsible for game looping
		self.timer = vizact.ontimer(1, self.updateTime) # speles taimeris
		self.gameLoop = vizact.onupdate(0, self.runGame)
		
	def updateTime(self):
		self.timeLeft -= 1
		self.laiks.message(f"time left: {floor(self.timeLeft)}")
		
	def checkCollision(self):
		playerPos = viz.MainView.getPosition()
		for ball in reversed(self.balls):
			dx = playerPos[0] - ball.position[0]
			dy = playerPos[1] - ball.position[1]
			dz = playerPos[2] - ball.position[2]
			
			distance = sqrt(dx**2 + dy**2 + dz**2)
			if distance <= 2: # colision is yes
				self.score += 1
				ball.deleteShape()
				self.balls.remove(ball)
				self.timeLeft += 0.25
				self.punkti.message(f"make the money: {self.score}")

	def runGame(self):
		self.checkCollision()
		viz.clearcolor(hsv_to_rgb(self.backgroundHue,1,1))
		self.backgroundHue += 0.002
		for ball in self.balls:
			ball.changeColor()
			ball.makeItBounce()

		if self.timeLeft <= 0:
			self.endGame()
			
	def endGame(self):
		self.gameLoop.setEnabled(False)
		self.timer.setEnabled(False)
		viz.cam.setHandler(None)
		
		self.onGameEnd()
	
class Player:
	def __init__(self):
		self.navigator = vizcam.WalkNavigate(moveScale = PLAYER_SPEED, turnScale = 0.5)
		viz.cam.setHandler(self.navigator)
		viz.MainView.collision(True)
		viz.MainView.setPosition(0, 30, 0)
		viz.MainView.setEuler(0, 0, 0)
		#viz.MainView.eyeheight(30)
		self.crouched = False
		
	def crouch(self):
		print("crouch")
		if self.crouched:
			viz.MainView.eyeheight(1.82)
			#self.navigator = vizcam.WalkNavigate(moveScale = PLAYER_SPEED, turnScale = 0.5)
			self.crouched = False
		else:
			viz.MainView.eyeheight(0.1)
			#self.navigator = vizcam.WalkNavigate(moveScale = PLAYER_SPEED - 6, turnScale = 0.5)
			self.crouched = True
	
class Ball:
	def __init__(self):
		self.position = self.generatePosition()
		self.hue = 0.5
		
		# the interface used to change the physical shape properties
		self.shape = vizshape.addSphere()
		self.shape.setPosition(self.position[0], self.position[1], self.position[2])
		
	def changeColor(self):
		self.hue += 0.002
		self.shape.color(hsv_to_rgb(self.hue, 1, 1))

	def makeItBounce(self):
		self.shape.setPosition(self.position[0], self.position[1] + abs(sin(viz.tick() * 7)), self.position[2])
		
	@staticmethod
	def generatePosition():
		x = randint(-PLATFORM_WIDTH, PLATFORM_WIDTH)/2
		y = randint(1, 3)
		z = randint(-PLATFORM_LENGTH, PLATFORM_LENGTH)/2
		return [x, y, z]
		
	def deleteShape(self):
		self.shape.remove()

if __name__ == "__main__":
	game = GameState()