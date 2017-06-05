from display import *
from matrix import *
from math import *
from gmath import *


def scanline_convert(polygons, i, screen, zbuffer):
    global red
    print red
    vert1 = polygons[i]
    vert2 = polygons[i+1]
    vert3 = polygons[i+2]
    color = [red % 255 + 50, 0, 0]
    #sets the top, middle, and bottom verticies
    if vert1[1] >= vert2[1] and vert1[1] >= vert3[1]:
        top = vert1
        if vert2[1] > vert3[1]:
            middle = vert2
            bottom = vert3
        else:
            middle = vert3
            bottom = vert2
    elif vert2[1] >= vert1[1] and vert2[1] >= vert3[1]:
        top = vert2
        if vert1[1] > vert3[1]:
            middle = vert1
            bottom = vert3
        else:
            middle = vert3
            bottom = vert1
    else:
        top = vert3
        if vert1[1] > vert2[1]:
            middle = vert1
            bottom = vert2
        else:
            middle = vert2
            bottom = vert1

    y = bottom[1]
    #case 1: middle and bottom are same
    #case 2: top and middle are same
    #case 3: middle before top
    #case 4: top before middle

    z = int(top[2])
    #case 1: middle and bottom are same
    if middle[1] == bottom[1]:
        #if middle is in front
        if middle[0] < bottom[0]:
            x0 = middle[0]
            x1 = bottom[0]
            x0_step = (top[0] - middle[0]) / (top[1] - middle[1])
            x1_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
        else:
            #if bottom is in front
            x0 = bottom[0]
            x1 = middle[0]
            x0_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
            x1_step = (top[0] - middle[0]) / (top[1] - middle[1])
        #fill in polygon
        for i in range(int(top[1] - bottom[1])):
            draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
            x0 += x0_step
            x1 += x1_step
            y += 1

    #case 2: top and middle are same
    elif top[1] == middle[1]:
        x0 = bottom[0]
        x1 = bottom[0]
        #if top in front
        if top[0] < middle[0]:
            x0_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
            x1_step = (middle[0] - bottom[0]) / (middle[1] - bottom[1])
        #if middle in front
        else:
            x0_step = (top[0] - middle[0]) / (top[1] - middle[1])
            x1_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
        #fill in polygon
        for i in range(int(top[1] - bottom[1])):
            draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
            x0 += x0_step
            x1 += x1_step
            y += 1
    
    else:
        x0 = bottom[0]
        x1 = bottom[0]
        #case 3: middle before top
        if middle[0] < top[0]:
            x0_step = (middle[0] - bottom[0]) / (middle[1] - bottom[1])
            x1_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
            x_top_step = (top[0] - middle[0]) / (top[1] - middle[1])

            #fill in from bottom to middle            
            for i in range(int(middle[1] - bottom[1])):
                draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
                x0 += x0_step
                x1 += x1_step
                y += 1

            #fill in from middle to top
            for i in range(int(top[1] - middle[1])):
                draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
                x0 += x_top_step
                x1 += x1_step
                y += 1
        #case 4: top before middle
        else:
            x0_step = (top[0] - bottom[0]) / (top[1] - bottom[1])
            x1_step = (middle[0] - bottom[0]) / (middle[1] - bottom[1])
            x_top_step = (top[0] - middle[0]) / (top[1] - middle[1])

            for i in range(int(middle[1] - bottom[1])):
                draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
                x0 += x0_step
                x1 += x1_step
                y += 1

            for i in range(int(top[1] - middle[1])):
                draw_line(int(x0), int(y), z, int(x1), int(y), z, screen, zbuffer, color)
                x0 += x0_step
                x1 += x_top_step
                y += 1
    


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0);
    add_point(polygons, x1, y1, z1);
    add_point(polygons, x2, y2, z2);

def draw_polygons( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 3 points to draw'
        return

    point = 0
    global red
    red = 50
    while point < len(matrix) - 2:
        normal = calculate_normal(matrix, point)[:]
        if normal[2] > 0:
            red += 30
            scanline_convert(matrix, point, screen, zbuffer)
            
##            draw_line( int(matrix[point][0]),
##                       int(matrix[point][1]),
##                       matrix[point][2],
##                       int(matrix[point+1][0]),
##                       int(matrix[point+1][1]),
##                       matrix[point+1][2],
##                       screen, zbuffer, color)
##            draw_line( int(matrix[point+2][0]),
##                       int(matrix[point+2][1]),
##                       matrix[point+2][2],
##                       int(matrix[point+1][0]),
##                       int(matrix[point+1][1]),
##                       matrix[point+1][2],
##                       screen, zbuffer, color)
##            draw_line( int(matrix[point][0]),
##                       int(matrix[point][1]),
##                       matrix[point][2],
##                       int(matrix[point+2][0]),
##                       int(matrix[point+2][1]),
##                       matrix[point+2][2],
##                       screen, zbuffer, color)    
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z);
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z);
  
    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1);
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1);
  
    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1);
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1);
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z);
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z);
  
    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1);
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z);
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z);
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1);

def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps

    num_steps+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            
            p0 = lat * (num_steps) + longt
            p1 = p0+1
            p2 = (p1+num_steps) % (num_steps * (num_steps-1))
            p3 = (p0+num_steps) % (num_steps * (num_steps-1))

            if longt != num_steps - 2:
	        add_polygon( edges, points[p0][0],
		             points[p0][1],
		             points[p0][2],
		             points[p1][0],
		             points[p1][1],
		             points[p1][2],
		             points[p2][0],
		             points[p2][1],
		             points[p2][2])
            if longt != 0:
	        add_polygon( edges, points[p0][0],
		             points[p0][1],
		             points[p0][2],
		             points[p2][0],
		             points[p2][1],
		             points[p2][2],
		             points[p3][0],
		             points[p3][1],
		             points[p3][2])

def generate_sphere( cx, cy, cz, r, step ):
    points = []
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps
            
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop+1):
            circ = step * circle

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points
        
def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps
    
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * (num_steps) + longt;
            if (longt == num_steps - 1):
	        p1 = p0 - longt;
            else:
	        p1 = p0 + 1;
            p2 = (p1 + num_steps) % (num_steps * num_steps);
            p3 = (p0 + num_steps) % (num_steps * num_steps);

            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(edges,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps
    
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop):
            circ = step * circle

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]
                
        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y)
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):
            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        loop_start+= 1

    plot( screen, zbuffer, color, x, y, z )

    
