# Breadth-First Search (BFS) Visualization

A Python-based interactive visualization of the Breadth-First Search (BFS) algorithm, built using `pygame`. This project lets users create a grid-based environment, set a start and goal point, and watch the BFS algorithm find the shortest path between them.

## Features

- **Interactive Grid Drawing**:
  - Click and drag to create walls.
  - Hold `Shift` and click to set the **start** point.
  - Hold `Ctrl` and click to set the **goal** point.
- **BFS Visualization**:
  - Watch BFS explore the grid in real-time, highlighting the explored nodes and the shortest path.
- **Interruptible Execution**:
  - Press `Spacebar` to start or interrupt the BFS process.
- **Reset Options**:
  - Press `C` to clear all walls while keeping the start and goal points.
  - Press `R` to reset the entire grid.

## Controls

| Action              | Key/Mouse Input |
| ------------------- | --------------- |
| Draw walls          | Click and drag  |
| Set start point     | `Shift + Click` |
| Set goal point      | `Ctrl + Click`  |
| Start/Interrupt BFS | `Spacebar`      |
| Clear walls         | `C`             |
| Reset grid          | `R`             |

## Requirements

- Python 3.10+ (with type hinting support)
- `pygame` library (Install via pip)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nofoxtugiv/bfs-visualization.git
   cd bfs-visualization
   ```
