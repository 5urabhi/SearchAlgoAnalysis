import matplotlib.pyplot as plt
import queue
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Grid_Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, pos: Grid_Position, cost, parent=None):
        self.pos = pos
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic_value(curr, dest):
    return abs(curr.x - dest.x) + abs(curr.y - dest.y)

def plot_maze(maze, visited_nodes, path, title, file_name, start, goal):
    fig, ax = plt.subplots(figsize=(10, 10))
    maze_array = [[0 if cell == 0 else 1 for cell in row] for row in maze]

    # Convert RGB values from 0-255 to 0-1 range
    def rgb_to_normalized(rgb):
        return tuple(val / 255.0 for val in rgb)

    # Define colors
    colors = {
        'wall': rgb_to_normalized((40, 40, 40)),
        'start': rgb_to_normalized((255, 0, 0)),
        'goal': rgb_to_normalized((0, 171, 28)),
        'solution': rgb_to_normalized((220, 235, 113)),
        'explored': rgb_to_normalized((212, 97, 85)),
        'empty': rgb_to_normalized((237, 240, 252))
    }

    # Plot the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 0:
                fill = colors['wall']
            elif (i, j) == (start.x, start.y):
                fill = colors['start']
            elif (i, j) == (goal.x, goal.y):
                fill = colors['goal']
            elif any(node.x == i and node.y == j for node in path):
                fill = colors['solution']
            elif any(node.x == i and node.y == j for node in visited_nodes):
                fill = colors['explored']
            else:
                fill = colors['empty']
            
            ax.add_patch(patches.Rectangle((j, i), 1, 1, color=fill))

    ax.set_title(title)
    ax.set_xlim([0, len(maze[0])])
    ax.set_ylim([0, len(maze)])
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig(file_name)
    plt.close()





def trace_path(end_node):
    path = []
    current = end_node
    while current:
        path.append(current.pos)
        current = current.parent
    return path[::-1]  # Return reversed path

def load_maze(file_path):
    maze = []
    start = None
    goal = None
    with open(file_path, 'r') as file:
        for x, line in enumerate(file):
            row = []
            for y, char in enumerate(line.rstrip('\n')):
                if char == 'A':
                    start = Grid_Position(x, y)
                    row.append(1)
                elif char == 'B':
                    goal = Grid_Position(x, y)
                    row.append(1)
                elif char == ' ':
                    row.append(1)
                else:
                    row.append(0)
            maze.append(row)
    if start is None or goal is None:
        raise ValueError("Maze must have a starting point 'A' and a goal 'B'.")
    
    # Print maze for debugging
    print("Maze:")
    for row in maze:
        print(''.join([' ' if cell == 1 else '#' for cell in row]))
    print(f"Start: ({start.x}, {start.y})")
    print(f"Goal: ({goal.x}, {goal.y})")
    
    return maze, start, goal

             

def gbfs(Grid, dest: Grid_Position, start: Grid_Position):
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]
    visited_blocks = [[False for _ in range(len(Grid[0]))] for _ in range(len(Grid))]
    q = queue.PriorityQueue()
    start_node = Node(start, 0)
    q.put((0, start_node))
    visited_blocks[start.x][start.y] = True
    visited_nodes = []

    while not q.empty():
        _, current_node = q.get()
        visited_nodes.append(current_node.pos)
        print(f"GBFS Visiting: ({current_node.pos.x}, {current_node.pos.y})")
        if current_node.pos.x == dest.x and current_node.pos.y == dest.y:
            return current_node, visited_nodes

        for dx, dy in zip(adj_cell_x, adj_cell_y):
            nx, ny = current_node.pos.x + dx, current_node.pos.y + dy
            if 0 <= nx < len(Grid) and 0 <= ny < len(Grid[0]) and Grid[nx][ny] == 1:
                if not visited_blocks[nx][ny]:
                    visited_blocks[nx][ny] = True
                    neighbor = Node(Grid_Position(nx, ny), current_node.cost + 1, current_node)
                    h = heuristic_value(neighbor.pos, dest)
                    q.put((h, neighbor))
    return None, visited_nodes


def main():
    file_path = 'maze2.txt'
    maze, starting_position, destination = load_maze(file_path)
    
    # Run GBFS
    gbfs_result, gbfs_visited_nodes = gbfs(maze, destination, starting_position)
    if gbfs_result:
        gbfs_path = trace_path(gbfs_result)
        plot_maze(maze, gbfs_visited_nodes, gbfs_path, "Greedy Best-First Search Solution", "gbfs_solution.png", starting_position, destination)
        print("GBFS Path cost = ", gbfs_result.cost)
        print("GBFS Path:", [(pos.x, pos.y) for pos in gbfs_path])
        print("GBFS Visited Nodes:", [(pos.x, pos.y) for pos in gbfs_visited_nodes])
    else:
        print("GBFS Path does not exist")
                                    
if __name__ == '__main__':
    main()



