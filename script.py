import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    name = 'default'
    num_frames = 1

    for command in commands:
        c = command["op"]
        args = command["args"]
        if c == "basename":
            name = args[0]
        if c == "frames":
            num_frames = args[0]
        if c == "vary":
            if num_frames == 1:
                quit()
    if name == 'default':
        print("Basename is not found and default is used as a name instead")
    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a separate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropriate value.
  ===================="""
def second_pass( commands, num_frames, symbols):
    frames = [ {} for i in range(int(num_frames)) ]
    for command in commands:
        c = command["op"]
        if c == "vary":
            knob = command["knob"]
            args = command["args"]
            counter = 0
            if (symbols[knob][1] == 0): #linear
                start_frame = args[0]
                end_frame = args[1]
                start_value = args[2]
                end_value = args[3]
                for i, fram in enumerate(frames):
                    if i <= end_frame and i >= start_frame:
                        frames_bet = end_frame - start_frame
                        step = (end_value - start_value)/frames_bet
                        frames[i][knob] = start_value + counter*step
                        counter = counter + 1;
            if (symbols[knob][1] == 1): #polynomial degree n
                n = args[0]
                start_frame = args[1]
                end_frame = args[2]
                start_value = args[3]
                end_value = args[4]
                for i, fram in enumerate(frames):
                    if i <= end_frame and i >= start_frame:
                        numstep = end_frame - start_frame
                        dx = (end_value - start_value)/numstep
                        num = math.pow(start_value + dx*counter,n)
                        #print start_value + num
                        frames[i][knob] = num
                        counter = counter + 1;
            '''if (symbols[knob][1] == 2): #exponential base b
                b = args[0]
                start_frame = args[1]
                end_frame = args[2]
                start_value = args[3]
                end_value = args[4]
                for i, fram in enumerate(frames):
                    if i <= end_frame and i >= start_frame:
                        numstep = end_frame - start_frame
                        dx = (1/b)*(end_value-start_value)/numstep
                        num = math.pow(b,start_value + dx*counter) - 1
                        print(num)
                        frames[i][knob] = num
                        counter = counter + 1;'''

    return frames

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    print(symbols)
    reflect = '.white'
    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames,symbols)

    tmp = new_matrix()
    ident( tmp )

    #stack = [ [x[:] for x in tmp] ]
    #screen = new_screen()
    #zbuffer = new_zbuffer()
    #tmp = []
    step_3d = 10
    consts = ''
    coords = []
    coords1 = []
    for i, frame in enumerate(frames):
        tmp = new_matrix()
        ident( tmp )


        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []

        #checking what type of shading the user wants
        if 'shading' in symbols:
            shading = symbols['shading'][1]
        else:
            shading = 'flat'

        for command in commands:
            c = command['op']
            args = command['args']
            knob_value = 1

            if c == 'mesh':
                #print(args[0])
                filename = args[0] + ".obj"
                add_obj(tmp, filename)
                matrix_mult(stack[-1], tmp)
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
            elif c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                        args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect, shading)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if command["knob"] is not None:
                    knob_value = frames[i][command["knob"]]
                tmp = make_translate(args[0]*knob_value, args[1]*knob_value, args[2]*knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if command["knob"] is not None:
                    knob_value = frames[i][command["knob"]]
                tmp = make_scale(args[0]*knob_value, args[1]*knob_value, args[2]*knob_value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                if command["knob"] is not None:
                    knob_value = frames[i][command["knob"]]

                theta = args[1] * (math.pi/180) * knob_value
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
        num = format(i, "03")
        save_extension(screen, "anim/" + name + num)
        # end operation loop
