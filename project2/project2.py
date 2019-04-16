from matplotlib.pyplot import xlim, plot, vlines, legend, savefig, show, hlines, title, ylim
import numpy as np
import math
from math import fabs
from sympy.solvers import solve
from sympy import Symbol

num_lines = sum(1 for line in open("input.txt"))
with open("input.txt") as input_file:
    lines = input_file.readlines()
output_file = open("output.txt", 'w')

for i in range(0, num_lines):

    data = lines[i].strip().split(';')

    ''' starting position '''
    starting_position = data[0].strip()[1:-1].split(',')
    current_x = float(starting_position[0])
    current_y = float(starting_position[1])
    starting_x = current_x
    starting_y = current_y

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
    time = round(velocity / acceleration,2)
    total_time = time

    ''' starting conditions '''

    plot(current_x, current_y, 'or', markersize=8,  label='starting point', zorder=100)

    lista = []
    out = False
    end = False

    distance_x_max = velocity_x * time - 0.5 * acceleration_x * time * time
    distance_y_max = velocity_y * time - 0.5 * acceleration_y * time * time

    if velocity_x > 0:
        right = True
        left = False
    elif velocity_x < 0:
        right = False
        left = True
    else:
        right = False
        left = False

    if velocity_y > 0:
        top = True
        down = False
    elif velocity_y < 0:
        top = False
        down = True
    else:
        top = False
        down = False

    t = Symbol('t')

    # main loop
    while distance_y_max > 0 or distance_x_max > 0:

        previous_x = current_x
        previous_y = current_y

        if right:

            if top:

                if distance_x_max >= (60 - current_x - radius) and distance_y_max >= (40 - current_y - radius):

                    # krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej
                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius + current_x - 60, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius + current_y - 40, t)

                    if solution_x_time[0] == complex or solution_x_time[0]==0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0]==0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    if time_x_needed <= time_y_needed:

                        # szybicej uderzy w prawą ścianę
                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                        if current_y < 20.5 and current_y > 19.5:
                            out = True
                            distance_y_max = 0
                            distance_x_max = 0

                        else:

                            distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                            distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                            time -= time_x_needed

                            velocity_x -= acceleration_x * time_x_needed
                            velocity_y -= acceleration_y * time_x_needed

                            velocity_x = -velocity_x
                            acceleration_x = -acceleration_x
                            right = False
                            left = True

                    else:
                        # szybicej uderzy w górną ścianę

                        current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                        current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                        distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                        distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                        time -= time_y_needed

                        velocity_x -= acceleration_x * time_y_needed
                        velocity_y -= acceleration_y * time_y_needed

                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y

                        top = False
                        down = True

                elif distance_x_max >= (60 - current_x - radius):
                    # uderzy w ścianę prawą

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius + current_x - 60, t)

                    if solution_x_time[0] == complex or solution_x_time[0]==0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    if current_y < 20.5 and current_y > 19.5:
                        out = True
                        distance_y_max = 0
                        distance_x_max = 0
                    else:

                        distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                        distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                        time -= time_x_needed

                        velocity_x -= acceleration_x * time_x_needed
                        velocity_y -= acceleration_y * time_x_needed

                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        right = False
                        left = True

                elif distance_y_max >= (40 - current_y - radius):
                    # uderzy w ścianę gorna

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius + current_y - 40, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                    distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                    distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                    time -= time_y_needed

                    velocity_x -= acceleration_x * time_y_needed
                    velocity_y -= acceleration_y * time_y_needed

                    velocity_y = -velocity_y
                    acceleration_y = -acceleration_y
                    top = False
                    down = True

                else:
                    # zatrzyma się w środku

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                    end = True

            elif down:

                if distance_x_max >= (60 - current_x - radius) and distance_y_max >= (current_y - radius):
                    # krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius + current_x - 60, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius - current_y, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    if time_x_needed <= time_y_needed:
                        # szybicej uderzy w prawą ścianę

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                        if current_y < 20.5 and current_y > 19.5:
                            out = True
                            distance_y_max = 0
                            distance_x_max = 0
                        else:
                            distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                            distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                            time -= time_x_needed

                            velocity_x -= acceleration_x * time_x_needed
                            velocity_y -= acceleration_y * time_x_needed

                            velocity_x = -velocity_x
                            acceleration_x = -acceleration_x
                            right = False
                            left = True

                    else:
                        # szybicej uderzy w dolna ścianę

                        current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                        current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                        distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                        distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                        time -= time_y_needed

                        velocity_x -= acceleration_x * time_y_needed
                        velocity_y -= acceleration_y * time_y_needed

                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y

                        down = False
                        top = True

                elif distance_x_max >= (60 - current_x - radius):
                    # uderzy w ścianę prawą

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius + current_x - 60, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    if current_y < 20.5 and current_y > 19.5:
                        out = True
                        distance_y_max = 0
                        distance_x_max = 0

                    else:

                        distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                        distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                        time -= time_x_needed

                        velocity_x -= acceleration_x * time_x_needed
                        velocity_y -= acceleration_y * time_x_needed

                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        right = False
                        left = True

                elif distance_y_max >= (current_y - radius):
                    # uderzy w ścianę dolna

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius - current_y, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = fabs(round(current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed,2))

                    distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                    distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                    time -= time_y_needed

                    velocity_x -= acceleration_x * time_y_needed
                    velocity_y -= acceleration_y * time_y_needed

                    velocity_y = -velocity_y
                    acceleration_y = -acceleration_y
                    down = False
                    top = True

                else:
                    # zatrzyma się w środku

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                    end = True

        elif left:

            if top:

                if distance_x_max >= (current_x - radius) and distance_y_max >= (40 - current_y - radius):
                    # krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius - current_x, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius + current_y - 40, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    # previous_x = current_x
                    # previous_y = current_y

                    if time_x_needed <= time_y_needed:
                        # szybicej uderzy w lewa ścianę

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                        if current_y < 20.5 and current_y > 19.5:
                            out = True
                            distance_y_max = 0
                            distance_x_max = 0

                        else:

                            distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                            distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                            time -= time_x_needed

                            velocity_x -= acceleration_x * time_x_needed
                            velocity_y -= acceleration_y * time_x_needed

                            velocity_x = -velocity_x
                            acceleration_x = -acceleration_x
                            left = False
                            right = True

                    else:
                        # szybicej uderzy w górną ścianę

                        current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                        current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                        distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                        distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                        time -= time_y_needed

                        velocity_x -= acceleration_x * time_y_needed
                        velocity_y -= acceleration_y * time_y_needed

                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y

                        top = False
                        down = True

                elif distance_x_max >= (current_x - radius):
                    # uderzy w ścianę lewa

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius - current_x, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    if current_y < 20.5 and current_y > 19.5:
                        out = True
                        distance_y_max = 0
                        distance_x_max = 0

                    else:

                        distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                        distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                        time -= time_x_needed

                        velocity_x -= acceleration_x * time_x_needed
                        velocity_y -= acceleration_y * time_x_needed

                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        left = False
                        right = True

                elif distance_y_max >= 40 - current_y - radius:
                    # uderzy w ścianę gorna

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius + current_y - 40, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                    distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                    distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                    time -= time_y_needed

                    velocity_x -= acceleration_x * time_y_needed
                    velocity_y -= acceleration_y * time_y_needed

                    velocity_y = -velocity_y
                    acceleration_y = -acceleration_y
                    top = False
                    down = True

                else:
                    # zatrzyma się w środku

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                    end = True

            elif down:

                if distance_x_max >= (current_x - radius) and distance_y_max >= (current_y - radius):
                    # krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius - current_x, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius - current_y, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    if time_x_needed <= time_y_needed:
                        # szybicej uderzy w lewa ścianę

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                        if current_y < 20.5 and current_y > 19.5:
                            out = True
                            distance_y_max = 0
                            distance_x_max = 0

                        else:

                            distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                            distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                            time -= time_x_needed

                            velocity_x -= acceleration_x * time_x_needed
                            velocity_y -= acceleration_y * time_x_needed

                            velocity_x = -velocity_x
                            acceleration_x = -acceleration_x
                            left = False
                            right = True

                    else:
                        # szybicej uderzy w dolna ścianę

                        current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                        current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                        distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                        distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                        time -= time_y_needed

                        velocity_x -= acceleration_x * time_y_needed
                        velocity_y -= acceleration_y * time_y_needed

                        velocity_y = -velocity_y
                        acceleration_y = -acceleration_y

                        down = False
                        top = True

                elif distance_x_max >= (current_x - radius):
                    # uderzy w ścianę lewa

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + radius - current_x, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    if current_y < 20.5 and current_y > 19.5:
                        out = True
                        distance_y_max = 0
                        distance_x_max = 0

                    else:

                        distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                        distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                        time -= time_x_needed

                        velocity_x -= acceleration_x * time_x_needed
                        velocity_y -= acceleration_y * time_x_needed

                        velocity_x = -velocity_x
                        acceleration_x = -acceleration_x
                        left = False
                        right = True

                elif distance_y_max >= (current_y - radius):
                    # uderzy w ścianę dolna

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + radius - current_y, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                    distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                    distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed

                    time -= time_y_needed

                    velocity_x -= acceleration_x * time_y_needed
                    velocity_y -= acceleration_y * time_y_needed

                    velocity_y = -velocity_y
                    acceleration_y = -acceleration_y
                    down = False
                    top = True

                else:
                    # zatrzyma się w środku

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                    end = True

        # rysuję drogę oraz punkt uderzenia

        plot([previous_x, current_x], [previous_y, current_y], 'k-', linewidth=3)

        if not out:
            plot(current_x, current_y, 'ok', markersize=5)

        if not end and not out:
            lista.append(round(current_x, 2))
            lista.append(round(current_y, 2))

    if out:
        output_file.write(f"(out); {round(total_time, 2)}; ")
    else:
        output_file.write(f"({round(current_x, 2)}, {round(current_y, 2)}); {round(total_time,2)}; ")

    for j in range (0, len(lista), 2):
        output_file.write(f"({lista[j]}, {lista[j+1]}); ")

    output_file.write("\n")

    if not out:

        if previous_x != starting_x and previous_y != starting_y:
            plot(current_x, current_y, 'ok', markersize=6, label='bounce points')

        plot(current_x, current_y, 'ob', markersize=8, label='end point')

    else:
        plot(previous_x, previous_y, 'ok', markersize=6, label='bounce points')

    rink_width = np.linspace(0, 60)
    rink_height1 = np.linspace(0, 19.5)
    rink_height2 = np.linspace(20.5, 40)

    vlines(0, ymin=0, ymax=19.5)
    vlines(60, ymin=0, ymax=19.5)
    vlines(0, ymin=20.5, ymax=40)
    vlines(60, ymin=20.5, ymax=40)
    hlines(0, xmin=0, xmax=60)
    hlines(40, xmin=0, xmax=60)

    legend(loc='best')
    xlim(-5, 65)
    ylim(-5, 45)
    title(f"Hockey Puck No.: {i + 1}")
    savefig(f"{i + 1}.png")
    show()

output_file.close()
