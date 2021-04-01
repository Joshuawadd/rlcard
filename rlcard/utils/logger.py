import os
import csv


class Logger(object):
    ''' Logger saves the running results and helps make plots from the results
    '''

    def __init__(self, log_dir):
        ''' Initialize the labels, legend and paths of the plot and log file.

        Args:
            log_path (str): The path the log files
        '''
        self.log_dir = log_dir
        self.txt_path = os.path.join(log_dir, 'log.txt')
        self.csv_path = os.path.join(log_dir, 'performance.csv')
        self.fig_path = os.path.join(log_dir, 'fig.png')

        self.txt_path_win = os.path.join(log_dir, 'win_log.txt')
        self.csv_path_win = os.path.join(log_dir, 'win_performance.csv')
        self.fig_path_win = os.path.join(log_dir, 'win_fig.png')
        self.fig_path_win_easy = os.path.join(log_dir, 'win_fig_easy.png')
        self.fig_path_win_medium = os.path.join(log_dir, 'win_fig_medium.png')
        self.fig_path_win_hard = os.path.join(log_dir, 'win_fig_hard.png')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.txt_file = open(self.txt_path, 'a')
        self.csv_file = open(self.csv_path, 'a')
        #self.txt_file_win = open(self.txt_path_win, 'w')
        self.csv_file_win = open(self.csv_path_win, 'a')
        fieldnames = ['timestep', 'reward']
        fieldnames_win = ['timestep', 'win rate', 'win rate easy', 'win rate medium', 'win rate hard']
        self.writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.writer_win = csv.DictWriter(self.csv_file_win, fieldnames=fieldnames_win)
        self.writer.writeheader()
        self.writer_win.writeheader()

    def log(self, text):
        ''' Write the text to log file then print it.
        Args:
            text(string): text to log
        '''
        self.txt_file.write(text+'\n')
        self.txt_file.flush()
        print(text)

    def log_performance(self, timestep, reward, win_rate):
        ''' Log a point in the curve
        Args:
            timestep (int): the timestep of the current point
            reward (float): the reward of the current point
        '''

        self.txt_file = open(self.txt_path, 'a')
        self.csv_file = open(self.csv_path, 'a')
        self.csv_file_win = open(self.csv_path_win, 'a')

        fieldnames = ['timestep', 'reward']
        fieldnames_win = ['timestep', 'win rate', 'win rate easy', 'win rate medium', 'win rate hard']
        self.writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.writer_win = csv.DictWriter(self.csv_file_win, fieldnames=fieldnames_win)

        self.writer.writerow({'timestep': timestep, 'reward': reward})
        self.writer_win.writerow({'timestep': timestep, 'win rate': win_rate[0], 'win rate easy': win_rate[1] , 'win rate medium': win_rate[2], 'win rate hard': win_rate[3]})
        print('')
        self.log('----------------------------------------')
        self.log('  timestep        |  ' + str(timestep))
        self.log('  reward          |  ' + str(reward))
        self.log('  win rate        |  ' + str(win_rate[0]))
        self.log('  win rate easy   |  ' + str(win_rate[1]))
        self.log('  win rate medium |  ' + str(win_rate[2]))
        self.log('  win rate hard   |  ' + str(win_rate[3]))
        self.log('----------------------------------------')

    def plot(self, algorithm):
        plot(self.csv_path, self.fig_path, algorithm)
        plot_win(self.csv_path_win, self.fig_path_win, 'win rate', algorithm)
        plot_win(self.csv_path_win, self.fig_path_win_easy, 'win rate easy', algorithm)
        plot_win(self.csv_path_win, self.fig_path_win_medium, 'win rate medium', algorithm)
        plot_win(self.csv_path_win, self.fig_path_win_hard, 'win rate hard', algorithm)

    def close_files(self):
        ''' Close the created file objects
        '''
        if self.txt_path is not None:
            self.txt_file.close()
        if self.csv_path is not None:
            self.csv_file.close()
        if self.csv_path_win is not None:
            self.csv_file_win.close()

def plot(csv_path, save_path, algorithm):
    ''' Read data from csv file and plot the results
    '''
    import matplotlib.pyplot as plt
    with open(csv_path) as csvfile:
        print(csv_path)
        reader = csv.DictReader(csvfile)
        xs = []
        ys = []
        for row in reader:
            xs.append(int(row['timestep']))
            ys.append(float(row['reward']))
        fig, ax = plt.subplots()
        ax.plot(xs, ys, label=algorithm)
        ax.set(xlabel='timestep', ylabel='reward')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path)
        plt.close(fig)

def plot_win(csv_path, save_path, row_name, algorithm):
    ''' Read data from csv file and plot the results
    '''
    import matplotlib.pyplot as plt
    with open(csv_path) as csvfile:
        print(csv_path)
        reader = csv.DictReader(csvfile)
        xs = []
        ys = []
        for row in reader:
            xs.append(int(row['timestep']))
            ys.append(float(row[row_name]))
        fig, ax = plt.subplots()
        ax.plot(xs, ys, label=algorithm)
        ax.set(xlabel='timestep', ylabel='win rate')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path)
        plt.close(fig)
