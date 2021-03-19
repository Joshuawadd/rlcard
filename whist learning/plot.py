import matplotlib.pyplot as plt
import sys
import os
import csv

def dot_plot(log_dir):

    csv_path = './experiments/whist_dqn_result/' + log_dir + '/performance.csv'
    win_csv_path = './experiments/whist_dqn_result/' + log_dir + '/win_performance.csv'

    save_path_win = os.path.join(
        './experiments/whist_dqn_result/' + log_dir, 'win_fig_dots.png')
    save_path = os.path.join(
        './experiments/whist_dqn_result/' + log_dir, 'fig_dots.png')

    algorithm = 'DQN'

    with open(csv_path) as csvfile:
        #print(csv_path)
        reader = csv.DictReader(csvfile)
        xs = []
        ys = []
        for row in reader:
            xs.append(int(row['timestep']))
            ys.append(float(row['reward']))
        fig, ax = plt.subplots()
        ax.plot(xs, ys, label=algorithm, linestyle="", marker="o")
        ax.set(xlabel='timestep', ylabel='reward')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path)

    with open(win_csv_path) as csvfile:
        #print(win_csv_path)
        reader = csv.DictReader(csvfile)
        xs = []
        ys = []
        for row in reader:
            xs.append(int(row['timestep']))
            ys.append(float(row['win rate']))
        fig, ax = plt.subplots()
        ax.plot(xs, ys, label=algorithm, linestyle="",marker="o")
        ax.set(xlabel='timestep', ylabel='win rate')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path_win)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path_win)
