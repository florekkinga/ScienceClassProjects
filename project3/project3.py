import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# constant parameters
ball_radius = 0.030
ball_mass = 0.017
ball_friction = 0.015
kinetic_energy_loss = 0.300
pocket_diameter = 0.100
pool_table_length = 2.70
pool_table_width = 1.350
standard_gravity = 9.810
collisions_with_each_other = 0
deltat = 0.100


class BilliardBall(object):

    def __init__(self, starting_x, starting_y, velocity_x, velocity_y):
        self.starting_x = round(starting_x, 3)
        self.starting_y = round(starting_y, 3)
        self.previous_x = round(starting_x,3)
        self.previous_y = round(starting_y,3)
        self.current_x = round(starting_x, 3)
        self.current_y = round(starting_y, 3)
        self.velocity_x = round(velocity_x, 3)
        self.velocity_y = round(velocity_y, 3)
        self.velocity = math.sqrt(velocity_x*velocity_x + velocity_y*velocity_y)
        self.kinetic_energy_x = round(0.5 * ball_mass * self.velocity_x, 3)
        self.kinetic_energy_y = round(0.5 * ball_mass * self.velocity_y, 3)
        if velocity_x != 0 and velocity_y != 0:
            acceleration = round(ball_friction * standard_gravity, 3)
            self.acceleration_x = round(acceleration * velocity_x / self.velocity, 3)
            self.acceleration_y = round(acceleration * velocity_y / self.velocity, 3)
        else:
            self.acceleration_x = 0
            self.acceleration_y = 0
        self.collision_with_band = 0
        self.score_foul = False

    def velocity_after_energy_loss(self):
        if self.velocity_x > 0:
            self.velocity_x = round(math.sqrt(0.7 * math.fabs(self.kinetic_energy_x) * 2 / ball_mass), 3)
        else:
            self.velocity_x = -round(math.sqrt(0.7 * math.fabs(self.kinetic_energy_x) * 2 / ball_mass), 3)

        if self.velocity_y > 0:
            self.velocity_y = round(math.sqrt(0.7 * math.fabs(self.kinetic_energy_y) * 2 / ball_mass), 3)
        else:
            self.velocity_y = -round(math.sqrt(0.7 * math.fabs(self.kinetic_energy_y) * 2 / ball_mass), 3)

        self.velocity = math.sqrt(self.velocity_x*self.velocity_x + self.velocity_y*self.velocity_y)

        '''if self.velocity_x < 0:
            self.acceleration_x = fabs(self.acceleration_x)
        else:
            self.acceleration_x = -fabs(self.acceleration_x)

        if self.velocity_y < 0:
            self.acceleration_y = fabs(self.acceleration_y)
        else:
            self.acceleration_y = -fabs(self.acceleration_y)'''

    def kinetic_energy_loss(self):
        self.kinetic_energy_x = round(0.7 * self.kinetic_energy_x, 3)
        self.kinetic_energy_y = round(0.7 * self.kinetic_energy_y, 3)

    def velocity_change(self):
        if self.velocity_x > 0:
            self.velocity_x -= round(math.fabs(self.acceleration_x) * deltat, 3)
        else:
            self.velocity_x += round(math.fabs(self.acceleration_x) * deltat, 3)
        if self.velocity_y > 0:
            self.velocity_y -= round(math.fabs(self.acceleration_y) * deltat, 3)
        else:
            self.velocity_y += round(math.fabs(self.acceleration_y) * deltat, 3)

        self.kinetic_energy_x = round(0.5 * ball_mass * self.velocity_x, 3)
        self.kinetic_energy_y = round(0.5 * ball_mass * self.velocity_y, 3)

        self.velocity = math.sqrt(self.velocity_x*self.velocity_x + self.velocity_y*self.velocity_y)

    def current_position(self):
        self.current_x += round(self.velocity_x * deltat - 0.5 * self.acceleration_x * deltat * deltat, 3)
        self.current_y += round(self.velocity_y * deltat - 0.5 * self.acceleration_y * deltat * deltat, 3)

    def get_velocity(self):
        return round(self.velocity_x, 3), round(self.velocity_y, 3)

    def set_velocity(self, velocity_x, velocity_y):
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def set_starting_point(self, starting_x, starting_y):
        self.starting_x = round(starting_x, 3)
        self.starting_y = round(starting_y, 3)


