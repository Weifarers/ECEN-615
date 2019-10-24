import numpy as np


def main():
    # Initialize the A matrix: From Bus = 1, To Bus = -1.
    a_matrix = np.matrix([[1, -1, 0, 0, 0, 0],
                          [1, 0, -1, 0, 0, 0],
                          [0, 1, -1, 0, 0, 0],
                          [0, 1, 0, -1, 0, 0],
                          [0, 1, 0, 0, -1, 0],
                          [0, 1, 0, 0, 0, -1],
                          [0, 0, 1, -1, 0, 0],
                          [0, 0, 0, 1, -1, 0],
                          [0, 0, 0, 0, -1, 0],
                          [0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 1]])
    # Initialize all reactance values.
    x_val = np.array([.06, .24, .18, .18, .12, .06, .03, .24, .06, .24, .24], dtype=float)
    x_matrix = np.diag(x_val)
    # Calculate the susceptance values.
    b_matrix = -np.linalg.inv(x_matrix)
    # Calculates the injection shift factors.
    bp_matrix = np.transpose(a_matrix)*b_matrix*a_matrix
    isf_matrix = b_matrix*a_matrix*np.linalg.inv(bp_matrix)
    print("The Injection Shift Factors are: \n", np.around(isf_matrix, decimals=4))

    # Prints the PTDFs' for transactions between Bus 2 and Bus 7.
    print("The PTDFs' for a transaction between Bus 2 and Bus 7 are: \n",
          np.transpose(np.around(isf_matrix[:, 1], decimals=4)))

    # Calculating the LODFs' for an outage between Bus 2 and Bus 5.
    ptdf25 = isf_matrix[:, 1] - isf_matrix[:, 4]
    lodf25 = ptdf25/(1 - ptdf25[4])
    lodf25[4] = -1
    print("The LODFs' for an outage between Bus 2 and Bus 5 are: \n",
          np.transpose(np.around(lodf25, decimals=4)))

    # Calculating the LODFs' for a double outage between Bus 2/Bus 5, and Bus 2/Bus 4
    # Gets the LODFs' for an outage between Bus 2 and Bus 4.
    ptdf24 = isf_matrix[:, 1] - isf_matrix[:, 3]
    lodf24 = ptdf24/(1 - ptdf24[3])
    print(lodf24[3])
    lodf24[3] = -1

    # Calculates the LODFs' for the double outage.
    # In this case, the outage for Bus 2 to Bus 5 is k1, and the outage for Bus 2 to Bus 4 is k2.
    d_k1_k2 = np.matrix([[1, -lodf24.item(4)], [-lodf25.item(3), 1]])
    d_k2_k1 = np.matrix([[1, -lodf25.item(3)], [-lodf24.item(4), 1]])
    # The LODFs' for a 2->5 and then 2->4 contingency are different from a 2->4 then 2->5 contingency.
    lodf2425 = []
    lodf2524 = []
    for i in range(len(lodf24)):
        l25 = lodf25[i].item()
        l24 = lodf24[i].item()
        # Calculates both LODFs' simultaneously.
        lodf_temp = np.matrix([[l25, l24]])*np.linalg.inv(d_k1_k2)
        # Stores the 2->4 then 2->5 LODFs.
        lodf2425.append(np.asarray(lodf_temp)[0][0])
        # Stores the 2->5 then 2->4 LODFs.
        lodf2524.append(np.asarray(lodf_temp)[0][1])
    print("The LODFs' for a double outage between Bus 2 and 5 and then Bus 2 and 4 are: \n",
          np.around(lodf2524, decimals=4))
    print("The LODFs' for a double outage between Bus 2 and 4 and then Bus 2 and 5 are: \n",
          np.around(lodf2425, decimals=4))


main()
