import random
import time
import math 
import matplotlib.pyplot as plt
import sys
import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
# Items and their weight
stock_status={
    1 : [[60, 4], [80, 3], [35, 1]],
    2 : [[12, 4], [45, 2], [25, 2]],
    3 : [[20, 2], [30, 1], [20, 3]],
    4 : [[30, 7], [10, 1]],
    5 : [[25, 2], [10, 10]]
}

# Neighbor matrix of path: {start point : {end point: [time, steps]}
neighbor_matrix={0 : {0 : [0, 0],
                      1 : [10, 10],
                      2 : [12, 12],
                      3 : [11, 11],
                      4 : [9, 9],
                      5 : [8, 8]},

                1 :  {0 : [10, 0],
                      1 : [0, 0],
                      2 : [11, 20],
                      3 : [15, 30],
                      4 : [22, 25],
                      5 : [12, 8]},

                2 :  {0 : [12, 0],
                      1 : [11, 20],
                      2 : [0, 0],
                      3 : [7, 11],
                      4 : [22, 35],
                      5 : [12, 8]},

                3 :  {0 : [11, 0],
                      1 : [15, 30],
                      2 : [7, 11],
                      3 : [0, 0],
                      4 : [13, 20],
                      5 : [35, 40]},

                4 :  {0 : [9, 0],
                      1 : [22, 35],
                      2 : [23, 32],
                      3 : [13, 20],
                      4 : [0, 0],
                      5 : [16, 25]},

                5 :  {0 : [8, 0],
                      1 : [12, 8],
                      2 : [15, 22],
                      3 : [35, 40],
                      4 : [16, 25],
                      5 : [0, 0]}}


# Parameters
max_weight=30 #maximum weight that can be carried by the employee
temperature=100 #starting temperature
alpha=0.99 #alpha parameter
min_temperatura=1 #target temperature
max_step=5000 #maximum number of steps before the mandatory break
break_time=100 #break time
n_vertex=2 #the number of vertices that are randomly selected




