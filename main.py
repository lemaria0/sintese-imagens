# Letícia Maria Eufrásio Reis / Maria Luiza Pereira Sousa / Maria Auxiliadora de Oliveira Chaves
# 04/08/2025
# Trabalho de Síntese de Imagens

import time
import random
from math import cos, sin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# física
ground_y = -2.5
size_cube = 2
pos_y = ground_y + size_cube / 2
vel_y = 0.0
acc_y = -9.8
rotation_speed = [0.0, 0.0, 0.0]
rotation_angle = [0.0, 0.0, 0.0]
bouncing = False
first_launch = True
result = False

# tempo
last_time = time.time()


class Ground:
    def __init__(self, y):
        self.y = y

    def draw(self):
        glColor3f(0.55, 0.27, 0.07)
        glBegin(GL_QUADS)
        glVertex3f(-10, self.y, -10)
        glVertex3f(10, self.y, -10)
        glVertex3f(10, self.y, 10)
        glVertex3f(-10, self.y, 10)
        glEnd()


class Cube:
    def __init__(self, base):
        self.base = base / 2.0

    def draw_dot(self, x, y, radius=0.1):
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 0)
        glVertex2f(x, y)
        for angle in range(0, 361, 30):
            rad = angle * 3.14159 / 180.0
            glVertex2f(x + radius * cos(rad), y + radius * sin(rad))
        glEnd()

    def draw_dice_face(self, number):
        positions = {
            1: [(0, 0)],
            2: [(-0.3, -0.3), (0.3, 0.3)],
            3: [(-0.3, -0.3), (0, 0), (0.3, 0.3)],
            4: [(-0.3, -0.3), (-0.3, 0.3), (0.3, -0.3), (0.3, 0.3)],
            5: [(-0.3, -0.3), (-0.3, 0.3), (0.3, -0.3), (0.3, 0.3), (0, 0)],
            6: [(-0.3, -0.3), (-0.3, 0), (-0.3, 0.3), (0.3, -0.3), (0.3, 0), (0.3, 0.3)],
        }

        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)
        for (x, y) in positions[number]:
            self.draw_dot(x, y)
        glDisable(GL_POLYGON_OFFSET_FILL)

    def draw(self):
        b = self.base
        faces = [
            (2, (0, -1 - 0.05, 0), (-90, 1, 0, 0)),  # baixo
            (5, (0, 1 + 0.05, 0), (-90, 1, 0, 0)),   # cima
            (1, (0, 0, 1 + 0.05), (0, 0, 0, 0)),     # frente
            (6, (0, 0, -1 - 0.05), (180, 0, 1, 0)),  # trás
            (3, (1 + 0.05, 0, 0), (90, 0, 1, 0)),    # direita
            (4, (-1 - 0.05, 0, 0), (-90, 0, 1, 0)),  # esquerda
        ]

        glColor3f(0.95, 0.95, 0.95)
        glBegin(GL_QUADS)
        for face in [
            [(-b, -b, b), (b, -b, b), (b, -b, -b), (-b, -b, -b)],
            [(-b, b, b), (b, b, b), (b, b, -b), (-b, b, -b)],
            [(-b, -b, b), (b, -b, b), (b, b, b), (-b, b, b)],
            [(-b, -b, -b), (b, -b, -b), (b, b, -b), (-b, b, -b)],
            [(b, -b, b), (b, -b, -b), (b, b, -b), (b, b, b)],
            [(-b, -b, b), (-b, -b, -b), (-b, b, -b), (-b, b, b)],
        ]:
            for v in face:
                glVertex3f(*v)
        glEnd()

        for i, (num, trans, rot) in enumerate(faces):
            glPushMatrix()
            glTranslatef(*trans)
            if rot[0] != 0:
                glRotatef(*rot)
            self.draw_dice_face(num)
            glPopMatrix()


myCube = Cube(size_cube)
ground = Ground(ground_y)

def keyboard(key, _x, _y):
    global vel_y, rotation_speed, bouncing, result, first_launch

    if key == b'\x1b':
        exit(0)
    elif key == b' ' and not bouncing:
        vel_y = 6.0
        bouncing = True
        result = False
        first_launch = False
        rotation_speed = [
            random.uniform(300, 600),
            random.uniform(300, 600),
            random.uniform(300, 600)
        ]
    glutPostRedisplay()


def init():
    glClearColor(0.1, 0.1, 0.25, 1)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    global pos_y, vel_y, rotation_angle, last_time, bouncing, result, first_launch, size_cube

    now = time.time()
    dt = now - last_time
    last_time = now

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

    ground.draw()

    glPushMatrix()
    glTranslatef(0, pos_y, 0)

    if bouncing:
        vel_y += acc_y * dt
        pos_y += vel_y * dt
        for i in range(3):
            rotation_angle[i] += rotation_speed[i] * dt

        if pos_y <= ground_y + size_cube / 2:
            pos_y = ground_y + size_cube / 2
            vel_y = -vel_y * 0.4
            for i in range(3):
                rotation_speed[i] *= 0.5
            if abs(vel_y) < 0.1 and max(rotation_speed) < 1:
                bouncing = False
                for i in range(3):
                    rotation_angle[i] = round(rotation_angle[i] / 90.0) * 90.0
                result = True
                
    glColor3f(1.0, 1.0, 0.0)
    if first_launch:
        glRasterPos3f(-3.6, 4.5, 0)
        for c in 'Aperte a tecla espaço para lançar o cubo:':
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    if result:
        glRasterPos3f(-1, 4.5, 0)
        for c in 'Resultado:':
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glRotatef(rotation_angle[0], 1, 0, 0)
    glRotatef(rotation_angle[1], 0, 1, 0)
    glRotatef(rotation_angle[2], 0, 0, 1)

    myCube.draw()
    glPopMatrix()

    glutSwapBuffers()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"Sintese de Imagens")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()