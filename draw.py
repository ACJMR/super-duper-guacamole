import re
from display import *
from matrix import *
from gmath import *

def add_obj(polygons, filename):
    f = open(filename, "r");
    #r = raw statement
    #^ = start of a line
    #\s = whitespace
    #$ = end of a line
    #(a|b) = or
    filtered = filter(lambda x: not re.match(r'^\s*$', x), f)
    filtered = filter(lambda x: not re.match('(^#|^g)', x), filtered)
    pts = []
    vertices = []
    faces = []
    for line in filtered:
        args = line.split()
        if args[0] == 'v':
            p1 = args[1]
            p2 = args[2]
            p3 = args[3]
            pts = [p1, p2, p3]
            vertices.append(pts)
        elif args[0] == 'f':
            if len(args) == 4:
                if '//' in args[1]:
                    print("found //")
                    p1 = args[1]
                    p1 = p1.split('//')[0]
                    p2 = args[2]
                    p2 = p2.split('//')[0]
                    p3 = args[3]
                    p3 = p3.split('//')[0]
                elif '/' in args[1]:
                    print("found /")
                    p1 = args[1]
                    p1 = p1.split('/')[0]
                    p2 = args[2]
                    p2 = p2.split('/')[0]
                    p3 = args[3]
                    p3 = p3.split('/')[0]
                else:
                    print("didnt find anything")
                    p1 = args[1]
                    p2 = args[2]
                    p3 = args[3]
                pts = [p1, p2, p3]
            elif len(args) == 5:
                if '//' in args[1]:
                    print("FOUND //")
                    p1 = args[1]
                    p1 = p1.split('//')[0]
                    p2 = args[2]
                    p2 = p2.split('//')[0]
                    p3 = args[3]
                    p3 = p3.split('//')[0]
                    p4 = args[4]
                    p4 = p4.split('//')[0]
                elif '/' in args[1]:
                    p1 = args[1]
                    p1 = p1.split('/')[0]
                    p2 = args[2]
                    p2 = p2.split('/')[0]
                    p3 = args[3]
                    p3 = p3.split('/')[0]
                    p4 = args[4]
                    p4 = p4.split('/')[0]
                else:
                    print("DID NOT FIND ANYTHING")
                    p1 = args[1]
                    p2 = args[2]
                    p3 = args[3]
                    p4 = args[4]
                pts = [p1, p2, p3, p4]
            faces.append(pts)
    for face in faces:
        if len(face) == 3:
            vertex1 = (int(face[0]) - 1) % len(vertices)
            vertex2 = (int(face[1]) - 1) % len(vertices)
            vertex3 = (int(face[2]) - 1) % len(vertices)
            x0 = float(vertices[vertex1][0])
            y0 = float(vertices[vertex1][1])
            z0 = float(vertices[vertex1][2])
            x1 = float(vertices[vertex2][0])
            y1 = float(vertices[vertex2][1])
            z1 = float(vertices[vertex2][2])
            x2 = float(vertices[vertex3][0])
            y2 = float(vertices[vertex3][1])
            z2 = float(vertices[vertex3][2])
            add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2)

        elif len(face) == 4:
            vertex1 = (int(face[0]) - 1) % len(vertices)
            vertex2 = (int(face[1]) - 1) % len(vertices)
            vertex3 = (int(face[2]) - 1) % len(vertices)
            vertex4 = (int(face[3]) - 1) % len(vertices)
            x0 = float(vertices[vertex1][0])
            y0 = float(vertices[vertex1][1])
            z0 = float(vertices[vertex1][2])
            x1 = float(vertices[vertex2][0])
            y1 = float(vertices[vertex2][1])
            z1 = float(vertices[vertex2][2])
            x2 = float(vertices[vertex3][0])
            y2 = float(vertices[vertex3][1])
            z2 = float(vertices[vertex3][2])
            add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2)
            x0 = float(vertices[vertex3][0])
            y0 = float(vertices[vertex3][1])
            z0 = float(vertices[vertex3][2])
            x1 = float(vertices[vertex4][0])
            y1 = float(vertices[vertex4][1])
            z1 = float(vertices[vertex4][2])
            x2 = float(vertices[vertex1][0])
            y2 = float(vertices[vertex1][1])
            z2 = float(vertices[vertex1][2])
            add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2)

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color0, color1=[300,300,300], normal0=[600, 600, 600], normal1=[600,600,600]):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        if color1[0] != 300:
            colort = color0
            color0 = color1
            color1 = colort
        if normal0[0] != 600:
            normalt = normal0
            normal0 = normal1
            normal1 = normalt
    x = x0
    z = z0
    if color1[0] != 300:
        r = color0[0]
        g = color0[1]
        b = color0[2]
    if normal0[0] != 600:
        nx = normal0[0]
        ny = normal0[1]
        nz = normal0[2]

    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    if color1[0] != 300:
        dr = (color1[0] - color0[0]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        dg = (color1[1] - color0[1]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        db = (color1[2] - color0[2]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    if normal0[0] != 600:
        dnx = (normal1[0] - normal0[0]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        dny = (normal1[1] - normal0[1]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        dnz = (normal1[2] - normal0[2]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        if color1[0] != 300:
            color = [int(r),int(g),int(b)]
        elif normal0[0] != 600:
            normal = [nx, ny, nz]
            color = get_lighting(normal, color0[0], color0[1], color0[2], color0[3], color0[4])
        else:
            color = color0
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z
        if color1[0] != 300:
            r += dr
            g += dg
            b += db
        if normal0[0] != 600:
            nx += dnx
            ny += dny
            nz += dnz

def scanline_convert(polygons, i, screen, zbuffer, color=["a"], normals=[600, 600, 600]):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1
    PNT = 0
    CLR = 1
    NRM = 2

    flat = isinstance(color[0], int)
    int_color = isinstance(color[0], str)
    points = [ [(polygons[i][0], polygons[i][1], polygons[i][2]), color[0], normals[0]],
               [(polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]), color[1], normals[1]],
               [(polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]), color[2], normals[2]]]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[PNT][1])
    x0 = points[BOT][PNT][0]
    z0 = points[BOT][PNT][2]
    x1 = points[BOT][PNT][0]
    z1 = points[BOT][PNT][2]
    if not int_color and normals[0] == 600 and not flat:
        r0 = points[BOT][CLR][0]
        g0 = points[BOT][CLR][1]
        b0 = points[BOT][CLR][2]
        r1 = points[BOT][CLR][0]
        g1 = points[BOT][CLR][1]
        b1 = points[BOT][CLR][2]
    if normals[0] != 600:
        nx0 = points[BOT][NRM][0]
        ny0 = points[BOT][NRM][1]
        nz0 = points[BOT][NRM][2]
        nx1 = points[BOT][NRM][0]
        ny1 = points[BOT][NRM][1]
        nz1 = points[BOT][NRM][2]

    y = int(points[BOT][PNT][1])

    distance0 = int(points[TOP][PNT][1]) - y * 1.0 + 1
    distance1 = int(points[MID][PNT][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][PNT][1]) - int(points[MID][PNT][1]) * 1.0 + 1

    dx0 = (points[TOP][PNT][0] - points[BOT][PNT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][PNT][2] - points[BOT][PNT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][PNT][0] - points[BOT][PNT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][PNT][2] - points[BOT][PNT][2]) / distance1 if distance1 != 0 else 0
    if not int_color and normals[0] == 600 and not flat:
        dr0 = (points[TOP][CLR][0] - points[BOT][CLR][0]) / distance0 if distance0 != 0 else 0
        dg0 = (points[TOP][CLR][1] - points[BOT][CLR][1]) / distance0 if distance0 != 0 else 0
        db0 = (points[TOP][CLR][2] - points[BOT][CLR][2]) / distance0 if distance0 != 0 else 0
        dr1 = (points[MID][CLR][0] - points[BOT][CLR][0]) / distance1 if distance1 != 0 else 0
        dg1 = (points[MID][CLR][1] - points[BOT][CLR][1]) / distance1 if distance1 != 0 else 0
        db1 = (points[MID][CLR][2] - points[BOT][CLR][2]) / distance1 if distance1 != 0 else 0
    if normals[0] != 600:
        dnx0 = (points[TOP][NRM][0] - points[BOT][NRM][0]) / distance0 if distance0 != 0 else 0
        dny0 = (points[TOP][NRM][1] - points[BOT][NRM][1]) / distance0 if distance0 != 0 else 0
        dnz0 = (points[TOP][NRM][2] - points[BOT][NRM][2]) / distance0 if distance0 != 0 else 0
        dnx1 = (points[MID][NRM][0] - points[BOT][NRM][0]) / distance1 if distance1 != 0 else 0
        dny1 = (points[MID][NRM][1] - points[BOT][NRM][1]) / distance1 if distance1 != 0 else 0
        dnz1 = (points[MID][NRM][2] - points[BOT][NRM][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][PNT][1]):
        if ( not flip and y >= int(points[MID][PNT][1])):
            flip = True

            dx1 = (points[TOP][PNT][0] - points[MID][PNT][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][PNT][2] - points[MID][PNT][2]) / distance2 if distance2 != 0 else 0
            if not int_color and normals[0] == 600 and not flat:
                dr1 = (points[TOP][CLR][0] - points[MID][CLR][0]) / distance2 if distance2 != 0 else 0
                dg1 = (points[TOP][CLR][1] - points[MID][CLR][1]) / distance2 if distance2 != 0 else 0
                db1 = (points[TOP][CLR][2] - points[MID][CLR][2]) / distance2 if distance2 != 0 else 0
            if normals[0] != 600:
                dnx1 = (points[TOP][NRM][0] - points[MID][NRM][0]) / distance2 if distance2 != 0 else 0
                dny1 = (points[TOP][NRM][1] - points[MID][NRM][1]) / distance2 if distance2 != 0 else 0
                dnz1 = (points[TOP][NRM][2] - points[MID][NRM][2]) / distance2 if distance2 != 0 else 0

            x1 = points[MID][PNT][0]
            z1 = points[MID][PNT][2]
            if not int_color and normals[0] == 600 and not flat:
                r1 = points[MID][CLR][0]
                g1 = points[MID][CLR][1]
                b1 = points[MID][CLR][2]
            if normals[0] != 600:
                nx1 = points[MID][NRM][0]
                ny1 = points[MID][NRM][1]
                nz1 = points[MID][NRM][2]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        if not int_color and normals[0] == 600 and not flat:
            color0 = [r0, g0, b0]
            color1 = [r1, g1, b1]
            draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color0, color1)
        elif normals[0] != 600:
            normal0 = [nx0, ny0, nz0]
            normal1 = [nx1, ny1, nz1]
            fakecolor1 = [300, 300, 300]
            draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color, fakecolor1, normal0, normal1)
        else:
            draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        if not int_color and normals[0] == 600 and not flat:
            r0+= dr0
            g0+= dg0
            b0+= db0
            r1+= dr1
            g1+= dg1
            b1+= db1
        if normals[0] != 600:
            nx0+= dnx0
            ny0+= dny0
            nz0+= dnz0
            nx1+= dnx1
            ny1+= dny1
            nz1+= dnz1
        y+= 1

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect, shading):
    print(shading)
    if len(polygons) < 2:
        print 'Need at least 3 points to draw'
        return

    point = 0
    if shading == "gouraud" or shading == "phong":
        vnorms = {}
        while point < len(polygons) - 2:
            norm = calculate_normal(polygons, point)
            normalize(norm)
            #if it doesn't exist, create the key
            if tuple(polygons[point]) not in vnorms.keys():
                #set to zero
                vnorms[tuple(polygons[point])] = [0, 0, 0]
            if tuple(polygons[point + 1]) not in vnorms.keys():
                vnorms[tuple(polygons[point + 1])] = [0, 0, 0]
            if tuple(polygons[point + 2]) not in vnorms.keys():
                vnorms[tuple(polygons[point + 2])] = [0, 0, 0]

        # for averaging of the normals
            #accumulating the sums
            nx = norm[0]
            print("normalx", nx)
            ny = norm[1]
            print("normaly", ny)
            nz = norm[2]
            print("normalz", nz)
            vnorms[tuple(polygons[point])] = [vnorms[tuple(polygons[point])][0] + nx,  vnorms[tuple(polygons[point])][1] + ny, vnorms[tuple(polygons[point])][2] + nz]
            vnorms[tuple(polygons[point + 1])] = [vnorms[tuple(polygons[point + 1])][0] + nx, vnorms[tuple(polygons[point + 1])][1] + ny, vnorms[tuple(polygons[point + 1])][2] + nz]
            vnorms[tuple(polygons[point + 2])] = [vnorms[tuple(polygons[point + 2])][0] + nx, vnorms[tuple(polygons[point + 2])][1] + ny, vnorms[tuple(polygons[point + 2])][2] + nz]
            point += 3
        for key in vnorms:
            print("before", vnorms[key])
            normalize(vnorms[key])
            print("after", vnorms[key])

    point = 0
    while point < len(polygons) - 2:

        normal = calculate_normal(polygons, point)[:]

        if normal[2] > 0:
            if shading == "flat":
                color = get_lighting(normal, view, ambient, light, symbols, reflect )
                scanline_convert(polygons, point, screen, zbuffer, color)
            elif shading == "gouraud":
                normal0 = vnorms[tuple(polygons[point])]
                normal1 = vnorms[tuple(polygons[point + 1])]
                normal2 = vnorms[tuple(polygons[point + 2])]
                color0 = get_lighting(normal0, view, ambient, light, symbols, reflect)
                color1 = get_lighting(normal1, view, ambient, light, symbols, reflect)
                color2 = get_lighting(normal2, view, ambient, light, symbols, reflect)
                colors = [color0, color1, color2]
                print("point: ", point)
                print("npoint: ", normal0)
                scanline_convert(polygons, point, screen, zbuffer, colors)
            elif shading == "phong":
                normal0 = vnorms[tuple(polygons[point])]
                normal1 = vnorms[tuple(polygons[point + 1])]
                normal2 = vnorms[tuple(polygons[point + 2])]
                save_for_color = [view, ambient, light, symbols, reflect]
                normals = [normal0, normal1, normal2]
                scanline_convert(polygons, point, screen, zbuffer, save_for_color, normals)

            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            screen, zbuffer, color)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
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

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
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
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


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



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color0, color1=[300,300,300]):

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
        #if a 2nd normal exists
        if color1[0] != 300:
            cnormt = color0
            color0 = color1
            color1 = cnormt

    x = x0
    y = y0
    z = z0
    if color1[0] != 300:
        r = color0[0]
        g = color0[1]
        b = color0[2]
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
        distance = x1 - x + 1
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
        distance = abs(y1 - y) + 1
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

    dz = (z1 - z0) / distance if distance != 0 else 0
    if color1[0] != 300:
        dr = (color1[0] - color0[0]) / distance if distance != 0 else 0
        dg = (color1[1] - color0[1]) / distance if distance != 0 else 0
        db = (color1[2] - color0[2]) / distance if distance != 0 else 0
    while ( loop_start < loop_end ):
        if color1[0] != 300:
            color = [int(r),int(g),int(b)]
        else:
            color = color0
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
        z+= dz
        if color1[0] != 300:
            r+= dr
            g+= dg
            b+= db
        #change color here
        loop_start+= 1
    #change color again
    if color1[0] != 300:
        print("not 300")
        color = [int(r),int(g),int(b)]
    else:
        color = color0
    plot( screen, zbuffer, color, x, y, z )
