from gl import Render, color

r = Render()
r.glInit()
r.glClearColor(1, 0, 0)
r.glCreateWindow(128, 128)

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
    dx = x2 - x1

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
line(20, 20, 80, 20)
line(20, 20, 20, 80)
line(20, 80, 80, 80)
line(80, 20, 80, 81)
line(20, 80, 60, 100)
line(80, 80, 110, 100)
line(60, 100, 110, 100)
#line(80, 20, 110, 40)
#line(110, 40, 110, 100)
r.point(110, 100)


r.display()


