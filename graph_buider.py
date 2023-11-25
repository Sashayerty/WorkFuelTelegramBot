import matplotlib.pyplot as plt


def graph_builder(days, nums, dish):
    plt.subplots()
    plt.title(f'График {dish}')
    plt.bar(days, nums, color='darkorange')
    plt.savefig('save.png')
