import struct

#se codifica en bytes lo que entre como parametro 
def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])


class Render(object):
    def glInit(self):
        self.framebuffer = []

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

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

    def glVertex(self, x, y):
        self.Xw = int((x + 1) * (self.widthV * 0.5) + self.x)
        self.Yw = int((y + 1) * (self.heightV *0.5 ) + self.y)
        if self.Xw == self.widthV: 
            self.Xw -= 1
        if self.Yw == self.heightV: 
            self.Yw -= 1
        self.framebuffer[self.Yw][self.Xw] = self.vertexColor

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
        f.write(dword(14 + 40 + self.height * self.width * 3))
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
        for x in range(self.widthV):
            for y in range(self.heightV):
                f.write(self.framebuffer[y + self.y][x + self.x])
        
        f.close()
    
    def point(self, x ,y):
        self.framebuffer[y][x] = color(0, 0, 0)

bitmap = Render()
bitmap.glInit()
bitmap.glCreateWindow(800, 600)
bitmap.glClearColor(1, 0, 0)
bitmap.glColor(1, 1, 1)
bitmap.clear()
bitmap.glViewPort(0, 0, 800, 600)
#bitmap.point(400, 300)
#bitmap.point(300, 400)
for x in range(50):
    for y in range(100):
        bitmap.point(y, x)
bitmap.glVertex(0, 0)


bitmap.glFinish('out.bmp')
    