def make_widnow(neighbor_matrix):
    current_option_index = 0
    def on_closing():
        root.destroy()
        sys.exit()

    G = nx.DiGraph()

    for start_point, end_points in neighbor_matrix.items():
        for end_point, (time, steps) in end_points.items():
            G.add_edge(start_point, end_point, time=time, steps=steps)

    pos = nx.spring_layout(G)

    def update_graph(neighbor_matrix=neighbor_matrix):
        nonlocal G, pos
        G.clear()
        for start_point, end_points in neighbor_matrix.items():
            for end_point, (time, steps) in end_points.items():
                G.add_edge(start_point, end_point, time=time, steps=steps)
        pos = nx.spring_layout(G)
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_color="black",
                font_weight="bold", arrowsize=5)
        canvas.draw()


    # Create Tkinter window
    root = tk.Tk()
    root.title("Graph Viewer")

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    left_side_frame = tk.Frame(root, bg="lightblue")
    left_side_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

    # Create entry widgets and labels for user input using grid
    label_temperatura_poczatkowa = tk.Label(left_side_frame, text="Temperatura Początkowa:")
    label_temperatura_poczatkowa.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    entry_temperatura_poczatkowa = tk.Entry(left_side_frame, width=10)
    entry_temperatura_poczatkowa.insert(0, str(temperature))
    entry_temperatura_poczatkowa.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    label_temperatura_koncowa = tk.Label(left_side_frame, text="Temperatura Końcowa:")
    label_temperatura_koncowa.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    entry_temperatura_koncowa = tk.Entry(left_side_frame, width=10)
    entry_temperatura_koncowa.insert(0, str(min_temperatura))
    entry_temperatura_koncowa.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    label_liczba_iteracji = tk.Label(left_side_frame, text="możliwa l.kroków bez przerwy:")
    label_liczba_iteracji.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    entry_liczba_iteracji = tk.Entry(left_side_frame, width=10)
    entry_liczba_iteracji.insert(0, str(max_step))
    entry_liczba_iteracji.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    label_udzwigi = tk.Label(left_side_frame, text="udzwig:")
    label_udzwigi.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    entry_udzwigi = tk.Entry(left_side_frame, width=10)
    entry_udzwigi.insert(0, str(max_weight))
    entry_udzwigi.grid(row=3, column=1, padx=5, pady=5, sticky="w")


    label_alpha = tk.Label(left_side_frame, text="alpha:")
    label_alpha.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    entry_alpha = tk.Entry(left_side_frame, width=10)
    entry_alpha.insert(0, str(alpha))
    entry_alpha.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    label_break_time = tk.Label(left_side_frame, text="czas przerwy:")
    label_break_time.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    entry_break_time = tk.Entry(left_side_frame, width=10)
    entry_break_time.insert(0, str(break_time))
    entry_break_time.grid(row=5, column=1, padx=5, pady=5, sticky="w")


    label_vertex = tk.Label(left_side_frame, text="liczba vertex:")
    label_vertex.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    entry_vertex = tk.Entry(left_side_frame, width=10)
    entry_vertex.insert(0, str(n_vertex))
    entry_vertex.grid(row=6, column=1, padx=5, pady=5, sticky="w")


    button_option_1 = tk.Button(left_side_frame, text="Option 1", command=lambda: opcja1())
    button_option_1.grid(row=13, column=0, columnspan=2, pady=5)

    # Button to switch to the second option
    button_option_2 = tk.Button(left_side_frame, text="Option 2", command=lambda: opcja2())
    button_option_2.grid(row=14, column=0, columnspan=2, pady=5)

    # Button to switch to the third option
    button_option_3 = tk.Button(left_side_frame, text="Option 3", command=lambda: opcja3())
    button_option_3.grid(row=15, column=0, columnspan=2, pady=5)


    def opcja1():
        global stock_status, neighbor_matrix
        stock_status = {
                1: [[80, 4], [80, 3], [35, 1], [45, 5], [20, 2], [30, 1], [20, 3], [40, 4], [15, 2], [25, 2]],
                2: [[12, 4], [45, 2], [25, 2], [30, 3], [15, 1], [35, 4], [22, 5], [18, 2], [10, 3], [28, 4]],
                3: [[20, 2], [30, 1], [20, 3], [40, 4], [15, 2], [25, 2], [12, 1], [33, 3], [18, 4], [26, 2]],
                4: [[30, 7], [10, 1], [22, 5], [18, 2], [10, 3], [28, 4], [15, 2], [25, 2], [12, 4], [45, 2]],
                5: [[25, 2], [10, 10], [30, 3], [15, 1], [35, 4], [22, 5], [18, 2], [45, 2], [25, 2], [12, 4]]
            }
        neighbor_matrix= {
        0: {0: [0, 0], 1: [10, 10], 2: [12, 12], 3: [11, 11], 4: [9, 9], 5: [8, 8], 6: [15, 14], 7: [14, 13], 8: [13, 12], 9: [12, 11]},
        1: {0: [10, 0], 1: [0, 0], 2: [11, 20], 3: [15, 30], 4: [22, 25], 5: [12, 8], 6: [17, 16], 7: [16, 15], 8: [15, 14], 9: [14, 13]},
        2: {0: [12, 0], 1: [11, 20], 2: [0, 0], 3: [7, 11], 4: [22, 35], 5: [12, 8], 6: [14, 13], 7: [13, 12], 8: [12, 11], 9: [11, 10]},
        3: {0: [11, 0], 1: [15, 30], 2: [7, 11], 3: [0, 0], 4: [13, 20], 5: [35, 40], 6: [12, 11], 7: [11, 10], 8: [10, 9], 9: [9, 8]},
        4: {0: [9, 0], 1: [22, 35], 2: [23, 32], 3: [13, 20], 4: [0, 0], 5: [16, 25], 6: [11, 10], 7: [10, 9], 8: [9, 8], 9: [8, 7]},
        5: {0: [8, 0], 1: [12, 8], 2: [15, 22], 3: [35, 40], 4: [16, 25], 5: [0, 0], 6: [10, 9], 7: [9, 8], 8: [8, 7], 9: [7, 6]},
        6: {0: [15, 14], 1: [17, 16], 2: [14, 13], 3: [12, 11], 4: [11, 10], 5: [10, 9], 6: [0, 0], 7: [20, 19], 8: [19, 18], 9: [18, 17]},
        7: {0: [14, 13], 1: [16, 15], 2: [13, 12], 3: [11, 10], 4: [10, 9], 5: [9, 8], 6: [20, 19], 7: [0, 0], 8: [25, 24], 9: [24, 23]},
        8: {0: [13, 12], 1: [15, 14], 2: [12, 11], 3: [10, 9], 4: [9, 8], 5: [8, 7], 6: [19, 18], 7: [25, 24], 8: [0, 0], 9: [30, 29]},
        9: {0: [12, 11], 1: [14, 13], 2: [11, 10], 3: [9, 8], 4: [8, 7], 5: [7, 6], 6: [18, 17], 7: [24, 23], 8: [29, 28], 9: [0, 0]}
    }

        update_graph(neighbor_matrix)

        
    def opcja2():
        global stock_status, neighbor_matrix
        stock_status={
            1 : [[60, 4], [80, 3], [35, 1]],
            2 : [[12, 4], [45, 2], [25, 2]],
            3 : [[20, 2], [30, 1], [20, 3]],
            4 : [[30, 7], [10, 1]],
            5 : [[25, 2], [10, 10]]}
        neighbor_matrix={0 : {0 : [0, 0],
                      1 : [10, 10],
                      2 : [12, 12],
                      3 : [11, 11],
                      4 : [9, 9],
                      5 : [8, 8]},

                1 :  {0 : [10, 0],
                      1 : [0, 0],
                      2 : [11, 20],
                      3 : [15, 30],
                      4 : [22, 25],
                      5 : [12, 8]},

                2 :  {0 : [12, 0],
                      1 : [11, 20],
                      2 : [0, 0],
                      3 : [7, 11],
                      4 : [22, 35],
                      5 : [12, 8]},

                3 :  {0 : [11, 0],
                      1 : [15, 30],
                      2 : [7, 11],
                      3 : [0, 0],
                      4 : [13, 20],
                      5 : [35, 40]},

                4 :  {0 : [9, 0],
                      1 : [22, 35],
                      2 : [23, 32],
                      3 : [13, 20],
                      4 : [0, 0],
                      5 : [16, 25]},

                5 :  {0 : [8, 0],
                      1 : [12, 8],
                      2 : [15, 22],
                      3 : [35, 40],
                      4 : [16, 25],
                      5 : [0, 0]}}
        update_graph(neighbor_matrix)
            
    def opcja3():
        global stock_status, neighbor_matrix
        stock_status = {
        1: [[80, 4], [80, 3], [35, 1], [45, 5], [20, 2], [30, 1], [20, 3], [40, 4], [15, 2], [25, 2], [60, 3], [55, 5], [42, 2], [18, 3], [50, 4]],
        2: [[12, 4], [45, 2], [25, 2], [30, 3], [15, 1], [35, 4], [22, 5], [18, 2], [10, 3], [28, 4], [38, 2], [33, 3], [20, 1], [22, 5], [15, 2]],
        3: [[20, 2], [30, 1], [20, 3], [40, 4], [15, 2], [25, 2], [12, 1], [33, 3], [18, 4], [26, 2], [42, 4], [17, 3], [30, 1], [40, 4], [15, 2]],
        4: [[30, 7], [10, 1], [22, 5], [18, 2], [10, 3], [28, 4], [15, 2], [25, 2], [12, 4], [45, 2], [20, 1], [35, 4], [22, 5], [18, 2], [10, 3]],
        5: [[25, 2], [10, 10], [30, 3], [15, 1], [35, 4], [22, 5], [18, 2], [45, 2], [25, 2], [12, 4], [80, 3], [80, 3], [35, 1], [45, 5], [20, 2]],
        6: [[60, 3], [38, 2], [42, 4], [20, 1], [80, 4], [60, 3], [30, 1], [40, 4], [22, 5], [18, 2], [30, 1], [20, 3], [40, 4], [15, 2], [25, 2]],
        7: [[55, 5], [33, 3], [17, 3], [35, 4], [80, 3], [40, 4], [20, 2], [35, 4], [18, 2], [10, 3], [20, 3], [40, 4], [15, 2], [25, 2], [12, 4]],
        8: [[42, 2], [20, 1], [30, 1], [22, 5], [35, 4], [18, 2], [35, 4], [0, 0], [60, 3], [38, 2], [25, 2], [30, 3], [15, 1], [35, 4], [22, 5]],
        9: [[18, 3], [22, 5], [40, 4], [18, 2], [25, 2], [45, 2], [18, 4], [60, 3], [38, 2], [0, 0], [12, 4], [45, 2], [25, 2], [30, 3], [15, 1]],
        10: [[50, 4], [15, 2], [26, 2], [10, 3], [12, 4], [22, 5], [10, 3], [28, 4], [20, 1], [12, 4], [0, 0], [55, 5], [33, 3], [17, 3], [35, 4]],
        11: [[60, 3], [35, 4], [42, 4], [28, 4], [35, 4], [18, 2], [20, 3], [30, 1], [35, 4], [45, 5], [55, 5], [0, 0], [30, 1], [20, 3], [40, 4]],
        12: [[55, 5], [22, 5], [17, 3], [18, 2], [22, 5], [30, 1], [40, 4], [15, 2], [22, 5], [25, 2], [33, 3], [30, 1], [0, 0], [60, 3], [38, 2]],
        13: [[42, 2], [18, 4], [30, 1], [22, 5], [18, 2], [40, 4], [15, 2], [25, 2], [18, 2], [30, 3], [17, 3], [20, 3], [60, 3], [0, 0], [22, 5]],
        14: [[18, 3], [10, 3], [40, 4], [18, 2], [10, 3], [15, 2], [25, 2], [12, 4], [25, 2], [15, 2], [35, 4], [40, 4], [38, 2], [22, 5], [0, 0]],
        15: [[50, 4], [28, 4], [15, 2], [10, 3], [12, 4], [25, 2], [12, 4], [22, 5], [30, 3], [15, 1], [22, 5], [15, 2], [2, 1], [5, 2], [12, 4]],
    }
        neighbor_matrix = {
            0: {0: [0, 0], 1: [10, 10], 2: [12, 12], 3: [11, 11], 4: [9, 9], 5: [8, 8], 6: [15, 14], 7: [14, 13], 8: [13, 12], 9: [12, 11], 10: [20, 19], 11: [19, 18], 12: [18, 17], 13: [17, 16], 14: [16, 15], 15: [15, 14]},
            1: {0: [10, 0], 1: [0, 0], 2: [11, 20], 3: [15, 30], 4: [22, 25], 5: [12, 8], 6: [17, 16], 7: [16, 15], 8: [15, 14], 9: [14, 13], 10: [13, 12], 11: [12, 11], 12: [11, 10], 13: [10, 9], 14: [9, 8], 15: [8, 7]},
            2: {0: [12, 0], 1: [11, 20], 2: [0, 0], 3: [7, 11], 4: [22, 35], 5: [12, 8], 6: [14, 13], 7: [13, 12], 8: [12, 11], 9: [11, 10], 10: [10, 9], 11: [9, 8], 12: [8, 7], 13: [7, 6], 14: [6, 5], 15: [5, 4]},
            3: {0: [11, 0], 1: [15, 30], 2: [7, 11], 3: [0, 0], 4: [13, 20], 5: [35, 40], 6: [12, 11], 7: [11, 10], 8: [10, 9], 9: [9, 8], 10: [8, 7], 11: [7, 6], 12: [6, 5], 13: [5, 4], 14: [4, 3], 15: [3, 2]},
            4: {0: [9, 0], 1: [22, 35], 2: [23, 32], 3: [13, 20], 4: [0, 0], 5: [16, 25], 6: [11, 10], 7: [10, 9], 8: [9, 8], 9: [8, 7], 10: [7, 6], 11: [6, 5], 12: [5, 4], 13: [4, 3], 14: [3, 2], 15: [2, 1]},
            5: {0: [8, 0], 1: [12, 8], 2: [15, 22], 3: [35, 40], 4: [16, 25], 5: [0, 0], 6: [10, 9], 7: [9, 8], 8: [8, 7], 9: [7, 6], 10: [6, 5], 11: [5, 4], 12: [4, 3], 13: [3, 2], 14: [2, 1], 15: [1, 0]},
            6: {0: [15, 14], 1: [17, 16], 2: [14, 13], 3: [12, 11], 4: [11, 10], 5: [10, 9], 6: [0, 0], 7: [20, 19], 8: [19, 18], 9: [18, 17], 10: [17, 16], 11: [16, 15], 12: [15, 14], 13: [14, 13], 14: [13, 12], 15: [12, 11]},
            7: {0: [14, 13], 1: [16, 15], 2: [13, 12], 3: [11, 10], 4: [10, 9], 5: [9, 8], 6: [20, 19], 7: [0, 0], 8: [25, 24], 9: [24, 23], 10: [23, 22], 11: [22, 21], 12: [21, 20], 13: [20, 19], 14: [19, 18], 15: [18, 17]},
            8: {0: [13, 12], 1: [15, 14], 2: [12, 11], 3: [10, 9], 4: [9, 8], 5: [8, 7], 6: [19, 18], 7: [25, 24], 8: [0, 0], 9: [30, 29], 10: [29, 28], 11: [28, 27], 12: [27, 26], 13: [26, 25], 14: [25, 24], 15: [24, 23]},
            9: {0: [12, 11], 1: [14, 13], 2: [11, 10], 3: [9, 8], 4: [8, 7], 5: [7, 6], 6: [18, 17], 7: [24, 23], 8: [29, 28], 9: [0, 0], 10: [28, 27], 11: [27, 26], 12: [26, 25], 13: [25, 24], 14: [24, 23], 15: [23, 22]},
            10: {0: [20, 19], 1: [13, 12], 2: [10, 9], 3: [8, 7], 4: [7, 6], 5: [6, 5], 6: [17, 16], 7: [23, 22], 8: [29, 28], 9: [28, 27], 10: [0, 0], 11: [20, 19], 12: [19, 18], 13: [18, 17], 14: [17, 16], 15: [16, 15]},
            11: {0: [19, 18], 1: [12, 11], 2: [10, 9], 3: [6, 5], 4: [5, 4], 5: [4, 3], 6: [16, 15], 7: [22, 21], 8: [28, 27], 9: [27, 26], 10: [20, 19], 11: [0, 0], 12: [11, 10], 13: [10, 9], 14: [9, 8], 15: [8, 7]},
            12: {0: [18, 17], 1: [11, 10], 2: [9, 8], 3: [5, 4], 4: [4, 3], 5: [3, 2], 6: [15, 14], 7: [21, 20], 8: [27, 26], 9: [26, 25], 10: [19, 18], 11: [11, 10], 12: [0, 0], 13: [12, 11], 14: [11, 10], 15: [10, 9]},
            13: {0: [17, 16], 1: [10, 9], 2: [8, 7], 3: [4, 3], 4: [3, 2], 5: [2, 1], 6: [14, 13], 7: [20, 19], 8: [26, 25], 9: [25, 24], 10: [18, 17], 11: [10, 9], 12: [12, 11], 13: [0, 0], 14: [13, 12], 15: [12, 11]},
            14: {0: [16, 15], 1: [9, 8], 2: [7, 6], 3: [3, 2], 4: [2, 1], 5: [1, 0], 6: [13, 12], 7: [19, 18], 8: [25, 24], 9: [24, 23], 10: [17, 16], 11: [9, 8], 12: [11, 10], 13: [13, 12], 14: [0, 0], 15: [14, 13]},
            15: {0: [15, 14], 1: [8, 7], 2: [5, 4], 3: [2, 1], 4: [1, 0], 5: [0, 0], 6: [12, 11], 7: [18, 17], 8: [24, 23], 9: [23, 22], 10: [16, 15], 11: [8, 7], 12: [10, 9], 13: [12, 11], 14: [14, 13], 15: [0, 0]},
        }

        update_graph(neighbor_matrix)


    # Button to update graph based on selected nodes



    def button_start_clicked():
        temperatura_poczatkowa_val = float(entry_temperatura_poczatkowa.get())
        temperatura_koncowa_val = float(entry_temperatura_koncowa.get())
        liczba_iteracji_val = int(entry_liczba_iteracji.get())
        label_udzwigi= int(entry_udzwigi.get())
        break_time= int(entry_break_time.get())
        alpha= float(entry_alpha.get())
        vertex= int(entry_vertex.get())
        
        najlepsza_trasa, minimalna_dlugosc = simulated_annealing(temperatura_poczatkowa_val, alpha, temperatura_koncowa_val,liczba_iteracji_val,label_udzwigi,break_time,vertex)
        print('start acitvated')
        print("Najlepsza trasa:", najlepsza_trasa)
        print("Minimalna długość trasy:", minimalna_dlugosc)

    # Create some example buttons in the left_side_frame
    button1 = tk.Button(left_side_frame, text="START", command=lambda: button_start_clicked())
    button1.grid(row=7, column=0, columnspan=2, pady=10)


    fig, ax = plt.subplots()

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_color="black",
            font_weight="bold", arrowsize=5)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=1, sticky="nsew")

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def generate_first_path(max_weight): #generationg first random path
    # sum all items on all shelfs
    all_items=[]
    print(stock_status)
    for key, value in stock_status.items():
        for elem in value:
            for el in range(elem[0]):
                all_items.append((key,elem[1]))
    # generate random path between every item
    random_points=random.sample(all_items,len(all_items))
    first_path=[]
    cur_weight=0
    #taking items
    for elem in random_points:
        cur_weight=cur_weight+elem[1]
        # if possible take next item 
        if cur_weight<=max_weight:
            first_path.append([elem[0],cur_weight])
        # else put down items
        else:
            cur_weight=0
            first_path.append([0,cur_weight])
            cur_weight=cur_weight+elem[1]
            first_path.append([elem[0],cur_weight])

    return first_path, len(all_items)




