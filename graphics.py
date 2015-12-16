import OpenGL
import time
from OpenGL.GLUT import *
from OpenGL.GL import *
import sys, math, os
from math import *

'''
Values to configure OpenGL
'''
camera_angle_x = 0

window_pos_x = 50
window_pos_y = 50
window_width = 800
window_height= 800

frustum_near = 25
frustum_far = 50
frustum_width = 40
frustum_height = frustum_width * ((window_height*1.0) / window_width)

'''
Function that sets the projection
'''
def setProjection ():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Create frustum
    glOrtho(-frustum_width,frustum_width,-frustum_height,frustum_height, frustum_near, frustum_far)

    # Center frustum
    glTranslatef(0.0,-5.0,-0.50*(frustum_far+frustum_near))

'''
Function that sets the window
'''
def setViewport ():
	glViewport(0,0,window_width, window_height)

'''
Function that sets the camera
'''
def setCamera ():
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glRotatef(camera_angle_x,1.0,0,0)

'''
Function that draws a sphere at @pos, with radius @radius
'''
def drawSphere(pos,radius, r, g, b):
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    glPushMatrix()
    glLoadIdentity()
    print('radius: '+str(radius))
    print('RGB: '+ str(r)+' '+ str(g) + ' ' + str(b))
    glColor3f(r/255.0,g/255.0,b/255.0)
    glTranslatef(pos[0],pos[1],0)
    glutSolidSphere(radius,8,8)

    glPopMatrix()

'''
Function that draws a line from @start_pos to @end_pos
'''
def drawLine(start_pos, end_pos):
	glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
	glColor3f(1.0,1.0,1.0)

	glBegin(GL_LINES)
	glVertex3f( start_pos[0], start_pos[1], start_pos[2] )
	glVertex3f( end_pos[0], end_pos[1], end_pos[2] )
	glEnd()

'''
Function that draws the scene
'''
def draw(planets, active_planets, t):
    glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT) #Clean the frame

    setViewport()
    setProjection()
    setCamera()

    for i, planet in enumerate(planets):
        if active_planets[i].get():
            drawSphere(planet.position(t),planet.radius, planet.r, planet.g, planet.b)

    glutSwapBuffers() #Change this frame and the old frame

'''
Function to recognize the letter 'q' as exit
'''
def keyboardFunc(key, x_mouse, y_mouse):
	if key == 'q' or key == 'Q':
		sys.exit(0)

'''
Function that sets window and OpenGL loop
'''
def initGlut(arguments):

	glutInit(arguments)
	glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )

	glutInitWindowPosition( window_pos_x, window_pos_y )
	glutInitWindowSize( window_width, window_height )

	glutCreateWindow("Solar System")

	glutKeyboardFunc( keyboardFunc )
	glutDisplayFunc(draw)
	glutIdleFunc(draw)

'''
Function that sets graphics configurations
'''
def initOpenGL():
	glEnable( GL_DEPTH_TEST ) #Needed to use 3D graphics

	glClearColor(0.0,0.1,0.1,1.0)

	glLineWidth( 8.0 )
	glPointSize( 2.0 )

	glPolygonMode ( GL_FRONT_AND_BACK, GL_LINE)

	setViewport()
	setProjection()
	setCamera()
