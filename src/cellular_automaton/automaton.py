import numpy as np
import copy 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import colors


class Node:
    def __init__(self, x:float, y:float, cov_radius: float):
        self.x = x
        self.y = y
        self.cov_radius = cov_radius

    def update(self, width: float , height: float, change_probability:float):
        x_old = self.x
        y_old = self.y

        # С вероятностью P пытаемся переместить узел
        if random.random() < change_probability:

            # Выбираем случайное направление
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            dx, dy = random.choice(directions)
            
            new_x, new_y = x_old + dx, y_old + dy
                
            # Проверяем, что новая позиция в пределах поля и свободна
            if 0 <= new_x < width and 0 <= new_y < height:

                # Меняем положение узла
                self.x = new_x
                self.y = new_y
    
class NodeStructure:
    def __init__(self, init_coordinates: np.array, cov_radius: float, change_probability:float):
        nodes = []

        if init_coordinates.size != 0:
            for x,y in init_coordinates:
                curr_Node = Node(x = x, y = y, cov_radius=float)
                nodes.append(curr_Node)

        self.cov_radius = cov_radius
        self.change_probablity = change_probability
        self.nodes = nodes

    @property
    def node_count(self):
        return self.nodes.size
    
    def update(self, width: float , height: float):
        nodes = copy.deepcopy(self.nodes)
        for node in nodes:
            node.update(width = width, 
                        height = height,
                        change_probability = self.change_probablity)
        
        self.nodes = nodes

class CellularAutomaton:
    def __init__(self, width: float, height: float, node_structure: NodeStructure):
        self.width = width
        self.height = height
        self.node_structure = node_structure
        self.grid = []
        
    def initialize_grid(self, width, height):

        # Инициализация начальной сетки
        grid = np.zeros((width, height), dtype=int)
        
        # Расстановка аппаратов
        for node in self.node_structure.nodes:
            if 0 <= node.x < width and 0 <= node.y < height:
                grid[node.x, node.y] = 1
        return grid
    
    def update(self):

        new_grid = self.grid.copy()

        self.node_structure.update(self.width, self.height)
        
        # Расстановка аппаратов
        for node in self.node_structure.nodes:
            if 0 <= node.x < self.width and 0 <= node.y < self.height:
                new_grid[node.x, node.y] = 1

        self.grid = new_grid
        return self.grid
    
    def animate(self, frames=1000, interval=50):
        fig, ax = plt.subplots(figsize=(10, 10))
        
        cmap = colors.ListedColormap(['black', 'white'])
        bounds = [0, 1, 2]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        
        img = ax.imshow(self.grid, cmap=cmap, norm=norm, interpolation='nearest')
        ax.set_title('Cellular Automaton')
        ax.set_axis_off()

        def animate(frame):
            self.update()
            img.set_array(self.grid)
            return [img]

        ani = animation.FuncAnimation(
            fig, animate, frames=frames, interval=interval, blit=True
        )
        plt.tight_layout()
        plt.show()
