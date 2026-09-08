from random import randint
from colorsys import hsv_to_rgb

# viz lietas
import viz
import vizshape
import vizcam

PLATFORM_WIDTH = 100
PLATFORM_LENGTH = 100
GAME_TIME = 5 #in seconds

def generatePosition():
	x = randint(-PLATFORM_WIDTH, PLATFORM_WIDTH)/2
	y = randint(1, 10)
	z = randint(-PLATFORM_LENGTH, PLATFORM_LENGTH)/2
	return [x, y, z]

# si klase saka aiziet un stop, kas tagad notie
class GameState:
	def __init__(self):
		viz.fov(90)
		viz.fullscreen = 1
		viz.go()
		viz.clearcolor(1,0,0)
		viz.mouse.setVisible(viz.OFF)
		viz.callback(viz.KEYDOWN_EVENT, self.handleInput)
		
		self.state = ""
		
		
		self.changeState("GAME")
		
	def changeState(self, newState):
		self.state = newState
		if self.state == "MENU":
			self.startMenu()
		elif self.state == "GAME":
			self.game = Game(lambda: self.changeState("END"))
		elif self.state == "END":
			endMenu()
		
	def handleInput(self, key):
		if key == viz.KEY_RETURN and self.state == "MENU":
			self.changeState("GAME")
			
		if key == viz.KEY_F1 and self.state == "GAME":
			viz.MainView.setPosition(0, 30, 0)
		
	def startMenu(self):
		title = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.5, 0.9, 0), fontSize=50)
		title.alignment(viz.ALIGN_CENTER_CENTER)

		press = viz.addText('spied ENTER lai turpinātu', parent=viz.SCREEN, pos=(0.5, 0.5, 0), fontSize=50)
		press.alignment(viz.ALIGN_CENTER_CENTER)
	
	def endMenu(self):
		return

# Note to self - JAPARLIEK GEIM LOOPS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111111!!!!
# jaizbeids ir:
# game loops
# taimeri
class Game:
	def __init__(self, onGameEnd):
		self.onGameEnd = onGameEnd
		self.hue = 0.001
		self.score = 0
		self.timeLeft = GAME_TIME
		self.balls = []
		
	def startGame(self):
		navigator = vizcam.WalkNavigate(moveScale = 30, turnScale = 0.5)
		viz.cam.setHandler(navigator)
		viz.MainView.collision(True)
		viz.MainView.setPosition(0, 30, 0)  # Iestata sākuma pozīciju
		viz.MainView.setEuler(0, 0, 0)  # Iestata sākuma skatiena virzienu

		# game UI
		cau = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.75, 0.9, 0))
		cau.alignment(viz.ALIGN_CENTER_CENTER)
		cau.fontSize(54)
		cau.color(viz.YELLOW)
		
		self.punkti = viz.addText('make the money: 0', parent=viz.SCREEN, pos=(0.25, 0.9, 0))
		self.punkti.alignment(viz.ALIGN_CENTER_CENTER)
		self.punkti.fontSize(54)
		self.punkti.color(viz.YELLOW)
		
		self.laiks = viz.addText("time left: 5", parent=viz.SCREEN, pos=(0.6, 0.7, 0))
		self.laiks.alignment(viz.ALIGN_CENTER_CENTER)
		self.laiks.fontSize(54)
		self.laiks.color(viz.YELLOW)

		# Pievieno virziena gaismu, AKA saule
		dir_light = viz.addDirectionalLight(euler=(0, 90, 0))
		dir_light.intensity(1.0)

		# grida
		floor = vizshape.addPlane(size=(PLATFORM_WIDTH, PLATFORM_LENGTH), color=(0, 1, 0))
		floor.setPosition(0, 0, 0)

		for i in range(100):
			ball = vizshape.addSphere()
			position = generatePosition()
			ball.setPosition(position[0], position[1], position[2])
			self.balls.append(ball)
			
		# the callback functions responsible for game looping
		viz.callback(viz.COLLISION_EVENT, self.checkCollision)
		self.timer = vizact.ontimer(1, self.updateTime) # speles taimeris
		self.gameLoop = vizact.onupdate(0, self.runGame)
		
	def updateTime(self):
		self.time -= 1
		self.laiks.message(f"time left: {self.time}")
		
	def checkCollision(self, e):
		if e.object in self.balls:
			self.score += 1
			e.object.remove()
			self.balls.remove(e.object)
			self.punkti.message(f"make the money: {self.score}")
			
	def runGame(self):
		viz.clearcolor(hsv_to_rgb(self.hue,1,1))
		self.hue += 0.001
		for ball in self.balls:
			ball.color(hsv_to_rgb(self.hue+0.5,1,1))
			
		# deaktivize visus ciklus
		if self.timeLeft <= 0:
			viz.callback(viz.COLLISION_EVENT, None)
			self.gameLoop.setEnabled(False)
			self.timer.setEnabled(False)
			self.onGameEnd()

if __name__ == "__main__":
	game = GameState()
