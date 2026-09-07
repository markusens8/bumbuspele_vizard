from random import randint
from colorsys import hsv_to_rgb

# viz lietas
import viz
import vizshape
import vizcam

PLATFORM_WIDTH = 100
PLATFORM_LENGTH = 100

# jabut funkcionalitatei lai izdestu visus izveidotos elementus uz ekrana
# 

def generatePosition():
	x = randint(-PLATFORM_WIDTH, PLATFORM_WIDTH)/2
	y = randint(1, 10)
	z = randint(-PLATFORM_LENGTH, PLATFORM_LENGTH)/2
	return [x, y, z]
	
class gameState:
	def __init__(self):
		viz.fov(90)
		viz.fullscreen = 1
		viz.go()
		viz.clearcolor(1,0,0)
		viz.mouse.setVisible(viz.OFF)
		viz.callback(viz.KEYDOWN_EVENT, self.handleInput)
		
		self.state = "MENU"
		self.hue = 0.001
		self.score = 0
		self.timeLeft = 0
		
		self.startMenu()
		
	def changeState(self, newState):
		# remove everything before loading in new stuff
		for child in viz.MainScene.getChildren():
			child.remove()
		
		self.state = newState
		if self.state == "MENU":
			self.startMenu()
		elif self.state == "GAME":
			self.startGame()
			vizact.onupdate(0, self.runGame)
		
	def handleInput(self, key):
		if key == viz.KEY_RETURN and self.state == "MENU":
			self.changeState("GAME")
		
	def startMenu(self):
		title = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.5, 0.9, 0), fontSize=50)
		title.alignment(viz.ALIGN_CENTER_CENTER)

		press = viz.addText('spied ENTER lai turpinātu!', parent=viz.SCREEN, pos=(0.5, 0.5, 0), fontSize=50)
		press.alignment(viz.ALIGN_CENTER_CENTER)
	
	def startGame(self):
		navigator = vizcam.WalkNavigate(moveScale = 30, turnScale = 0.5)
		viz.cam.setHandler(navigator)
		viz.MainView.collision(viz.ON)
		viz.MainView.setPosition(0, 100, 0)  # Iestata sākuma pozīciju
		viz.MainView.setEuler(0, 0, 0)  # Iestata sākuma skatiena virzienu

		# tekst
		cau = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.75, 0.9, 0))
		cau.alignment(viz.ALIGN_CENTER_CENTER)
		cau.fontSize(54)
		cau.color(viz.YELLOW)
		
		punkti = viz.addText('punkti: ', parent=viz.SCREEN, pos=(0.25, 0.9, 0))
		punkti.alignment(viz.ALIGN_CENTER_CENTER)
		punkti.fontSize(54)
		punkti.color(viz.YELLOW)

		# Pievieno virziena gaismu, AKA saule
		dir_light = viz.addDirectionalLight(euler=(0, 90, 0))
		dir_light.intensity(1.0)

		# grida
		floor = vizshape.addPlane(size=(PLATFORM_WIDTH, PLATFORM_LENGTH), color=(0, 1, 0))
		floor.setPosition(0, 0, 0)

		# genere bumbas
		balls = []
		for i in range(500):
			ball = vizshape.addSphere()
			position = generatePosition()
			ball.setPosition(position[0], position[1], position[2])
			balls.append(ball)
			
	def runGame(self):
		viz.clearcolor(hsv_to_rgb(self.hue,1,1))
		self.hue += 0.01	

if __name__ == "__main__":
	game = gameState()