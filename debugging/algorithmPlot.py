def plotHistory(history):
    # Plot History
    import matplotlib.pyplot as plt
    plt.plot(history)
    plt.ylabel('score')
    plt.xlabel('sample')
    plt.show()