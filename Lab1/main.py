import numpy as np
import matplotlib.pyplot as plt

# Choose number of chords to draw in the simulation:
num_chords = 20_000
plot_limit = num_chords

def draw_circle_and_triangle(ax):
    circle = plt.Circle((0, 0), 1, color='w', linewidth=2, fill=False)
    ax.add_patch(circle)  # Draw circle
    ax.plot([np.cos(np.pi / 2), np.cos(7 * np.pi / 6)],
            [np.sin(np.pi / 2), np.sin(7 * np.pi / 6)], linewidth=2, color='g')
    ax.plot([np.cos(np.pi / 2), np.cos(- np.pi / 6)],
            [np.sin(np.pi / 2), np.sin(- np.pi / 6)], linewidth=2, color='g')
    ax.plot([np.cos(- np.pi / 6), np.cos(7 * np.pi / 6)],
            [np.sin(- np.pi / 6), np.sin(7 * np.pi / 6)], linewidth=2, color='g')
    plt.show()


def bertrand_simulation(method_number):
    # Simulation initialisation parameters
    count = 0    

    # Figure initialization
    plt.style.use('dark_background')  # use dark background
    ax = plt.gca()
    ax.cla()  # clear things for fresh plot
    ax.set_aspect('equal', 'box')
    ax.set_xlim((-1, 1))  # Set x axis limits
    ax.set_ylim((-1, 1))  # Set y axis limits

    # Repeat the following simulation num_chords times:
    for k in range(1, num_chords + 1):
        # Step 1: Construct chord according to chosen method
        a, b = bertrand_methods[method_number]()

        # Step 2: Compute length of chord and compare it with triangle side sqrt(3)
        length = np.sqrt(np.power(a[0] - b[0], 2) + np.power(a[1] - b[1], 2))
        if (k % 10) == 0:
            print(f"Probability = {(count / k):.4f}, {(k / num_chords) * 100:.2f}% done")  # Display probability after each simulation

        def plotline(a, b, col):
            if k <= plot_limit:
                plt.plot([a[0], b[0]], [a[1], b[1]], color=col, alpha=0.1)

        if length > np.sqrt(3):
            count += 1
            plotline(a, b, 'y')
        else:
            plotline(a, b, 'm')

    plt.suptitle(f"Method {method_number}\n{plot_limit} chords plotted, p = {(count / num_chords) * 100:.2f}%")
    draw_circle_and_triangle(plt.gca())
    plt.show()
    

def random_edge():
    theta = np.random.random() * 2 * np.pi
    return (np.cos(theta), np.sin(theta))

def bertrand1():
    """Generate random chords and midpoints using "Method 1".
    
    Pairs of (uniformly-distributed) random points on the unit circle are
    selected and joined as chords.
    
    """
    return (random_edge(), random_edge())

def random_point_1():
    rot = np.random.random() * 2 * np.pi
    dist = np.random.random()
    x = dist * np.sin(rot)
    y = dist * np.cos(rot)
    return (x, y)

def chord_from_center(center):
    (x_0, y_0) = center
    m = -(x_0/y_0)
    c = (np.power(x_0, 2) + np.power(y_0, 2)) / y_0
    A = np.power(m, 2) + 1
    B = 2 * m * c
    C = np.power(c, 2) - 1
    x_1 = (-B - np.sqrt(np.power(B, 2) - 4*A*C)) / (2 * A)
    x_2 = (-B + np.sqrt(np.power(B, 2) - 4*A*C)) / (2 * A)
    y_1 = m*x_1 + c
    y_2 = m*x_2 + c
    return ((x_1, y_1), (x_2, y_2))

def bertrand2():
    return chord_from_center(random_point_1())

bertrand_methods = {1: bertrand1, 2: bertrand2}

method_choice = int(input('Choose method to simulate: '))
bertrand_simulation(method_choice)

