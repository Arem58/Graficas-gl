import struct

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
        self.Xw = int((x + 1) * (self.widthV * 0.5) + self.x)
        self.Yw = int((y + 1) * (self.heightV *0.5 ) + self.y)
        if self.Xw == self.widthV: 
            self.Xw -= 1
        if self.Yw == self.heightV: 
            self.Yw -= 1
        self.framebuffer[self.Yw][self.Xw] = self.vertexColor
        print(self.Yw, self.Xw)

    def glClearColor(self, r, g, b):
        self.r = (int(r * 255))
        self.g = (int(g * 255))
        self.b = (int(b * 255))
        self.color = color(self.r, self.g, self.b)

    def glColor(self, r, g, b):
        self.r = (int(r * 255))
        self.g = (int(g * 255))
        self.b = (int(b * 255))
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
        
    def point(self, x ,y):
        self.framebuffer[y][x] = color(0, 0, 0)
    
    def line(self, x1, y1, x2, y2):
        dy = (y2 - y1)
        dx = abs(x2 - x1)

        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = x2 - x1

        offset = 0 
        threshold = 1 * dx
        y = y1
        for x in range(x1, x2):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            offset += dy * 2 
            if offset>= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx

bitmap = Render()
bitmap.glClearColor(1, 0, 0)
bitmap.glInit()
bitmap.glCreateWindow(128, 128)
bitmap.glColor(1, 1, 1)
bitmap.glViewPort(0, 0, 800, 600)
#bitmap.point(400, 300)
#bitmap.point(300, 400)
#for x in range(100):
    #for y in range(600):
        #bitmap.point(y, x)
#bitmap.glVertex(-1, 1)
bitmap.line(20, 20, 80, 20)
bitmap.line(20, 20, 20, 80)
bitmap.line(20, 80, 80, 80)
bitmap.line(80, 20, 80, 81)
bitmap.line(20, 80, 60, 100)
bitmap.line(80, 80, 110, 100)
bitmap.line(60, 100, 110, 100)
bitmap.line(80, 20, 110, 40)
bitmap.line(110, 40, 110, 100)
bitmap.point(110, 100)
bitmap.display()
bitmap.glFinish('out.bmp')
    


