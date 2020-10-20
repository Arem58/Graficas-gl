import struct
from obj import Obj
from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

#se codifica en bytes lo que entre como parametro 
def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])


class Render(object):
    def glInit(self):
        self.framebuffer = []
        self.currentColor = color(0, 0, 0)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.color for x in range(self.width)]
            for y in range(self.height)
        ]

    def glViewPort(self, x, y, widthV, heightV):
        self.x = x
        self.y = y
        self.widthV = widthV
        self.heightV = heightV

    def glVertex(self, y, x):
        self.Xw = round((x + 1) * (self.widthV * 0.5) + self.x)
        self.Yw = round((y + 1) * (self.heightV *0.5 ) + self.y)
        if self.Xw == self.widthV: 
            self.Xw -= 1
        if self.Yw == self.heightV: 
            self.Yw -= 1
        self.framebuffer[self.Yw][self.Xw] = self.vertexColor

    def glClearColor(self, r, g, b):
        self.r = (round(r * 255))
        self.g = (round(g * 255))
        self.b = (round(b * 255))
        self.color = color(self.r, self.g, self.b)

    def glColor(self, r, g, b):
        self.r = (round(r * 255))
        self.g = (round(g * 255))
        self.b = (round(b * 255))
        self.vertexColor = color(self.r, self.g, self.b)

    def glFinish(self, filename):
        f = open(filename, 'bw')
        
        #file header
        #1 bytes es equivalente a char
        f.write(char('B'))
        f.write(char('M'))
        # 14 bytes del header + 40 bytes del info header + pixeles de la imagen 
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data 
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])
        
        f.close()
    
    def load(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face) 

            for j in range(vcount):
                vi1 = face[j][0] - 1
                vi2 = face[(j + 1) % vcount][0] - 1

                v1 = model.vertices[vi1]
                v2 = model.vertices[vi2]

                x1 = round(v1[0] * scale[0]) + translate[0] 
                y1 = round(v1[1] * scale[1]) + translate[1] 
                x2 = round(v2[0] * scale[0]) + translate[0] 
                y2 = round(v2[1] * scale[1]) + translate[1] 
                self.line(V2(x1, y1), V2(x2, y2))

    #carga los vectores y los conbierte en coordenadas x, y
    def loadPol(self, pol):
        vcount = len(pol)
        for i in range(len(pol)):
            x1 = pol[i][0] 
            y1 = pol[i][1] 
            x2 = pol[(i + 1) % vcount][0] 
            y2 = pol[(i + 1) % vcount][1]
            self.line(V2(x1, y1), V2(x2, y2))
        
    #Se agrega los limites de x y y con su maximo y minimo, el color del borde, el color del fondo, el color que va a pintar, el poligono y si es un poligono adentro de otro puedes agregar el color que se ignorara  
    def fillPol(self, yMin, yMax, xMin, xMax, borderColor, defaultColor, fillColor, pol, ignoredColor = None):
        border = []
        for y in range(yMin, yMax):
            pair = 0
            body = 0
            onBody = False 
            temp = 0
            vertex = False
            for x in range(xMin, xMax + 1): 
                #if y == 10:
                    #print(x)
                i = x
                if self.framebuffer[y][x] == borderColor:
                    #Detecta si esta en un borde y ve el tamanio que tiene el borde para poder recorrerlo
                    if not onBody:
                        while True:
                            #Se le suma 1 al cuerpo para tener el tamanio del cuerpo
                            body += 1
                            #Se termino de recorrer el borde y ya se llego al fondo de la imagen
                            if self.framebuffer[y][i + 1] == defaultColor or ignoredColor:
                                onBody = True
                                #Se tiene un contador para saber si es par o impar para ver si ya estan los dos estremos para pintar
                                pair += 1
                                break
                            #tiene el valor de x para poder ir reccoriendo el borde sin afectar a x 
                            i += 1
                    #Luego de tener el tamanio del borde se recorre restandole 1 al cuerpo del borde
                    body -= 1
                    #Cuando se esta en el ultimo bloque del borde o un borde de un cuadro
                    if body == 0:
                        onBody = False
                        #Si es impar detecta el primer vertice
                        if (pair % 2) == 1:
                            if self.framebuffer[y][x + 1] == defaultColor or ignoredColor:

                                #Se guarda temporalmente el primer vertice para luego agregarlo a la lista
                                temp = V2(x, y)
                        #Si es par detecta el ultimo vertice para poder pintar de extremo a extremo 
                        if (pair % 2) == 0:
                            if self.framebuffer[y][x - 1] == defaultColor or ignoredColor:
                                #Se agrega a la lista de borde en orden para poder recorrerlo luego
                                border.append(temp)
                                border.append(V2(x, y))
                    #Cuando se esta en el cuerpo del borde todavia 
                    else: 
                        #Si es par detecta el ultimo vertice para poder pintar de extremo a extremo 
                        if (pair % 2) == 0:
                            if self.framebuffer[y][x - 1] == defaultColor:
                                #Se agrega a la lista de borde en orden para poder recorrerlo luego
                                border.append(temp)
                                border.append(V2(x, y))
        #Funcion para pintar recorriendo la lista del borde
        for i in range(len(border) - 1):
            xi = border[i]
            xf = border[i + 1]
            #Se recorre de liminte inicial a final para pintar lineas horizontales
            for x in range(xi.x + 1, xf.x):
                borderSup = False
                borderInf = False
                #Se detecta si el pixel que se va a pintar tiene borde inferior para ver si esta adentro del poligono
                for y in range(xi.y, yMin, -1):
                    if self.framebuffer[y][x] == borderColor:
                        borderInf = True
                #Se detecta si el pixel que se va a pintar tiene borde superior para ver si esta adentro del poligono
                for y in range(xi.y, yMax):
                    if self.framebuffer[y][x] == borderColor:
                        borderSup = True
                #Se detecta si tiene los 2 border para estar encerrado 
                if borderInf == True and borderSup == True:
                    #Pinta solo si detecta el fondo de la imagen o el color ignorado
                    if self.framebuffer[xi.y][x] == defaultColor or ignoredColor:
                        #Pinta el pixel
                        self.point(x, (xi.y), fillColor)

    #codigo de prueba, Dennis Aldana
    def display(self, filename='out.bmp'):

        """
        Displays the image, a external library (wand) is used, but only for convenience during development
        """
    
        self.glFinish(filename)

        try:
            from wand.image import Image
            from wand.display import display

            with Image(filename=filename) as image:
                display(image)
        except ImportError:
            pass  # do nothing if no wand is installed
        
    def point(self, x ,y, color = None):
        try:
            self.framebuffer[y][x] = color or self.currentColor
        except:
            pass
    
    def line(self, A, B):
        x1 = A.x 
        y1 = A.y 
        x2 = B.x
        y2 = B.y 
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0 
        threshold = dx
        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            offset += dy * 2 
            if offset>= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx


