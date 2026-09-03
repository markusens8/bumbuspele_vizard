from random import randint

# viz lietas
import viz
import vizshape
import vizcam

PLATFORM_WIDTH = 50
PLATFORM_LENGTH = 50

def generatePosition():
	x = randint(-PLATFORM_WIDTH, PLATFORM_WIDTH)/2
	y = randint(1, 10)
	z = randint(-PLATFORM_LENGTH, PLATFORM_LENGTH)/2
	return [x, y, z]

def startMenu():
	title = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.5, 0.9, 0), fontSize=50)
	title.alignment(viz.ALIGN_CENTER_CENTER)

	press = viz.addText('spied ENTER lai turpinātu!', parent=viz.SCREEN, pos=(0.5, 0.5, 0), fontSize=50)
	press.alignment(viz.ALIGN_CENTER_CENTER)

def gameLoop():
	navigator = vizcam.WalkNavigate(moveScale = 30, turnScale = 0.8)
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
	for i in range(100):
		ball = vizshape.addSphere()
		position = generatePosition()
		ball.setPosition(position[0], position[1], position[2])
		balls.append(ball)


if __name__ == "__main__":
	viz.go()
	viz.clearcolor(1,0,0)
	viz.mouse.setVisible(viz.OFF)
	#startMenu()
	gameLoop()




