# Letícia Maria Eufrásio Reis / Maria Luiza Pereira Sousa / Maria Auxiliadora de Oliveira Chaves
# 04/08/2025
# Trabalho de Síntese de Imagens

import time
import random
from math import cos, sin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# posição do chão
ground_y = -2.5

# tamanho da aresta do dado
size_dice = 2

# posição vertical inicial do dado (encostado no chão)
pos_y = ground_y + size_dice / 2

# movimentação
vel_y = 0.0 # velocidade vertical inicial do dado
acc_y = -9.8 # gravidade
rotation_speed = [0.0, 0.0, 0.0] # velocidade de rotação
rotation_angle = [0.0, 0.0, 0.0] # ângulo de rotação

# estado
bouncing = False # no ar? 
first_launch = True # primeira vez?
result = False # mostrar resultado?

# tempo da última atualização de quadro
last_time = time.time()


# classe Ground
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


# classe Dice
class Dice:
    def __init__(self, base):
        self.base = base / 2.0

    # desenha um ponto com base na posição recebida
    def draw_dot(self, x, y, radius=0.1):
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 0)
        glVertex2f(x, y)
        for angle in range(0, 361, 30):
            rad = angle * 3.14159 / 180.0
            glVertex2f(x + radius * cos(rad), y + radius * sin(rad))
        glEnd()

    # para cada face, desenha seus pontos
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
        # desenha as faces do dado
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
            # desenha os pontos das faces
            self.draw_dice_face(num)
            glPopMatrix()


# instanciando objetos
myDice = Dice(size_dice)
myGround = Ground(ground_y)


# funcionamento das teclas
def keyboard(key, _x, _y):
    global vel_y, rotation_speed, bouncing, result, first_launch

    if key == b'\x1b':
        exit(0)
    elif key == b' ' and not bouncing: # quando tecla espaço e não está no ar
        vel_y = 6.0 # velocidade para cima
        bouncing = True # está no ar
        result = False # não mostra "Resultado:"
        first_launch = False # depois que aperta espaço pela primeira vez, não é mais a primeira jogada
        rotation_speed = [ # a velocidade de rotação para cada eixo é definida aleatoriamente e apenas uma vez
            random.uniform(300, 600), # eixo x
            random.uniform(300, 600), # eixo y
            random.uniform(300, 600) # eixo z
        ]
    glutPostRedisplay() # redesenha


# configuração inicial
def init():
    glClearColor(0.1, 0.1, 0.25, 1)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


# função de display
def display():
    global pos_y, vel_y, rotation_angle, last_time, bouncing, result, first_launch, size_dice

    # usaremos o tempo para calcular quanto o dado deve subir ou descer e quanto ele deve girar
    now = time.time()
    dt = now - last_time
    last_time = now

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0) # posição da câmera

    myGround.draw() # desenha chão 

    if bouncing: # se o cubo está no ar
        vel_y += acc_y * dt # atualiza a velocidade com base na gravidade // aceleração afeta a velocidade (v = v0 + a*t)
        pos_y += vel_y * dt # atualiza a posição com base nessa velocidade // velocidade afeta a posição (s = s0 + v*t)
        for i in range(3):
            # para cada eixo de rotação, vamos pegar a velocidade naquele eixo, multiplicar pelo tempo decorrido e somar esse valor ao ângulo de rotação atual
            rotation_angle[i] += rotation_speed[i] * dt

        if pos_y <= ground_y + size_dice / 2: # se estiver no chão
            pos_y = ground_y + size_dice / 2
            vel_y = -vel_y * 0.4 # quica
            for i in range(3):
                rotation_speed[i] *= 0.5 # velocidade de cada eixo diminuida pela metade
            if abs(vel_y) < 0.1 and max(rotation_speed) < 1: # se está quase parado
                bouncing = False # não está mais no ar
                for i in range(3):
                    rotation_angle[i] = round(rotation_angle[i] / 90.0) * 90.0 # arredonda os ângulos para múltiplos de 90
                result = True

    glPushMatrix()

    glTranslatef(0, pos_y, 0) # vamos desenhar o dado na tela de acordo com sua posição atual

    # aplica rotações para cada eixo
    glRotatef(rotation_angle[0], 1, 0, 0)
    glRotatef(rotation_angle[1], 0, 1, 0)
    glRotatef(rotation_angle[2], 0, 0, 1)

    myDice.draw() # desenha dado
    glPopMatrix() # isola a transformação atual da seguinte

    glColor3f(1.0, 1.0, 0.0)
    if first_launch: # se for a primeira jogada
        glRasterPos3f(-3.6, 4.5, 0)
        for c in 'Aperte a tecla espaço para lançar o dado:':
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    if result: # se deve mostrar resultado
        glRasterPos3f(-1, 4.5, 0)
        for c in 'Resultado:':
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glutSwapBuffers()
    glutPostRedisplay()


# função main
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