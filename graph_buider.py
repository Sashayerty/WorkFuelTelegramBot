import matplotlib.pyplot as plt


def graph_builder(days, nums, dish):
    fig, ax = plt.subplots()
    ax.set_title(f'График {dish}')
    ax.grid()
    ax.plot(days, [i[0] for i in nums])
    plt.savefig('save.png')
