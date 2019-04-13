from typing import Any, Union

from matplotlib.pyplot import xlim, plot, vlines, legend, savefig, show, hlines, title, ylim
import numpy as np
import math
from sympy.solvers import solve
from sympy import Symbol, Interval

# main loop

num_lines = sum(1 for line in open("input.txt"))
with open("input.txt") as input_file:
    lines = input_file.readlines()
output_file = open("output.txt", 'w')

for i in range(0, num_lines):

    print("kolejnyyyyyyyyyyyyyyyyyy ---------------------------------------------------------------------------------")
    data = lines[i].strip().split(';')

    ''' starting position '''
    starting_position = data[0].strip()[1:-1].split(',')
    starting_x = float(starting_position[0])
    starting_y = float(starting_position[1])

    ''' mass '''
    mass = float(data[1])

    ''' radius '''
    radius = float(data[2])

    ''' coefficient of friction '''
    c_friction = float(data[3])

    ''' velocity '''
    velocity_vector = data[4].strip()[1:-1].split(',')
    velocity_x = float(velocity_vector[0])
    velocity_y = float(velocity_vector[1])

    ''' acceleration '''
    g = 10
    acceleration = c_friction * g
    alpha = math.atan(velocity_y / velocity_x)

    acceleration_x = math.cos(alpha) * acceleration
    acceleration_y = math.sin(alpha) * acceleration

    ''' total time '''
    velocity = math.sqrt(velocity_x * velocity_x + velocity_y * velocity_y)
    time = velocity / acceleration

    ''' finding the bounce points'''
    while time > 0:
        t = Symbol('t')
        motion_x = starting_x + velocity_x * t - 0.5 * acceleration_x * t * t
        motion_y = starting_y + velocity_y * t - 0.5 * acceleration_y * t * t

        ''' top or right '''
        if velocity_x >= 0 and velocity_y >= 0:
            time_x_bool = solve([t >= 0, t <= time, motion_x - 60], t)
            time_y_bool = solve([t >= 0, t <= time, motion_y - 40], t)
            print("\n", time_x_bool)
            print(time_y_bool)

            # top or right
            if time_x_bool != False and time_y_bool != False:
                time_x = solve(motion_x - 60, t)
                print(time_x)
                time_y = solve(motion_y - 40, t)
                print(time_y)

                if time_x[0] > 0 and time_y[0] > 0:

                    # right
                    if time_x[0] < time_y[0]:
                        time = time - time_x[0]
                        velocity_x = velocity_x - acceleration_x*time
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x

                    # top
                    else:
                        time = time - time_y[0]
                        velocity_y = velocity_y - acceleration_y*time
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y

                elif time_x[0] <= 0 and time_y[0] > 0:

                    # right
                    if time_x[1] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] > 0 and time_y[0] <= 0:

                    # right
                    if time_x[0] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

                elif time_x[0] <= 0 and time_y[0] <= 0:

                    # right
                    if time_x[1] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

            # right
            elif time_x_bool != False:
                time_x = solve(motion_x - 60, t)
                print(time_x)
                velocity_x = -velocity_x
                acceleration_x = -acceleration_x
                if time_x[0] > 0:
                    time = time - time_x[0]
                else:
                    time = time - time_x[1]

            # top
            elif time_y_bool != False:
                time_y = solve(motion_y - 40, t)
                print(time_y)
                velocity_y = -velocity_y
                acceleration_y = -acceleration_y
                if time_y[0] > 0:
                    time = time - time_y[0]
                else:
                    time = time - time_y[1]

            else:
                print("w tym przypadku już nie odbija się od żadnej ściany tylko zatrzymuje się w środku")
                time = 0

        '''bottom or right'''
        if velocity_x >= 0 and velocity_y < 0:
            time_x_bool = solve([t >= 0, t <= time, motion_x - 60], t)
            time_y_bool = solve([t >= 0, t <= time, motion_y - 0], t)
            print("\n", time_x_bool)
            print(time_y_bool)

            # bottom or right
            if time_x_bool != False and time_y_bool != False:
                time_x = solve(motion_x - 60, t)
                print(time_x)
                time_y = solve(motion_y - 0, t)
                print(time_y)

                if time_x[0] > 0 and time_y[0] > 0:

                    # right
                    if time_x[0] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] <= 0 and time_y[0] > 0:

                    # right
                    if time_x[1] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] > 0 and time_y[0] <= 0:

                    # right
                    if time_x[0] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

                elif time_x[0] <= 0 and time_y[0] <= 0:

                    # right
                    if time_x[1] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

            # right
            elif time_x_bool != False:
                time_x = solve(motion_x - 60, t)
                print(time_x)
                velocity_x = -velocity_x
                acceleration_x = -acceleration_x
                if time_x[0] > 0:
                    time = time - time_x[0]
                else:
                    time = time - time_x[1]

            # bottom
            elif time_y_bool != False:
                time_y = solve(motion_y - 0, t)
                print(time_y)
                velocity_y = -velocity_y
                acceleration_y = -acceleration_y
                if time_y[0] > 0:
                    time = time - time_y[0]
                else:
                    time = time - time_y[1]

            else:
                print("w tym przypadku już nie odbija się od żadnej ściany tylko zatrzymuje się w środku")
                time = 0

        '''top or left'''
        if velocity_x < 0 and velocity_y >= 0:
            time_x_bool = solve([t >= 0, t <= time, motion_x - 0], t)
            time_y_bool = solve([t >= 0, t <= time, motion_y - 40], t)
            print("\n", time_x_bool)
            print(time_y_bool)

            # top or left
            if time_x_bool != False and time_y_bool != False:
                time_x = solve(motion_x - 0, t)
                print(time_x)
                time_y = solve(motion_y - 40, t)
                print(time_y)

                if time_x[0] > 0 and time_y[0] > 0:

                    # left
                    if time_x[0] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] <= 0 and time_y[0] > 0:

                    # left
                    if time_x[1] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] > 0 and time_y[0] <= 0:

                    # left
                    if time_x[0] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

                elif time_x[0] <= 0 and time_y[0] <= 0:

                    # left
                    if time_x[1] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # top
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

            # left
            elif time_x_bool != False:
                time_x = solve(motion_x - 0, t)
                print(time_x)
                velocity_x = -velocity_x
                acceleration_x = -acceleration_x
                if time_x[0] > 0:
                    time = time - time_x[0]
                else:
                    time = time - time_x[1]

            # top
            elif time_y_bool != False:
                time_y = solve(motion_y - 40, t)
                print(time_y)
                velocity_y = -velocity_y
                acceleration_y = -acceleration_y
                if time_y[0] > 0:
                    time = time - time_y[0]
                else:
                    time = time - time_y[1]

            else:
                print("w tym przypadku już nie odbija się od żadnej ściany tylko zatrzymuje się w środku")
                time = 0

        '''bottom or left'''
        if velocity_x < 0 and velocity_y < 0:
            time_x_bool = solve([t >= 0, t <= time, motion_x - 0], t)
            time_y_bool = solve([t >= 0, t <= time, motion_y - 0], t)
            print("\n", time_x_bool)
            print(time_y_bool)

            # bottom or left
            if time_x_bool != False and time_y_bool != False:
                time_x = solve(motion_x - 0, t)
                print(time_x)
                time_y = solve(motion_y - 0, t)
                print(time_y)

                if time_x[0] > 0 and time_y[0] > 0:

                    # left
                    if time_x[0] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] <= 0 and time_y[0] > 0:

                    # left
                    if time_x[1] < time_y[0]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[0]

                elif time_x[0] > 0 and time_y[0] <= 0:

                    # left
                    if time_x[0] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[0]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

                elif time_x[0] <= 0 and time_y[0] <= 0:

                    # left
                    if time_x[1] < time_y[1]:
                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        time = time - time_x[1]

                    # bottom
                    else:
                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y
                        time = time - time_y[1]

            # left
            elif time_x_bool != False:
                time_x = solve(motion_x - 0, t)
                print(time_x)
                velocity_x = -velocity_x
                acceleration_x = -acceleration_x
                if time_x[0] > 0:
                    time = time - time_x[0]
                else:
                    time = time - time_x[1]

            # bottom
            elif time_y_bool != False:
                time_y = solve(motion_y - 0, t)
                print(time_y)
                velocity_y = -velocity_y
                acceleration_y = -acceleration_y
                if time_y[0] > 0:
                    time = time - time_y[0]
                else:
                    time = time - time_y[1]

            else:
                print("w tym przypadku już nie odbija się od żadnej ściany tylko zatrzymuje się w środku")
                time = 0

    ''' plotting '''

    rink_width = np.linspace(0, 60)
    rink_height1 = np.linspace(0, 19.5)
    rink_height2 = np.linspace(20.5, 40)

    vlines(0, ymin=0, ymax=19.5)
    vlines(60, ymin=0, ymax=19.5)
    vlines(0, ymin=20.5, ymax=40)
    vlines(60, ymin=20.5, ymax=40)
    hlines(0, xmin=0, xmax=60)
    hlines(40, xmin=0, xmax=60)

    plot(starting_x, starting_y, 'ok', label='starting point')

    legend(loc='best')
    xlim(-5, 65)
    ylim(-5, 45)
    title(f"Hockey Puck No.: {i + 1}")
    savefig(f"{i + 1}.png")
    show()

    ''' output '''
    #outputfile.write(f"({round(hit_x,2)}, {round(hit_y,2)}); {round(maximum_height,2)}; [{round(vx1,2)}, "
     #                f"{round(vy1,2)}]; [{round(vx2,2)}, {round(vy2,2)}]; [{round(vx3,2)}, {round(vy3,2)}]; {hit} \n")

output_file.close()