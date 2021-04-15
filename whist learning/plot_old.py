import matplotlib.pyplot as plt
import sys
import csv
import os

file_name = sys.argv[1]
csv_path = './experiments/whist_dqn_result/' + file_name + '/win_performance.csv'
save_path = './experiments/whist_dqn_result/' + file_name + '/win_fig_all.png'

with open(csv_path) as csvfile:
    # print(csv_path)
    reader = csv.DictReader(csvfile)
    xs = []
    ys1 = []
    ys2 = []
    ys3 = []
    i = 0
    for row in reader:
        xs.append(i)
        ys1.append(float(row['win rate easy']))
        ys2.append(float(row['win rate medium']))
        ys3.append(float(row['win rate hard']))
        i += 1000
    fig, ax = plt.subplots()
    ax.plot(xs, ys1, label='Easy')
    ax.plot(xs, ys2, label='Medium')
    ax.plot(xs, ys3, label='Hard')
    ax.set(xlabel='episodes', ylabel='win rate')
    ax.legend()
    ax.grid()

    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    fig.savefig(save_path)
    plt.close(fig)
