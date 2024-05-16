import matplotlib.pyplot as plt
import queue

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

def load_maze(file_path):
    maze = []
    with open(file_path, 'r') as file:
        for line in file:
            maze.append([int(x) for x in line.strip().split(',')])
    return maze

def plot_maze(maze, path, title, file_name):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(maze, cmap='binary')
    for node in path:
        ax.scatter(node.y, node.x, color='red', s=100)  # y, x to align with column-row indexing
    ax.set_title(title)
    plt.savefig(file_name)
    plt.close()

def trace_path(end_node):
    path = []
    current = end_node
    while current:
        path.append(current.pos)
        current = current.parent
    return path[::-1]  # Return reversed path

def gbfs(Grid, dest: Grid_Position, start: Grid_Position):
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]
    visited_blocks = [[False for _ in range(len(Grid[0]))] for _ in range(len(Grid))]
    q = queue.PriorityQueue()
    start_node = Node(start, 0)
    q.put((0, start_node))
    visited_blocks[start.x][start.y] = True

    while not q.empty():
        _, current_node = q.get()
        if current_node.pos.x == dest.x and current_node.pos.y == dest.y:
            return current_node

        for dx, dy in zip(adj_cell_x, adj_cell_y):
            nx, ny = current_node.pos.x + dx, current_node.pos.y + dy
            if 0 <= nx < len(Grid) and 0 <= ny < len(Grid[0]) and Grid[nx][ny] == 1:
                if not visited_blocks[nx][ny]:
                    visited_blocks[nx][ny] = True
                    neighbor = Node(Grid_Position(nx, ny), current_node.cost + 1, current_node)
                    h = heuristic_value(neighbor.pos, dest)
                    q.put((h, neighbor))
    return None

def a_star(maze, end, start):
    # Define movement vectors for adjacent cells
    adj_cell_x = [-1, 0, 0, 1]
    adj_cell_y = [0, -1, 1, 0]

    open_set = queue.PriorityQueue()
    closed = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start_node = Node(start, 0)
    open_set.put((0, start_node))
    closed[start.x][start.y] = True

    while not open_set.empty():
        _, current_node = open_set.get()
        if current_node.pos.x == end.x and current_node.pos.y == end.y:
            return current_node

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
    return None

def main():
    file_path = 'maze_1.txt'
    maze = load_maze(file_path)
    destination = Grid_Position(12, 19)
    starting_position = Grid_Position(1, 19)
    
    gbfs_result = gbfs(maze, destination, starting_position)
    if gbfs_result:
        path = trace_path(gbfs_result)
        plot_maze(maze, path, "Greedy Best-First Search Solution", "gbfs_solution.png")
        print("GBFS Path cost = ", gbfs_result.cost)
    else:
        print("GBFS Path does not exist")

    a_star_result = a_star(maze, destination, starting_position)
    if a_star_result:
        path = trace_path(a_star_result)
        plot_maze(maze, path, "A* Search Solution", "a_star_solution.png")
        print("A* Path cost = ", a_star_result.cost)
    else:
        print("A* Path does not exist")

if __name__ == '__main__':
    main()
