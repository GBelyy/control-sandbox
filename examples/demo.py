import numpy as np
from src.cellular_automaton.automaton import CellularAutomaton, NodeStructure

def run_demo():

    init_coordinates = np.array([[25, 25, 30, 30], [25, 30, 25, 30]])
    nodes = NodeStructure(init_coordinates=init_coordinates, cov_radius=3, change_probability=0.3)
    automaton = CellularAutomaton(width=50, height=50, node_structure=nodes)
    automaton.animate(frames=500, interval=50)

if __name__ == "__main__":
    run_demo()