# RiskAwareAStar
Multi-agent pathfinding on procedurally generated mazes using A* augmented with dynamic threat-based heuristics

# Threat-Aware Path Planning (A* Simulation)

This Python project uses **Pygame** to simulate a procedurally generated maze in which multiple agents navigate using the **A\*** search algorithm. A primary agent (Pacman) plans paths toward goals while dynamically avoiding pursuing agents (ghosts) by incorporating **threat-based costs** into its heuristic.

## Features

- Procedural maze generation using DFS backtracking  
- Additional randomized wall removal to introduce cycles and multiple paths  
- Graph-based maze representation with wall-aware neighbors  
- Real-time A\* pathfinding and continuous replanning  
- Multi-agent pursuit and evasion (Pacman vs ghosts)  
- Dynamic threat (danger) field influencing path selection  
- Continuous simulation with emergent behavior  

## How it Works

### Maze Creation

- The environment is represented as a 2D grid where each cell starts with walls on all four sides.
- A **Depth-First Search (DFS) backtracking algorithm** is used to generate a *perfect maze* by randomly visiting neighboring cells and removing walls.
- After the initial maze is created, additional walls are randomly removed between regions to introduce **cycles**, preventing the maze from being strictly tree-like and allowing multiple valid paths between locations.
- The final result is a fully connected maze with both corridors and loops.

### Graph Representation

- Each maze cell acts as a node in a graph.
- Valid neighbors are determined by checking whether walls exist between adjacent cells.
- This graph structure is used directly by the A\* algorithm for path planning.

### Pathfinding with A\*

- Both Pacman and the ghosts use the **A\*** algorithm to plan paths.
- The heuristic used is **Manhattan distance**, which is well-suited for grid-based movement.
- Ghosts compute shortest paths directly toward Pacman.
- Pacman computes paths toward food while incorporating an additional **danger cost**.

### Threat-Aware Planning

- Each cell maintains a `danger` value based on its distance from nearby ghosts.
- Cells closer to ghosts are assigned higher costs.
- Pacman’s A\* cost function combines:
  - Distance traveled  
  - Estimated distance to the goal  
  - A weighted danger penalty  
- This causes Pacman to prefer *safer routes*, even if they are longer, and sometimes to stop moving entirely if no safe path exists.

### Multi-Agent Dynamics

- Ghosts periodically recompute paths to chase Pacman.
- Pacman continuously replans paths in response to:
  - Ghost movement  
  - Changes in danger levels  
  - New food locations  
- These interactions produce **emergent behaviors**, such as evasive movement, waiting when trapped, or choosing longer but safer paths.

## Challenges Faced

- Implementing A\* efficiently using priority queues, open/closed sets, and consistent node tracking.
- Designing a threat-based heuristic that influences behavior without breaking pathfinding correctness.
- Handling cases where **no valid path exists**, treating them as meaningful outcomes rather than failures.
- Synchronizing multiple agents with different replanning intervals in a real-time simulation.
- Balancing simulation speed and visualization clarity in Pygame.
