from search_algorithm.A_star import a_star
from search_algorithm.BFS import bfs
from search_algorithm.DFS import dfs
from search_algorithm.gbfs import gbfs, Grid_Position, trace_path, load_maze, plot_maze
from search_algorithm.chart import plot_comparison
import time

def compare_algorithms(file_path):
    maze, starting_position, destination = load_maze(file_path)
    
    results = []

    # Run A* Search
    start_time = time.time()
    a_star_result, a_star_visited_nodes = a_star(maze, destination, starting_position)
    a_star_time = time.time() - start_time
    if a_star_result:
        a_star_path = trace_path(a_star_result)
        plot_maze(maze, a_star_visited_nodes, a_star_path, "A* Search Solution", "path/a_star_solution.png", starting_position, destination)
        results.append(('A*', a_star_result.cost, len(a_star_path), a_star_time))
    else:
        results.append(('A*', None, None, a_star_time))

    # Run BFS
    start_time = time.time()
    bfs_solution, bfs_num_explored, bfs_explored = bfs(file_path)
    bfs_time = time.time() - start_time
    if bfs_solution:
        bfs_path = bfs_solution[1]
        plot_maze(maze, bfs_explored, bfs_path, "BFS Solution", "path/bfs_solution.png", starting_position, destination)
        results.append(('BFS', len(bfs_path), len(bfs_path), bfs_time))
    else:
        results.append(('BFS', None, None, bfs_time))

    # Run DFS
    start_time = time.time()
    dfs_solution, dfs_num_explored, dfs_explored = dfs(file_path)
    dfs_time = time.time() - start_time
    if dfs_solution:
        dfs_path = dfs_solution[1]
        plot_maze(maze, dfs_explored, dfs_path, "DFS Solution", "path/dfs_solution.png", starting_position, destination)
        results.append(('DFS', len(dfs_path), len(dfs_path), dfs_time))
    else:
        results.append(('DFS', None, None, dfs_time))

    # Run GBFS
    start_time = time.time()
    gbfs_result, gbfs_visited_nodes = gbfs(maze, destination, starting_position)
    gbfs_time = time.time() - start_time
    if gbfs_result:
        gbfs_path = trace_path(gbfs_result)
        plot_maze(maze, gbfs_visited_nodes, gbfs_path, "Greedy Best-First Search Solution", "path/gbfs_solution.png", starting_position, destination)
        results.append(('GBFS', gbfs_result.cost, len(gbfs_path), gbfs_time))
    else:
        results.append(('GBFS', None, None, gbfs_time))

    return results