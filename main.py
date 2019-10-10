import matplotlib.pyplot as plt
from Map import Map

if __name__ == '__main__':
    Map1 = Map(30, 20, (0,0))
    plt.imshow(Map1.map)
    plt.show()