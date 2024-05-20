from comparison import compare_algorithms
from chart import plot_comparison

if __name__ == '__main__':
    file_path = 'maze2.txt'
    results = compare_algorithms(file_path)
    plot_comparison(results)

    # Print results for reference
    for algorithm, cost, path_length, execution_time in results:
        print(f"{algorithm}: Cost = {cost}, Path Length = {path_length}, Execution Time = {execution_time:.4f} seconds")
