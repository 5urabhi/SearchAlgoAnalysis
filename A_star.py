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


def a_star(maze, end, start):
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]

    open_set = queue.PriorityQueue()
    closed = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start_node = Node(start, 0)
    open_set.put((0, start_node))
    closed[start.x][start.y] = True
    visited_nodes = []

    while not open_set.empty():
        _, current_node = open_set.get()
        visited_nodes.append(current_node.pos)
        print(f"A* Visiting: ({current_node.pos.x}, {current_node.pos.y})")
        if current_node.pos.x == end.x and current_node.pos.y == end.y:
            return current_node, visited_nodes

        for dx, dy in zip(adj_cell_x, adj_cell_y):
            nx, ny = current_node.pos.x + dx, current_node.pos.y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1:
                if not closed[nx][ny]:
                    closed[nx][ny] = True
                    h = heuristic_value(Grid_Position(nx, ny), end)
                    g = current_node.cost + 1
                    f = h + g
                    neighbor = Node(Grid_Position(nx, ny), f, current_node)
                    open_set.put((f, neighbor))
    return None, visited_nodes

def main():
    file_path = 'maze2.txt'
    maze, starting_position, destination = load_maze(file_path)
    
    a_star_result, a_star_visited_nodes = a_star(maze, destination, starting_position)
    if a_star_result:
        a_star_path = trace_path(a_star_result)
        plot_maze(maze, a_star_visited_nodes, a_star_path, "A* Search Solution", "a_star_solution.png", starting_position, destination)
        print("A* Path cost = ", a_star_result.cost)
        print("A* Path:", [(pos.x, pos.y) for pos in a_star_path])
        print("A* Visited Nodes:", [(pos.x, pos.y) for pos in a_star_visited_nodes])
    else:
        print("A* Path does not exist")

if __name__ == '__main__':
    main()



