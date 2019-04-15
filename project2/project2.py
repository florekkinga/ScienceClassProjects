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

    #current_x = starting_x
    #current_y = starting_y

    ''' mass '''
    mass = float(data[1])

    ''' radius '''
    radius = float(data[2])

    ''' coefficient of friction '''
    c_friction = float(data[3])

    ''' velocity '''
    velocity_vector = data[4].strip()[1:-1].split(',')
    velocity_x = float(velocity_vector[0])
    print(velocity_x)
    velocity_y = float(velocity_vector[1])
    print(velocity_y)

    ''' acceleration '''
    g = 10
    acceleration = c_friction * g
    alpha = math.atan(velocity_y / velocity_x)

    acceleration_x = math.cos(alpha) * acceleration
    acceleration_y = math.sin(alpha) * acceleration

    ''' total time '''
    velocity = math.sqrt(velocity_x * velocity_x + velocity_y * velocity_y)
    time = velocity / acceleration
    print(time)

    '''------------------------------------------------------------------------------------------------------'''

    plot(current_x, current_y, 'ok', markersize=10,  label='starting point')

    #time_x_max = velocity_x / acceleration_x
    #time_y_max = velocity_y / acceleration_y

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

    print("KOLEJNY KRĄŻEK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    while distance_y_max > 0 or distance_x_max > 0:
        print("xddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")

        if right:

            if top:

                if distance_x_max >= 60 - current_x and distance_y_max >= 40 - current_y:
                    print("krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej")

                    # liczę czas potrzebny aby uderzł w prawą i górną ścianę i porównuję
                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + current_x - 60, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + current_y - 40, t)

                    print(distance_x_max)
                    print(distance_y_max)

                    print(solution_x_time)
                    print(solution_y_time)

                    if solution_x_time[0] == complex or solution_x_time[0]==0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0]==0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    if time_x_needed <= time_y_needed:
                        print("szybicej uderzy w prawą ścianę (lub w prawy górny róg - do przemyslenia ten przypadek)")

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

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
                        print("szybicej uderzy w górną ścianę")

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

                elif distance_x_max >= 60 - current_x:
                    print("uderzy w ścianę prawą")

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + current_x - 60, t)

                    if solution_x_time[0] == complex or solution_x_time[0]==0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                    distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                    time -= time_x_needed

                    velocity_x -= acceleration_x * time_x_needed
                    velocity_y -= acceleration_y * time_x_needed

                    velocity_x = -velocity_x
                    acceleration_x = -acceleration_x
                    right = False
                    left = True

                elif distance_y_max >= 40 - current_y:
                    print("uderzy w ścianę gorna")

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + current_y - 40, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed

                    print(current_x)
                    print(current_y)

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
                    print("zatrzyma się w środku")

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                print("rysuję drogę oraz punkt uderzenia o tu ")
                plot([previous_x, current_x], [previous_y, current_y], 'm-', linewidth=3)
                plot(current_x, current_y, 'om', markersize=10, label='stop')

            elif down:

                if distance_x_max >= 60 - current_x and distance_y_max >= current_y:
                    print("krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej")

                    # liczę czas potrzebny aby uderzł w prawą i dolną ścianę i porównuję
                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + current_x - 60, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t - current_y, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    if time_x_needed <= time_y_needed:
                        print("szybicej uderzy w prawą ścianę (lub w prawy dolny róg - do przemyslenia ten przypadek)")

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

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
                        print("szybicej uderzy w dolna ścianę")

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

                elif distance_x_max >= 60 - current_x:
                    print("uderzy w ścianę prawą")

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t + current_x - 60, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                    distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                    time -= time_x_needed

                    velocity_x -= acceleration_x * time_x_needed
                    velocity_y -= acceleration_y * time_x_needed

                    velocity_x = -velocity_x
                    acceleration_x = -acceleration_x
                    right = False
                    left = True

                elif distance_y_max >= current_y:
                    print("uderzy w ścianę dolna!!!!")

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t - current_y, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    print(previous_x)
                    print(previous_y)

                    print(distance_y_max)
                    print(time_y_needed)
                    print(time)

                    current_x = current_x + velocity_x * time_y_needed - 0.5 * acceleration_x * time_y_needed * time_y_needed
                    current_y = fabs(round(current_y + velocity_y * time_y_needed - 0.5 * acceleration_y * time_y_needed * time_y_needed,2))

                    print(current_x)
                    print(round(current_y,2))

                    distance_x_max -= fabs(velocity_x) * time_y_needed - 0.5 * fabs(acceleration_x) * time_y_needed * time_y_needed
                    distance_y_max -= fabs(velocity_y) * time_y_needed - 0.5 * fabs(acceleration_y) * time_y_needed * time_y_needed
                    print(distance_y_max)

                    time -= time_y_needed

                    velocity_x -= acceleration_x * time_y_needed
                    velocity_y -= acceleration_y * time_y_needed

                    velocity_y = -velocity_y
                    acceleration_y = -acceleration_y
                    down = False
                    top = True

                else:
                    print("zatrzyma się w środku")

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                print("rysuję drogę oraz punkt uderzenia")
                plot([previous_x, current_x], [previous_y, current_y], 'm-', linewidth=3)
                plot(current_x, current_y, 'om', markersize=10, label='stop')

            '''else:
                # tylko prawo
                pass
                if distance_x_max > 60 - current_x:
                    print("poza lodowiskiem na współrzędnej x")

                    # liczę czas jaki potrzebuje krążek aby dotrzeć do ściany lodowiska
                    t = Symbol('t')
                    solution = solve(velocity_x * t - 0.5 * acceleration_x * t * t + current_x - 60, t)
                    if solution[0] == complex or solution[0] == 0:
                        time_x_needed = solution[1]
                    else:
                        time_x_needed = solution[0]

                    if time_x_needed > time_y_max:
                        print("zmiana kierunku ruchu w środku, prędkość po y spadła do 0")'''

        elif left:

            if top:

                if distance_x_max >= current_x and distance_y_max >= 40 - current_y:
                    print("krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej")

                    # liczę czas potrzebny aby uderzł w prawą i górną ścianę i porównuję
                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t - current_x, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + current_y - 40, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    if time_x_needed <= time_y_needed:
                        print("szybicej uderzy w lewa ścianę (lub w lewy górny róg - do przemyslenia ten przypadek)")

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

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
                        print("szybicej uderzy w górną ścianę")

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

                elif distance_x_max >= current_x:
                    print("uderzy w ścianę lewa")

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t - current_x, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                    distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                    time -= time_x_needed

                    velocity_x -= acceleration_x * time_x_needed
                    velocity_y -= acceleration_y * time_x_needed

                    velocity_x = -velocity_x
                    acceleration_x = -acceleration_x
                    left = False
                    right = True

                elif distance_y_max >= 40 - current_y:
                    print("uderzy w ścianę gorna")

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t + current_y - 40, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

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
                    print("zatrzyma się w środku")

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                print("rysuję drogę oraz punkt uderzenia")
                plot([previous_x, current_x], [previous_y, current_y], 'm-', linewidth=3)
                plot(current_x, current_y, 'om', markersize=10, label='stop')

            elif down:

                if distance_x_max >= current_x and distance_y_max >= current_y:
                    print("krążek na pewno wyjdzie poza lodowisko, nie wiadomo, w ktorą ściane uderzy szybciej")

                    # liczę czas potrzebny aby uderzł w prawą i dolną ścianę i porównuję
                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t - current_x, t)
                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t - current_y, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    if time_x_needed <= time_y_needed:
                        print("szybicej uderzy w lewa ścianę (lub w lewy dolny róg - do przemyslenia ten przypadek)")

                        current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                        current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

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
                        print("szybicej uderzy w dolna ścianę")

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

                elif distance_x_max >= current_x:
                    print("uderzy w ścianę lewa")

                    solution_x_time = solve(fabs(velocity_x) * t - 0.5 * fabs(acceleration_x) * t * t - current_x, t)

                    if solution_x_time[0] == complex or solution_x_time[0] == 0:
                        time_x_needed = solution_x_time[1]
                    else:
                        time_x_needed = solution_x_time[0]

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time_x_needed - 0.5 * acceleration_x * time_x_needed * time_x_needed
                    current_y = current_y + velocity_y * time_x_needed - 0.5 * acceleration_y * time_x_needed * time_x_needed

                    distance_x_max -= fabs(velocity_x) * time_x_needed - 0.5 * fabs(acceleration_x) * time_x_needed * time_x_needed
                    distance_y_max -= fabs(velocity_y) * time_x_needed - 0.5 * fabs(acceleration_y) * time_x_needed * time_x_needed

                    time -= time_x_needed

                    velocity_x -= acceleration_x * time_x_needed
                    velocity_y -= acceleration_y * time_x_needed

                    velocity_x = -velocity_x
                    acceleration_x = -acceleration_x
                    left = False
                    right = True

                elif distance_y_max >= current_y:
                    print("uderzy w ścianę dolna")

                    solution_y_time = solve(fabs(velocity_y) * t - 0.5 * fabs(acceleration_y) * t * t - current_y, t)

                    if solution_y_time[0] == complex or solution_y_time[0] == 0:
                        time_y_needed = solution_y_time[1]
                    else:
                        time_y_needed = solution_y_time[0]

                    previous_x = current_x
                    previous_y = current_y

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
                    print("zatrzyma się w środku")

                    previous_x = current_x
                    previous_y = current_y

                    current_x = current_x + velocity_x * time - 0.5 * acceleration_x * time * time
                    current_y = current_y + velocity_y * time - 0.5 * acceleration_y * time * time

                    distance_x_max = 0
                    distance_y_max = 0

                print("rysuję drogę oraz punkt uderzenia")
                plot([previous_x, current_x], [previous_y, current_y], 'm-', linewidth=3)
                plot(current_x, current_y, 'om', markersize=10, label='stop')

                '''else:
                # tylko lewo
                pass'''

        else:
            print("ERROR ------------- ")

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
