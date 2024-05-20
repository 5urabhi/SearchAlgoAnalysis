import matplotlib.pyplot as plt

def plot_comparison(results):
    algorithms, costs, path_lengths, execution_times = zip(*results)

    # Convert None to 0 for plotting
    costs = [0 if x is None else x for x in costs]
    path_lengths = [0 if x is None else x for x in path_lengths]
    execution_times = [0 if x is None else x for x in execution_times]

    # Plot Path Length
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, path_lengths, color='skyblue')
    plt.xlabel('Algorithms')
    plt.ylabel('Path Length')
    plt.title('Path Length Comparison')
    plt.savefig('comparison_charts/path_length_comparison.png')
    plt.close()

    # Plot Costs
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, costs, color='lightgreen')
    plt.xlabel('Algorithms')
    plt.ylabel('Path Cost')
    plt.title('Path Cost Comparison')
    plt.savefig('comparison_charts/path_cost_comparison.png')
    plt.close()

    # Plot Execution Time
    print("Execution Times: ", execution_times)  # Debugging statement
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, execution_times, color='salmon')
    plt.xlabel('Algorithms')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison')
    plt.savefig('comparison_charts/execution_time_comparison.png')
    plt.close()

if __name__ == '__main__':
    file_path = 'maze2.txt'
    # results = compare_algorithms(file_path)
    # plot_comparison(results)

    # # Print results for reference
    # for algorithm, cost, path_length, execution_time in results:
    #     print(f"{algorithm}: Cost = {cost}, Path Length = {path_length}, Execution Time = {execution_time:.4f} seconds")
