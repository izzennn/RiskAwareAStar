# RiskAwareAStar
Multi-agent pathfinding on procedurally generated mazes using A* augmented with dynamic threat-based heuristics

# Threat-Aware Path Planning (A* Simulation)

This Python project uses **Pygame** to simulate a procedurally generated maze in which multiple agents navigate using the **A\*** search algorithm. A primary agent (Pacman) plans paths toward food while dynamically avoiding pursuing agents (ghosts) by incorporating **threat-based costs** directly into the search process.

## Features

- Procedural maze generation using DFS backtracking  
- Grid-based maze with explicit wall representation  
- A\* pathfinding implemented using priority queues (`heapq`)  
- Node-based search with tracked `g`, `h`, and `f` costs  
- Multi-agent simulation (Pacman, multiple ghosts, food)  
- Dynamic danger values influencing Pacman’s decisions  
- Continuous real-time replanning and visualization using Pygame  

## How it Works

### Maze Creation

- The maze is represented as a grid of `Cell` objects.
- Each cell tracks whether its **top, bottom, left, and right walls** are present.
- A **Depth-First Search (DFS)** algorithm with an explicit `stack` is used to generate the maze:
  - A random unvisited neighbor is chosen.
  - Walls between the current cell and neighbor are removed.
  - The algorithm backtracks when no unvisited neighbors remain.
- This guarantees that the maze is **fully connected**, meaning every cell is reachable.

### Graph Representation

- Each cell corresponds to a node in a graph.
- Valid neighbors are determined by checking which walls have been removed.
- Nodes are indexed by `(row, col)` coordinates and stored in dictionaries during search.
- A dedicated `Node` class is used during A\* search to store:
  - `g`: cost from the start
  - `h`: heuristic estimate to the goal
  - `f = g + h`
  - `danger`: accumulated threat cost

### A\* Pathfinding Implementation

- A\* search is implemented explicitly using `heapq` as a priority queue.
- The heuristic function used is **Manhattan distance**, appropriate for grid movement.
- Open and closed sets are tracked to prevent revisiting nodes.
- Each step updates neighboring nodes only if a lower-cost path is found.

### Threat (Danger) Modeling

- Ghost positions are used to compute a **danger value** for each cell.
- Cells closer to ghosts contribute a higher danger penalty.
- During A\* expansion, Pacman’s path cost includes:
  - Movement cost (`g`)
  - Heuristic distance to food (`h`)
  - An added danger component derived from nearby ghosts
- This causes Pacman to:
  - Prefer longer but safer paths
  - Avoid corridors dominated by ghosts
  - Sometimes stop moving if no safe path exists

### Multi-Agent Behavior

- **Pacman**, **ghosts**, and **food** are implemented as separate classes.
- Ghosts continuously recompute paths toward Pacman using A\* without danger penalties.
- Pacman continuously replans its path toward food as ghost positions change.
- All agents update and move inside the main Pygame loop, keeping behavior synchronized with rendering.

### Simulation Loop

- The main loop:
  - Draws the maze, food, Pacman, and ghosts
  - Updates danger values
  - Calls each agent’s `chase()` logic
  - Renders the updated state every frame
- The simulation is designed to run indefinitely, allowing long-term observation of behavior.

## Challenges Faced

- Designing a reusable `Node` structure that cleanly supports dynamic costs.
- Correctly integrating danger penalties into A\* without breaking the algorithm.
- Handling cases where Pacman cannot find a valid path and treating them as expected outcomes.
- Coordinating multiple A\* searches per frame while maintaining performance.
- Debugging real-time path replanning in a continuously evolving environment.

