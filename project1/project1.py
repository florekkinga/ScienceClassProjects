import matplotlib.pyplot as plt
import numpy as np
import math
from sympy.solvers import solve
from sympy import Symbol


def ParseFormula(terrain_str):
    sign = True
    cp = []
    cp.clear()
    for j in range(0, len(terrain_str)):
        if terrain_str[j] == '+':
            sign = True
        elif terrain_str[j] == '-':
            sign = False
        else:
            if sign:
                c = float(terrain_str[j].split('x^')[0])
                cp.append(c)
                if 'x^' in terrain_str[j]:
                    p = int(terrain_str[j].split('x^')[1])
                    cp.append(p)
                elif 'x' in terrain_str[j]:
                    p = 1
                    cp.append(p)
                else:
                    p = 0
                    cp.append(p)
            else:
                c = float(terrain_str[j].split('x^')[0])
                cp.append(-c)
                if 'x^' in terrain_str[j]:
                    p = int(terrain_str[j].split('x^')[1])
                    cp.append(p)
                elif 'x' in terrain_str[j]:
                    p = 1
                    cp.append(p)
                else:
                    p = 0
                    cp.append(p)
    return cp


# main loop

num_lines = sum(1 for line in open("input.txt"))
with open("input.txt") as f:
    lines = f.readlines()
outputfile = open("output.txt", 'w')

for i in range(0, num_lines):

    data = lines[i].strip().split(';')

    ''' starting position '''
    starting_position = data[0].strip()[1:-1].split(',')
    starting_x = float(starting_position[0])
    starting_y = float(starting_position[1])

    ''' target position '''
    target_position = data[1].strip()[1:-1].split(',')
    target_x = float(target_position[0])
    target_y = float(target_position[1])

    ''' velocity vector '''
    velocity_vector = data[2].strip()[1:-1].split(',')
    velocity_x = float(velocity_vector[0])
    velocity_y = float(velocity_vector[1])

    ''' wind vector '''
    wind_vector = data[3].strip()[1:-1].split(',')
    wind_x = float(wind_vector[0])
    wind_y = float(wind_vector[1])

    ''' times '''
    t1 = float(data[4])
    t2 = float(data[5])
    t3 = float(data[6])

    ''' function defining the terrain '''
    coeff_pow = ParseFormula(data[7].strip().split(' '))

    x = Symbol('x')  # used for equation
    f = 0  # used for equation
    for k in range(0, len(coeff_pow), 2):
        f += coeff_pow[k] * (x ** coeff_pow[k + 1])

    ''' main equation '''
    g = 10
    y = starting_y + (velocity_y + wind_y) * ((x - starting_x) / (velocity_x + wind_x)) \
        - ((g * ((x - starting_x) ** 2)) / (2 * ((velocity_x + wind_x) ** 2)))

    '''finding the hit point'''
    solution = solve(y - f, x)  # y = f  ==> y - f = 0
    hit_x = float(solution[1])  # solution[0] = starting_x, so hit_x ==> solution[1]
    hit_y = starting_y + (velocity_y + wind_y) * ((hit_x - starting_x) / (velocity_x + wind_x)) \
            - ((g * ((hit_x - starting_x) ** 2)) / (2 * ((velocity_x + wind_x) ** 2)))

    '''finding the trajectory of projectiles'''
    x_trajectory = np.linspace(starting_x, hit_x, 10000)  # range for trajectory plot
    trajectory = starting_y + (velocity_y + wind_y) * ((x_trajectory - starting_x) / (velocity_x + wind_x)) \
                 - ((g * ((x_trajectory - starting_x) ** 2)) / (2 * ((velocity_x + wind_x) ** 2)))

    '''finding the maximum height'''
    maximum_height = starting_y + (velocity_y + wind_y)**2 / (2*g)

    '''finding the velocity at t1, t2 and t3 '''
    if hit_x > (starting_x + (velocity_x + wind_x) * t1):
        vx1 = velocity_x + wind_x
        vy1 = velocity_y + wind_y - g*t1
    else:
        vx1 = 0.0
        vy1 = 0.0

    if hit_x > (starting_x + (velocity_x + wind_x) * t2):
        vx2 = velocity_x + wind_x
        vy2 = velocity_y + wind_y - g*t2
    else:
        vx2 = 0.0
        vy2 = 0.0

    if hit_x > (starting_x + (velocity_x +  wind_x) * t3):
        vx3 = velocity_x + wind_x
        vy3 = velocity_y + wind_y - g*t3
    else:
        vx3 = 0.0
        vy3 = 0.0

    '''hit or not hit'''
    hit = 0
    distance = math.hypot(target_x-hit_x, target_y-hit_y)
    if distance <= 0.05:
        hit = 1

    ''' plotting '''
    if target_x < hit_x:
        x_terrain = np.linspace(starting_x - 0.2, hit_x + 0.2, 10000)  # range for terrain plot
        terrain = 0
        for k in range(0, len(coeff_pow), 2):
            terrain += coeff_pow[k] * x_terrain ** coeff_pow[k + 1]
        plt.xlim(starting_x - 0.2, hit_x + 0.2)
    else:
        x_terrain = np.linspace(starting_x - 0.2, target_x + 0.2, 10000)  # range for terrain plot
        terrain = 0
        for k in range(0, len(coeff_pow), 2):
            terrain += coeff_pow[k] * x_terrain ** coeff_pow[k + 1]
        plt.xlim(starting_x - 0.2, target_x + 0.2)

    plt.plot(x_terrain, terrain, 'g')
    plt.plot(x_trajectory, trajectory, 'k', label='trajectory of a projectile')
    plt.fill_between(x_terrain, terrain, starting_y - 0.2, facecolor='#0aa979', label='terrain')

    plt.plot(starting_x, starting_y, 'ok', label='starting point')
    plt.plot(target_x, target_y, '*r', markersize=15, label='target point')
    plt.plot(hit_x, hit_y, 'Xk', markersize=11, label='hit point')

    plt.legend(loc='best')

    plt.ylim(bottom=starting_y - 0.2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f"Shot No.: {i+1}")
    plt.savefig(f"{i+1}.png")
    plt.show()

    ''' output '''
    outputfile.write(f"({round(hit_x,2)}, {round(hit_y,2)}); {round(maximum_height,2)}; [{round(vx1,2)}, "
                     f"{round(vy1,2)}]; [{round(vx2,2)}, {round(vy2,2)}]; [{round(vx3,2)}, {round(vy3,2)}]; {hit} \n")

outputfile.close()