def swap_velocities(white_ball, colored_ball):
    white_velocity = white_ball.get_velocity()
    colored_velocity = colored_ball.get_velocity()
    white_ball.set_velocity(colored_velocity[0], colored_velocity[1])
    colored_ball.set_velocity(white_velocity[0], white_velocity[1])
    white_kinetic_x = white_ball.kinetic_energy_x
    white_kinetic_y = white_ball.kinetic_energy_y
    colored_kinetic_x = colored_ball.kinetic_energy_x
    colored_kinetic_y = colored_ball.kinetic_energy_y
    white_ball.kinetic_energy_x = colored_kinetic_x
    white_ball.kinetic_energy_y = colored_kinetic_y
    colored_ball.kinetic_energy_x = white_kinetic_x
    colored_ball.kinetic_energy_y = white_kinetic_y
    colored_acc_x = colored_ball.acceleration_x
    colored_acc_y = colored_ball.acceleration_y
    white_acc_x = white_ball.acceleration_x
    white_acc_y = white_ball.acceleration_y

    if white_ball.velocity_x < 0:
        white_ball.acceleration_x = colored_acc_x
    else:
        white_ball.acceleration_x = -colored_acc_x

    if white_ball.velocity_y < 0:
        white_ball.acceleration_y = colored_acc_y
    else:
        white_ball.acceleration_y = -colored_acc_y

    if colored_ball.velocity_x <0:
        colored_ball.acceleration_x = white_acc_x
    else:
        colored_ball.acceleration_x = -white_acc_x

    if colored_ball.velocity_y <0:
        colored_ball.acceleration_y = white_acc_y
    else:
        colored_ball.acceleration_y = -white_acc_y

def distance(first_x, first_y, second_x, second_y):
    return round(math.hypot(second_x - first_x, second_y - first_y), 3)


def deltat_incrementation(white_ball, colored_ball):
    white_ball.velocity_change()
    print("ok")
    colored_ball.velocity_change()
    white_ball.kinetic_energy_x = round(0.5 * ball_mass * white_ball.velocity_x, 3)
    white_ball.kinetic_energy_y = round(0.5 * ball_mass * white_ball.velocity_y, 3)
    colored_ball.kinetic_energy_x = round(0.5 * ball_mass * colored_ball.velocity_x, 3)
    colored_ball.kinetic_energy_y = round(0.5 * ball_mass * colored_ball.velocity_y, 3)
    white_ball.current_position()
    colored_ball.current_position()


def plot_line(ball):

    pass
    #plt.plot([ball.starting_x, ball.current_x], [ball.starting_y, ball.current_y], color='blue')
    #ball.set_starting_point(ball.current_x, ball.current_y)


def ball_in_pocket(ball):
    if distance(ball.current_x, ball.current_y, 0, 0) <= (pocket_diameter / 2 - ball_radius) or \
            distance(ball.current_x, ball.current_y, 0, pool_table_width) <= (pocket_diameter / 2 - ball_radius) or \
            distance(ball.current_x, ball.current_y, pool_table_length / 2, 0) <= (pocket_diameter / 2 - ball_radius) or \
            distance(ball.current_x, ball.current_y, pool_table_length / 2, pool_table_width) <= (
            pocket_diameter / 2 - ball_radius) or \
            distance(ball.current_x, ball.current_y, pool_table_length, 0) <= (pocket_diameter / 2 - ball_radius) or \
            distance(ball.current_x, ball.current_y, pool_table_length, pool_table_width) <= (
            pocket_diameter / 2 - ball_radius):
        return True
    else:
        return False


def hit_the_band_bool(ball):
    if -0.03 <= ball.current_x <= ball_radius + 0.03 or pool_table_length - ball_radius - 0.03 <= ball.current_x == pool_table_length - ball_radius + 0.03:
        return True

    elif -0.03 <= ball.current_y <= ball_radius + 0.03 or pool_table_width - ball_radius - 0.03 <= ball.current_y <= pool_table_width - ball_radius + 0.03:
        return True

    else:
        return False


def hit_the_band(ball):
    if -0.03 <= ball.current_x <= ball_radius + 0.03 or pool_table_length - ball_radius - 0.03 <= ball.current_x == pool_table_length - ball_radius + 0.03:
        ball.set_velocity(-ball.velocity_x, ball.velocity_y)
        print(ball.velocity_x, ball.velocity_y)

    elif -0.03 <= ball.current_y <= ball_radius + 0.03 or pool_table_width - ball_radius - 0.03 <= ball.current_y <= pool_table_width - ball_radius + 0.03:
        ball.set_velocity(ball.velocity_x, -ball.velocity_y)
        print(ball.velocity_x, ball.velocity_y)

    '''if ball.velocity_x < 0:
        ball.acceleration_x = fabs(ball.acceleration_x)
    else:
        ball.acceleration_x = -fabs(ball.acceleration_x)

    if ball.velocity_y < 0:
        ball.acceleration_y = fabs(ball.acceleration_y)
    else:
        ball.acceleration_y = -fabs(ball.acceleration_y)
'''


