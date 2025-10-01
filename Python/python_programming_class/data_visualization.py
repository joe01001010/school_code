import numpy as np
import matplotlib.pyplot as plt


def sine_waves():
    x_points = np.linspace(0, 2 * np.pi)
    
    for i in range(1,4):
        y_points = np.sin(x_points * i)
        plt.plot(x_points, y_points)

    plt.show()


def multi_sine_waves():
    x_points = np.linspace(0, 2 * np.pi)
    
    for i in range(1,4):
        y_points = np.sin(x_points * i)
        plt.subplot(3,1,i)
        plt.plot(x_points, y_points)

    plt.show()


def chaos_plot():
    n = 1500
    x_points = np.random.rand(n, 2) * 2 - 1
    points_color = np.ones(n)

    set1 = np.where(x_points[:,0] >= 0)
    set2 = np.where(x_points[:,1] >= 0)
    points_color[np.intersect1d(set1, set2)] = 0

    set1 = np.where(x_points[:,0] < 0)
    set2 = np.where(x_points[:,1] < 0)
    points_color[np.intersect1d(set1, set2)] = 0
    
    plt.scatter(x_points[:,0], x_points[:,1], c = points_color)
    plt.show()


def main():
    sine_waves()
    multi_sine_waves()
    chaos_plot()



if __name__ == '__main__':
    main()