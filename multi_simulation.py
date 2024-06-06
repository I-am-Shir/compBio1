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
            # When vertical and horizontal cells match
            if left != grid[i, j] and right != grid[i, j] and above == grid[i, j] and below == grid[i, j]:
                resemblance_value += cell_significance
            # When the vertical cells match but horizontal only partially
            elif (above == grid[i, j] and below == grid[i, j]) and (
                    (right == grid[i, j] and left != grid[i, j])
                    or (left == grid[i, j] and right != grid[i, j])):
                resemblance_value += partial_cell_signif

    return resemblance_value * 100


# Run a single simulation
def run_single_simulation(size, generations, interval):
    grid_data = initialize_grid(size)
    metric_values = []

    for _ in range(generations):
        grid_data = update_grid(grid_data)
        metric_value = calculate_stripe_percentage(grid_data)
        metric_values.append(metric_value)

    return metric_values


# Main function to run multiple simulations and plot the results
def run_multiple_simulations(size, generations, interval, num_runs=10):
    all_runs_metrics = []

    for run in range(num_runs):
        metric_values = run_single_simulation(size, generations, interval)
        all_runs_metrics.append(metric_values)

    # Plot the results
    plt.figure(figsize=(10, 6))
    for run_index, metrics in enumerate(all_runs_metrics):
        plt.plot(range(generations), metrics, label=f'Run {run_index + 1}')

    plt.title("Stripe Closeness Over Time for Multiple Runs")
    plt.xlabel("Generations")
    plt.ylabel("Stripe Closeness (%)")
    plt.legend()
    plt.grid(True)
    plt.show()


# Parameters
size = 80
generations = 500
interval = 100  # Time between updates in milliseconds

# Run the simulations
run_multiple_simulations(size, generations, interval, num_runs=10)
