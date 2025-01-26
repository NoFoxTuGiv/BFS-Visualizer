import pygame  # type: ignore
from typing import Dict, List, Optional, Tuple

# Type Aliases
Grid = Dict[Tuple[int, int], Dict[str, str]]
Graph = Dict[Tuple[int, int], List[Tuple[int, int]]]
Parents = Dict[Tuple[int, int], Optional[Tuple[int, int]]]

# Constants
CELL_SIZE = 30
MARGIN = 2
GRID_SIZE = 30
BORDER_SIZE = 5
RESOLUTION = ((CELL_SIZE + MARGIN) * GRID_SIZE) + (BORDER_SIZE * 2)
COLORS = {
    "empty": "white",
    "wall": "black",
    "start": "green",
    "goal": "orange",
    "explored": "yellow",
    "path": "purple",
}


def display_message(screen: pygame.Surface, message: str, duration: int = 2000) -> None:
    font = pygame.font.Font(None, 36)
    text_surface = font.render(message, True, "white")
    text_rect = text_surface.get_rect(center=(RESOLUTION // 2, RESOLUTION // 2))
    background = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
    background.set_alpha(150)
    background.fill("black")
    background_rect = background.get_rect(center=text_rect.center)
    screen.blit(background, background_rect)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration)


def initialize_grid() -> Grid:
    return {
        (col, row): {"state": "empty"}
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
    }


def build_graph(
    grid: Grid,
) -> Tuple[Graph, Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    start, goal = None, None
    graph = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for (col, row), cell in grid.items():
        if cell["state"] == "start":
            start = (col, row)
        elif cell["state"] == "goal":
            goal = (col, row)

        if cell["state"] in {"empty", "start", "goal"}:
            graph[(col, row)] = [
                (col + dc, row + dr)
                for dc, dr in directions
                if (col + dc, row + dr) in grid
                and grid[(col + dc, row + dr)]["state"] in {"empty", "goal"}
            ]
    return graph, start, goal


def reconstructRoute(
    parents: Parents, start: Tuple[int, int], goal: Tuple[int, int], grid: Grid
) -> List[Tuple[int, int]]:
    path = []
    currentNode = goal
    while currentNode is not None:
        path.append(currentNode)
        if grid[currentNode]["state"] not in {"start", "goal"}:
            grid[currentNode]["state"] = "path"
        currentNode = parents[currentNode]
    return path[::-1]


def is_within_bounds(col: int, row: int) -> bool:
    return 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE


def main() -> None:
    screen = pygame.display.set_mode((RESOLUTION, RESOLUTION))
    clock = pygame.time.Clock()
    running = True
    grid = initialize_grid()
    bfs_active = False
    bfs_queue: List[Tuple[int, int]] = []
    bfs_parents: Parents = {}
    bfs_visited: List[Tuple[int, int]] = []
    bfs_start: Optional[Tuple[int, int]] = None
    bfs_goal: Optional[Tuple[int, int]] = None
    mouse_held = False

    pygame.init()
    pygame.display.set_caption("Breadth-First Search")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse events for drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - BORDER_SIZE) // (CELL_SIZE + MARGIN)
                row = (mouse_y - BORDER_SIZE) // (CELL_SIZE + MARGIN)

                if is_within_bounds(col, row):
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_SHIFT:
                        for key in grid:
                            if grid[key]["state"] == "start":
                                grid[key]["state"] = "empty"
                        grid[(col, row)]["state"] = "start"
                    elif mods & pygame.KMOD_CTRL:
                        for key in grid:
                            if grid[key]["state"] == "goal":
                                grid[key]["state"] = "empty"
                        grid[(col, row)]["state"] = "goal"
                    else:
                        grid[(col, row)]["state"] = "wall"

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            if event.type == pygame.MOUSEMOTION and mouse_held:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = (mouse_x - BORDER_SIZE) // (CELL_SIZE + MARGIN)
                row = (mouse_y - BORDER_SIZE) // (CELL_SIZE + MARGIN)

                if is_within_bounds(col, row):
                    grid[(col, row)]["state"] = "wall"

            # Clear the grid
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                for key in grid:
                    if grid[key]["state"] != "wall":
                        grid[key]["state"] = "empty"

            # Reset the grid
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                grid = initialize_grid()

            # Start/Interrupt BFS
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bfs_active:
                    bfs_active = False
                    bfs_queue = []
                    bfs_parents = {}
                    bfs_visited = []
                    for key in grid:
                        if grid[key]["state"] in {"explored", "path"}:
                            grid[key]["state"] = "empty"
                else:
                    graph, bfs_start, bfs_goal = build_graph(grid)
                    if not bfs_start:
                        display_message(screen, "No start point set.")
                    elif not bfs_goal:
                        display_message(screen, "No end point set.")
                    else:
                        bfs_queue = [bfs_start]
                        bfs_parents = {bfs_start: None}
                        bfs_visited = []
                        bfs_active = True

        # BFS animation
        if bfs_active and bfs_queue:
            pygame.time.wait(25)
            currentNode = bfs_queue.pop(0)
            if currentNode not in bfs_visited:
                bfs_visited.append(currentNode)
                if grid[currentNode]["state"] not in {"start", "goal"}:
                    grid[currentNode]["state"] = "explored"

                if currentNode == bfs_goal:
                    bfs_active = False
                    reconstructRoute(bfs_parents, bfs_start, bfs_goal, grid)

                for neighbor in graph[currentNode]:
                    if neighbor not in bfs_visited and neighbor not in bfs_queue:
                        bfs_queue.append(neighbor)
                        bfs_parents[neighbor] = currentNode

            if bfs_active and not bfs_queue:
                bfs_active = False
                display_message(screen, "No valid path found.")

        # Render grid
        screen.fill("black")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * (CELL_SIZE + MARGIN) + BORDER_SIZE
                y = row * (CELL_SIZE + MARGIN) + BORDER_SIZE
                state = grid[(col, row)]["state"]
                cellColor = COLORS.get(state, "gray")
                pygame.draw.rect(screen, cellColor, (x, y, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