def generate_next_path(cur_path, list_vertex_id, max_weight): #generationg next path, changing cur_path by list_vertex_id
    cur_path_info=[]
    cur_path_info=[[cur_path[0][0],cur_path[0][1]]]
    # get only path without putting down items
    for id, elem in enumerate(cur_path[1:]):
        if cur_path[id+1]!= [0, 0]:
            if cur_path[id]!= [0, 0]:
                cur_path_info.append([cur_path[id+1][0],cur_path[id+1][1]-cur_path[id][1]])
            else:
                cur_path_info.append([cur_path[id+1][0],cur_path[id+1][1]])
    # change vertex by provided list
    for elem in list_vertex_id:
        cur_path_info[elem[0]], cur_path_info[elem[1]]=cur_path_info[elem[1]], cur_path_info[elem[0]] #changing vertex
    next_path=[]
    cur_weight=0
    #taking items
    for elem in cur_path_info:
        # if possible take next item 
        cur_weight=cur_weight+elem[1]
        #print(max_weight)
        if cur_weight<=max_weight:
            next_path.append([elem[0],cur_weight])
        # else put down items
        else:
            cur_weight=0
            next_path.append([0,cur_weight])
            cur_weight=cur_weight+elem[1]
            next_path.append([elem[0],cur_weight])

    return next_path


