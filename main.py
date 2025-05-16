import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Initialize the grid with 50% of each color
def initialize_grid(size):
    return np.random.choice([0, 1], size=(size, size)).astype(bool)

# Update the grid according to the new rules
def update_grid(grid):
    new_grid = grid.copy()
    size = grid.shape[0]
    for i in range(size):
        for j in range(size):
            # Vertical and horizontal neighbors
            above = grid[(i - 1) % size, j]
            below = grid[(i + 1) % size, j]
            left = grid[i, (j - 1) % size]
            right = grid[i, (j + 1) % size]

            # Diagonal neighbors
            top_left = grid[(i - 1) % size, (j - 1) % size]
            top_right = grid[(i - 1) % size, (j + 1) % size]
            bottom_left = grid[(i + 1) % size, (j - 1) % size]
            bottom_right = grid[(i + 1) % size, (j + 1) % size]

            neighbors = [above, below, left, right, top_left, top_right, bottom_left, bottom_right]
            side_neighbors = [left, right, top_left, top_right, bottom_left, bottom_right]
            prob = np.random.rand()  # Random probability between 0 and 1

            # If all neighbors are the same (either all 0 or all 1)
            if all(n == 0 for n in neighbors) or all(n == 1 for n in neighbors):
                new_grid[i, j] = 1 - neighbors[0]
            # If all side neighbors are the same (either all 0 or all 1)
            elif all(n == 0 for n in side_neighbors) or all(n == 1 for n in side_neighbors):
                # With a 99% probability, invert the value of the current cell
                if prob < 0.99:
                    new_grid[i, j] = 1 - side_neighbors[0]
            # If the cells above and below are the same
            elif above == below:
                # With an 80% probability, set the current cell to the value of the cell above/below
                if prob < 0.8:
                    new_grid[i, j] = above
            # If the cells to the left and right are the same
            elif left == right:
                # With an 80% probability, invert the value of the current cell
                if prob < 0.8:
                    new_grid[i, j] = 1 - left
            # If there are 5 or more neighbors with the value 1
            elif sum(neighbors) >= 5:
                # With a 70% probability, set the current cell to 0
                if prob < 0.7:
                    new_grid[i, j] = 0
            # If there are 3 or fewer neighbors with the value 1
            elif sum(neighbors) <= 3:
                # With a 70% probability, set the current cell to 1
                if prob < 0.7:
                    new_grid[i, j] = 1
            # If none of the above conditions are met
            else:
                # With a 50% probability, invert the value of the current cell
                if prob < 0.5:
                    new_grid[i, j] = 1 - grid[i, j]

    return new_grid

# Calculate the percentage of cells that match the expected striped pattern
def calculate_stripe_percentage(grid):
    size = grid.shape[0]
    cells_in_grid = size * size
    cell_significance = 1 / cells_in_grid
    partial_cell_signif = cell_significance / 2
    resemblance_value = 0

    for i in range(size):
        for j in range(size):
            above = grid[(i - 1) % size, j]
            below = grid[(i + 1) % size, j]
            left = grid[i, (j - 1) % size]
            right = grid[i, (j + 1) % size]
            # when vertical and horizontal cells match
            if left != grid[i, j] and right != grid[i, j] and above == grid[i, j] and below == grid[i, j]:
                resemblance_value += cell_significance
            # when the vertical cells match but horizontal only partially
            elif (above == grid[i, j] and below == grid[i, j]) and (
                    (right == grid[i, j] and left != grid[i, j])
                or (left == grid[i, j] and right != grid[i, j])):
                resemblance_value += partial_cell_signif

    return resemblance_value * 100

# Tkinter GUI to display the grid and track the progress of the metric
class GridDisplay(tk.Tk):
    def __init__(self, size, generations, interval):
        super().__init__()
        self.title("Grid Simulation")
        self.size = size
        self.generations = generations
        self.interval = interval
        self.grid_data = initialize_grid(size)
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()
        self.rect_size = 500 // size
        self.metric_label = ttk.Label(self, text="Stripe Closeness: 0%")
        self.metric_label.pack()
        self.generation_label = ttk.Label(self, text="Generation: 0")
        self.generation_label.pack()
        self.start_button = ttk.Button(self, text="Start", command=self.start_simulation)
        self.start_button.pack()
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_simulation)
        self.stop_button.pack()
        self.restart_button = ttk.Button(self, text="Restart", command=self.restart_simulation)
        self.restart_button.pack()
        self.current_generation = 0
        self.metric_values = []
        self.running = False

        self.draw_grid()

    # Initializes the grid's visuals.
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                color = "black" if self.grid_data[i, j] else "white"
                self.canvas.create_rectangle(
                    j * self.rect_size, i * self.rect_size,
                    (j + 1) * self.rect_size, (i + 1) * self.rect_size,
                    fill=color, outline="gray"
                )

    def update_metric(self):
        metric_value = calculate_stripe_percentage(self.grid_data)
        self.metric_label.config(text=f"Stripe Closeness: {metric_value:.2f}%")
        self.generation_label.config(text=f"Generation: {self.current_generation}")
        self.metric_values.append(metric_value)

    # Runs the simulation according to the number of generations
    def run_simulation(self):
        if self.running and self.current_generation < self.generations:
            self.grid_data = update_grid(self.grid_data)
            self.draw_grid()
            self.update_metric()
            self.current_generation += 1
            self.after(self.interval, self.run_simulation)
        elif self.current_generation >= self.generations:
            self.show_graph()  # Plot the metric progress at the end of simulation

    # a button for starting the run
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_simulation()

    # a button for stopping the run
    def stop_simulation(self):
        self.running = False

    # a button for restarting the run
    def restart_simulation(self):
        self.stop_simulation()
        self.grid_data = initialize_grid(self.size)
        self.current_generation = 0
        self.metric_values = []
        self.metric_label.config(text="Stripe Closeness: 0%")
        self.generation_label.config(text="Generation: 0")
        self.draw_grid()

    # plot metric for Stripe Closeness
    def show_graph(self):
        plt.figure()
        plt.plot(range(len(self.metric_values)), self.metric_values, linestyle='-', linewidth=1, label="Stripe Closeness")
        plt.title("Stripe Closeness Over Time")
        plt.xlabel("Generations")
        plt.ylabel("Stripe Closeness (%)")
        plt.legend()
        plt.grid(True)
        plt.show()

# Parameters
size = 80
generations = 500
interval = 100  # Time between updates in milliseconds

# Run the Tkinter GUI
app = GridDisplay(size, generations, interval)
app.mainloop()