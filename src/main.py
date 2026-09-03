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

viz.go()
viz.mouse.setVisible(viz.OFF)
viz.clearcolor(1,0,0)

navigator = vizcam.WalkNavigate(moveScale = 20, turnScale = 0.8)
viz.cam.setHandler(navigator)
viz.MainView.setPosition(0, 1.5, 0)  # Iestata sākuma pozīciju
viz.MainView.setEuler(0, 0, 0)  # Iestata sākuma skatiena virzienu

# tekst
text = viz.addText('Cau burvi!', parent=viz.SCREEN, pos=(0.5, 0.9, 0))
text.fontSize(54)
text.color(viz.YELLOW)

# grida
floor = vizshape.addPlane(size=(PLATFORM_WIDTH, PLATFORM_LENGTH), color=(0, 1, 0))
floor.setPosition(0, 0, 0)
floor.disable(viz.LIGHTING)

# genere bumbas
for i in range(50):
	ball = vizshape.addSphere()
	position = generatePosition()
	ball.setPosition(position[0], position[1], position[2])
	





