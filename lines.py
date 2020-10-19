from gl import Render, color

r = Render()
r.glInit()
r.glClearColor(1, 0, 0)
r.glCreateWindow(800, 600)

def line(x1, y1, x2, y2):
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
    dx = abs(x2 - x1)

    offset = 0 
    threshold = 1 * dx
    y = y1
    for x in range(x1, x2):
        if steep:
            r.point(y, x)
        else:
            r.point(x, y)
        offset += dy * 2 
        if offset>= threshold:
            y += 1 if y1 < y2 else -1
            threshold += 2 * dx

#line(0, 0, 100, 100)
line(165, 380, 185, 360)
line(180, 330, 207, 345)
line(233, 330, 230, 360)
line(250, 380, 220, 385)
line(205, 410, 193, 383)



r.display()


