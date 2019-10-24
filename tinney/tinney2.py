import sys
import numpy as np


def main():

    # Reading in the data file.
    filename = sys.argv[1]
    y_bus = open(filename, 'r')

    # Generating the list of all the connections from the y_bus.
    line_list = []
    for i, line in enumerate(y_bus):
        # Skips the first two lines of the .txt, which do not contain connections.
        if i < 2:
            continue
        # Gets the starting bus and ending bus.
        else:
            curr_idx = line.split()
            start_bus = int(curr_idx[1].replace(',', ''))
            end_bus = int(curr_idx[2].replace(')', ''))
            # Generates a coordinate containing the starting bus and ending bus.
            line_connect = (start_bus, end_bus)
            # Appends these coordinates to a list of all lines.
            line_list.append(line_connect)

    # Gets the number of buses.
    num_bus = max(max(line_list))

    # Creates the matrix with fills.
    fill_matrix = np.zeros((num_bus, num_bus), dtype=int)
    for i, line in enumerate(line_list):
        row_idx = line[0]
        col_idx = line[1]
        fill_matrix[row_idx - 1, col_idx - 1] = 1

    # Initializes permutation list.
    perm_list = []
    # Gets a list of all of the buses.
    index = list(np.arange(1, num_bus + 1, 1))

    # Iterates through the number of buses (max number of iterations for Tinney Scheme 2).
    for bus_idx in range(num_bus):
        # Generates a list of the valences by summing across the rows.
        val_list = fill_matrix.sum(axis=0)
        # Generates a list of the nodes associated with each valence.
        node_tab = np.array([(i + 1) for i, node_val in enumerate(val_list)])
        # Sorts the nodes by the valence, and then lexicographically.
        node_list = np.lexsort((node_tab, val_list))
        # Appends the first node to the permutation list.
        removed_node = index[node_list[0]]
        perm_list.append(removed_node)
        # Gets the column associated with the removed node.
        remove_col = fill_matrix[:, node_list[0]]
        # Gets all the indices that are currently connected to the node we've removed.
        indices = [i for i, row_val in enumerate(remove_col) if row_val == 1]
        # Looks through all current  nodes and creates any fills that are necessary.
        for i in range(len(indices)):
            node_one = indices[i]
            for j in range(i + 1, len(indices)):
                node_two = indices[j]
                if node_one != node_list[0] and node_two != node_list[0]:
                    fill_matrix[node_one, node_two] = 1
                    fill_matrix[node_two, node_one] = 1
        # Removes the node from the indices we are considering.
        index.remove(removed_node)
        # Removes the row and column associated with the removed node.
        fill_matrix = np.delete(fill_matrix, node_list[0], axis=0)
        fill_matrix = np.delete(fill_matrix, node_list[0], axis=1)

    print('The permutation order from Tinney Scheme 2 is:', *perm_list)


main()
