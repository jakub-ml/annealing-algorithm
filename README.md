# Project: Pallet Loading Optimization in a Warehouse
### Problem Introduction
The goal of the project is to optimize the process of loading a custom pallet with grocery products in a warehouse.
The worker must quickly collect products from shelves while being limited by a maximum carrying capacity of 30 kg and mandatory breaks after every 5,000 steps (each break lasting 2 minutes).
The objective is to maximize work efficiency by planning the most effective movement path.

### Task Description
* Maximum carrying weight: 30 kg

* Breaks: Every 5,000 steps – 2-minute break

* Product collection rules:

    * The worker can carry products from multiple shelves simultaneously (as long as the weight limit is not exceeded).

    * The worker operates continuously except for the mandatory breaks.

    * Carried products are placed onto the pallet immediately after pickup.

    * All shelves have the same priority.

    * The weight carried does not affect movement speed.

    * Travel time between any two objects (shelves, pallet) is constant.

### Warehouse Map Layout
The project assumes a simplified warehouse map showing the placement of shelves and the pallet.
Movement between objects always takes the same amount of time, regardless of distance.
  
<p align="center">
  <img src="https://github.com/user-attachments/assets/f3ba173e-a33e-4b1c-9720-a44502aff8e8" alt="image">
</p>

### Simplifications
* No products exceed the worker’s maximum carrying capacity.

* Movement speed is not affected by the carried weight.

* Constant time for traveling between any two objects.

* No additional breaks other than the ones required after 5,000 steps.

### Theory: Simulated Annealing
* The optimization algorithm uses Simulated Annealing – a metaheuristic inspired by the process of annealing metals.

* Temperature: A parameter controlling the randomness of solution modifications; it decreases over time.

* Iterative Process: In each iteration, a new solution is generated by modifying the previous one.

* Acceptance of Worse Solutions: There is a probability of accepting worse solutions to avoid getting stuck in local maxima.

* Boltzmann Distribution Formula: The probability of accepting a worse solution 


### Application Interface Overview
The image presents the graphical interface of a simulation tool used to visualize and control the simulated annealing algorithm for warehouse optimization.

**Left Panel** – Parameter Configuration
On the left side of the interface, the user can configure various parameters for the algorithm.

**Right Panel** – Graph Visualization
On the right side, a fully connected graph with 6 vertices (labeled 0 to 5) is displayed. Each vertex represents a possible location in the warehouse (e.g., shelf or pallet location), and each edge represents a possible direct path between two locations.

![image](https://github.com/user-attachments/assets/a7a1cbb7-553e-4a44-8353-fd23cf1ac461)

The graph illustrates the performance of the Simulated Annealing algorithm as it searches for an optimal solution. Initially, the score fluctuates due to high temperature, allowing exploration of various paths, including suboptimal ones. Over time, the score steadily decreases, reaching a best result of 2530, as the algorithm converges toward an optimal solution.

![image](https://github.com/user-attachments/assets/64038632-e351-407e-a68c-4bdc25770049)

### Conclusions
As demonstrated, the simulated annealing algorithm proves to be highly effective, particularly due to its ability to avoid local minima through careful temperature management.
It can be applied to a wide range of problems, with its efficiency largely depending on the complexity of the specific task and the ability to properly tailor the algorithm to the problem domain.

In our case, through testing various scenarios, it became evident that the results are significantly influenced by the input data and the chosen parameters.
In one scenario, the performance graphs resembled the typical behavior of the algorithm, with notable jumps at the beginning caused by high temperatures. In another scenario, the graph showed a more stepwise decline, dominated by the impact of certain parameters.

In summary, the simulated annealing algorithm successfully addressed the defined problem and provided valuable insights throughout the process.

The complete analysis, including additional scenarios, solutions, and parameter configurations, is available in the attached **Results.pdf** file.