num_lines = sum(1 for line in open("input.txt"))
with open("input.txt") as input_file:
    lines = input_file.readlines()
output_file = open("output.txt", 'w')

# main loop
for i in range(0, num_lines):

    fig, ax = plt.subplots(1)

    data = lines[i].strip().split(';')

    starting_position_white = data[0].strip()[1:-1].split(',')
    starting_x_white = float(starting_position_white[0])
    starting_y_white = float(starting_position_white[1])

    velocity_vector_white = data[1].strip()[1:-1].split(',')
    velocity_x_white = float(velocity_vector_white[0])
    velocity_y_white = float(velocity_vector_white[1])

    # creating a white ball
    white_ball = BilliardBall(starting_x_white, starting_y_white, velocity_x_white, velocity_y_white)
    plt.plot(white_ball.starting_x, white_ball.starting_y, 'ow', markersize=10, label='white ball starting point',
             zorder=10)

    starting_position_colored = data[2].strip()[1:-1].split(',')
    starting_x_colored = float(starting_position_colored[0])
    starting_y_colored = float(starting_position_colored[1])

    # creating a colored ball
    colored_ball = BilliardBall(starting_x_colored, starting_y_colored, 0, 0)
    plt.plot(colored_ball.starting_x, colored_ball.starting_y, 'o', color='#f3cd3d', markersize=10,
             label='colored ball starting point', zorder=10)

    while (((white_ball.velocity_x >= 0.05 or white_ball.velocity_x <= -0.05) and (
            white_ball.velocity_y >= 0.05 or white_ball.velocity_y <= -0.05)) or (
                   (colored_ball.velocity_x >= 0.05 or colored_ball.velocity_x <= -0.05) and (
                   colored_ball.velocity_y >= 0.05 or colored_ball.velocity_y <= -0.05))) and not white_ball.score_foul and not colored_ball.score_foul:

        # pierwszy warunek na to czy wpadła już kolorowa bila (jeśli tak, to wtedy sprawdzamy tylko tor ruchu białej),
        # tak samo gdy wpadła biała to trzeba sprawdzić gdzie zatrzyma sie kolorowa wiec osobne dwa while?
        if not colored_ball.score_foul:

            print("czy biała bila wpadnie do łuzy?")
            if ball_in_pocket(white_ball):
                print("tak, biała bila wpadnie do łuzy FOUL")
                white_ball.score_foul = True
                plot_line(white_ball)

                print("czy kolorowa bila też wpadnie do łuzy?")
                if ball_in_pocket(colored_ball):
                    print("tak, kolorowa też wpadnie do łuzy FOUL / SCORE")
                    colored_ball.score_foul = True
                    plot_line(colored_ball)
            else:
                print("czy kolorowa bila wpadnie do łuzy?")
                if ball_in_pocket(colored_ball):
                    print("tak, kolorowa wpadnie do łuzy SCORE")
                    colored_ball.score_foul = True
                    plot_line(colored_ball)

                else:
                    print("czy kule się zderzą?")
                    if distance(white_ball.current_x, white_ball.current_y, colored_ball.current_x,
                                colored_ball.current_y) < 2 * ball_radius:
                        swap_velocities(white_ball, colored_ball)
                        collisions_with_each_other += 1
                        print("kule sie zderzyly, zamiana predkosci i N1++")
                        plot_line(colored_ball)
                        plot_line(white_ball)

                    else:
                        print("czy obie kule uderzą w ścianę?")
                        if hit_the_band_bool(colored_ball) and hit_the_band_bool(white_ball):
                            hit_the_band(colored_ball)
                            hit_the_band(white_ball)
                            colored_ball.velocity_after_energy_loss()
                            colored_ball.kinetic_energy_loss()
                            white_ball.velocity_after_energy_loss()
                            white_ball.kinetic_energy_loss()
                            colored_ball.collision_with_band += 1
                            white_ball.collision_with_band += 1
                            print("obydwie kule uderza w sciane")
                            plot_line(colored_ball)
                            plot_line(white_ball)

                        else:
                            print("czy tylko biala kula uderzy w sciane?")
                            if hit_the_band_bool(white_ball):
                                hit_the_band(white_ball)
                                white_ball.velocity_after_energy_loss()
                                white_ball.kinetic_energy_loss()
                                white_ball.collision_with_band += 1
                                print("biala kula uderzy w sciane!")
                                plot_line(white_ball)

                            else:
                                print("czy tylko kolorowa kula uderzy w sciane?")
                                if hit_the_band_bool(colored_ball):
                                    hit_the_band(colored_ball)
                                    colored_ball.velocity_after_energy_loss()
                                    colored_ball.kinetic_energy_loss()
                                    colored_ball.collision_with_band += 1
                                    print("kolorowa kula uderzy w sciane lol")
                                    plot_line(colored_ball)

        print("predkosc bialej ")
        print(white_ball.velocity_x, white_ball.velocity_y)
        print("energia kinetyczna bialej")
        print(white_ball.kinetic_energy_x, white_ball.kinetic_energy_y)
        deltat_incrementation(white_ball, colored_ball)
        print("predkosc bialej po deltat incrr")
        print(white_ball.velocity_x, white_ball.velocity_y)
        print("wspolrzedne białej")
        print(white_ball.current_x, white_ball.current_y)
        print("wsporzedne kolorowej")
        print(colored_ball.current_x, colored_ball.current_y)
        print("predkosc kolorowej")
        print(colored_ball.velocity_x, colored_ball.velocity_y)

        plt.plot([white_ball.previous_x, white_ball.current_x], [white_ball.previous_y, white_ball.current_y], color = "white")
        white_ball.previous_x = white_ball.current_x
        white_ball.previous_y = white_ball.current_y
        plt.plot([colored_ball.previous_x, colored_ball.current_x], [colored_ball.previous_y, colored_ball.current_y], color = "#f3cd3d")
        colored_ball.previous_x = colored_ball.current_x
        colored_ball.previous_y = colored_ball.current_y
        #plt.plot(white_ball.current_x, white_ball.current_y, 'om')
        #plt.plot(colored_ball.current_x, colored_ball.current_y, 'or')

    # plotting

    # pockets
    plt.plot(0, 0, 'ok', markersize=15, label='pocket', zorder=10)
    plt.plot(0, pool_table_width, 'ok', markersize=15, zorder=10)
    plt.plot(pool_table_length / 2, 0, 'ok', markersize=15, zorder=10)
    plt.plot(pool_table_length / 2, pool_table_width, 'ok', markersize=15, zorder=10)
    plt.plot(pool_table_length, 0, 'ok', markersize=15, zorder=10)
    plt.plot(pool_table_length, pool_table_width, 'ok', markersize=15, zorder=10)

    plt.plot([0, pool_table_length], [0, 0], color="#1c1c1c", linewidth=4)
    plt.plot([0, pool_table_length], [pool_table_width, pool_table_width], color="#1c1c1c", linewidth=4)
    plt.plot([0, 0], [pocket_diameter / 2, pool_table_width - pocket_diameter / 2], color="#1c1c1c", linewidth=4)
    plt.plot([pool_table_length, pool_table_length], [pocket_diameter / 2, pool_table_width - pocket_diameter / 2],
             color="#1c1c1c", linewidth=4)

    rect = patches.Rectangle((0, 0), pool_table_length, pool_table_width, edgecolor='#127e5c', facecolor='#127e5c')
    ax.add_patch(rect)

    plt.xlim(-0.2, pool_table_length + 0.2)
    plt.ylim(-0.2, 2)

    plt.legend(loc='upper center', facecolor='#127e5c', edgecolor='black')
    plt.title(f"Billiard Table No.: {i + 1}")
    plt.savefig(f"{i + 1}.png")
    plt.show()

    if not white_ball.score_foul and not colored_ball.score_foul:
        output_file.write(f"({round(white_ball.current_x,3)}, {round(white_ball.current_y,3)}); ({round(colored_ball.current_x,3)}, {round(colored_ball.current_y,3)}); {collisions_with_each_other}; {white_ball.collision_with_band}; {colored_ball.collision_with_band} \n")
    elif white_ball.score_foul and colored_ball.score_foul:
        output_file.write(f" (foul); (score); {collisions_with_each_other}; {white_ball.collision_with_band}; {colored_ball.collision_with_band} \n")
    elif white_ball.score_foul:
        output_file.write(f" ({round(white_ball.current_x,3)}, {round(white_ball.current_y,3)}); ({round(colored_ball.current_x,3)}, {round(colored_ball.current_y,3)}); {collisions_with_each_other}; {white_ball.collision_with_band}; {colored_ball.collision_with_band} \n")
    else:
        output_file.write(f" (foul); (score); {collisions_with_each_other}; {white_ball.collision_with_band}; {colored_ball.collision_with_band} \n")


output_file.close()