bitmap = Render()
bitmap.glClearColor(1, 0, 1)
bitmap.glInit()
bitmap.glCreateWindow(800, 600)
bitmap.glColor(1, 1, 1)
bitmap.glViewPort(0, 0,400, 300)
#bitmap.load('./Modelos/face.obj', translate = [400, 300], scale = [20, 20])
pol1 = [V2(165, 380), V2(185, 360), V2(180, 330), V2(207, 345), V2(233, 330), V2(230, 360), V2(250, 380), V2(220, 385), V2(205, 410), V2(193, 383)]
pol2 = [V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)]
pol3 = [V2(377, 249), V2(411, 197), V2(436, 249)]
pol4 = [V2(413, 177), V2(448, 159), V2(502, 88), V2(553, 53), V2(535, 36),
V2(676, 37), V2(660, 52), V2(750, 145), V2(761, 179), V2(672, 192), 
V2(659, 214), V2(615, 214), V2(632, 230), V2(580, 230),
V2(597, 215), V2(552, 214), V2(517, 144), V2(466, 180)]
pol5 = [V2(682, 175), V2(708, 120), V2(735, 148), V2(739, 170)]
#bitmap.triangle(V2(10, 70), V2(50, 160), V2(70, 80), color(255, 0, 0))
#bitmap.triangle(V2(180, 50), V2(150, 1),  V2(70, 180), color(0, 255, 0))
#bitmap.triangle(V2(180, 150), V2(120, 160), V2(130, 180), color(0, 0, 255))
bitmap.loadPol(pol4)
bitmap.loadPol(pol2)
bitmap.loadPol(pol1)

#Cuadrado
#bitmap.line(V2(2,2), V2(2,18))
#bitmap.line(V2(18,2), V2(18,18))
#bitmap.line(V2(2,2), V2(18,2))
#bitmap.line(V2(2,18), V2(19,18))

#Triangulo
#bitmap.line(V2(2,2), V2(18,2))
#bitmap.line(V2(2,2), V2(10,18))
#bitmap.line(V2(18,2), V2(10,18))

#bitmap.fillPol(330, 410, 165, 250, color(0,0,0), color(255, 0, 255), color(0, 255, 0), pol1)
#bitmap.fillPol(250, 336, 288, 374, color(0,0,0), color(255, 0, 255), color(255, 255, 0), pol2)
#bitmap.fillPol(35, 231, 413, 761, color(0,0,0), color(255, 0, 255), color(0, 0, 255), pol4)
bitmap.loadPol(pol3)
bitmap.fillPol(197, 250, 377, 436, color(0,0,0), color(255, 0, 255), color(0, 255, 255), pol3)

bitmap.loadPol(pol5)
#bitmap.fillPol(120, 176, 682, 739, color(0,0,0), color(255, 0, 255), color(255, 255, 255), color(0, 0, 255))

bitmap.display()
bitmap.glFinish('out.bmp')
    


