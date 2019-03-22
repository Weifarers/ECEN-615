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

    # Gets the valences by summing across the rows.
    val_list = fill_matrix.sum(axis=0)
    # Generates a list of the nodes associated with each valence.
    node_tab = np.array([(i + 1) for i, node_val in enumerate(val_list)])
    # Sorts the nodes by the valence, and then lexicographically.
    perm_list = np.lexsort((node_tab, val_list))

    # Prints out the permutation list, and adds 1 to compensate for 0 indexing.
    print('The permutation order from Tinney Scheme 1 is:', *perm_list + 1)


main()