def steps_time(path): #number of steps in path, time spend by walking (without breaks)
    n_steps=0
    s_time=0
    #sum steps and time
    for id, point in enumerate(path[:-1]):
        if path[id][0]!=path[id+1][0]:
            n_steps=n_steps+neighbor_matrix[path[id][0]][path[id+1][0]][1]
            s_time=s_time+neighbor_matrix[path[id][0]][path[id+1][0]][0]
    return {"Liczba kroków:" : n_steps, "Całkowity czas:" : s_time}


def funkcja_celu(droga, czas,max_step,break_time): #calculate cost 
    return czas+(droga//max_step)*break_time


def random_vertex(temperature, n_items,n_vertex): #generate random list of random vertex
    n_vertex=random.randint(2, int(temperature+2))
    n_vertex=random.randint(2, int(n_vertex))
    lista=[random.sample(range(0, int(n_items)), 2) for elem in range(n_vertex)]
    return lista


def plot_data(x, y): #plot output 
    plt.plot(x, y)
    plt.title("SA algorithm")
    plt.xlabel("Path number")
    plt.ylabel("Score")
    plt.show()


def simulated_annealing(temperature, alpha, min_temperatura,max_step,udzwigi,break_time,vertex): #implementation os SA function
    first_path, n_items=generate_first_path(udzwigi) #generating first path
    best_score=999999 # initialazing best_score param
    cur_path=first_path #setting first path as current path
    new_score=steps_time(cur_path) #calculating new_score

    # ploting 
    all_scores=[]
    all_iterations=[] 
    acc=0

    while temperature>min_temperatura: #while currtent temperature is higher then minimal temperature
        vertex_id_change=random_vertex(temperature, n_items,vertex) #generate IDs of vertex to change
        new_path = generate_next_path(cur_path,vertex_id_change, udzwigi) #generate next path
        new_score=steps_time(new_path) #calculate score
        new_score=funkcja_celu(new_score['Liczba kroków:'],new_score['Całkowity czas:'],max_step,break_time)

        delta_dlugosc = new_score - funkcja_celu(steps_time(cur_path)['Liczba kroków:'],steps_time(cur_path)['Całkowity czas:'],max_step,break_time) # calculate delta

        if delta_dlugosc < 0 or random.uniform(0, 1) < math.exp(-delta_dlugosc / (temperature)): #if new score is better then previos or random state is True - add new best score
            cur_path = new_path
            acc=acc+1
            all_scores.append(new_score) #add new score
            all_iterations.append(acc)
            if best_score>new_score: #if current best score is better then previos 
                best_score=new_score #set new best score
                print(best_score)
            temperature = temperature * alpha #change temperature by alpha

    plot_data(all_iterations, all_scores) #plot results
            
    return cur_path, best_score #return path and best score


make_widnow(neighbor_matrix)