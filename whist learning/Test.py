''' Another example of loading a pre-trained NFSP model on Leduc Hold'em
    Here, we directly load the model from model zoo
'''
import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard import models
from tqdm import tqdm
import tensorflow as tf
import os
from rlcard.agents import DQNAgent
from rlcard.utils import Logger
import plot

import time

# Make environment
env_1 = rlcard.make('whist', config={'seed': 0})
env_2 = rlcard.make('whist', config={'seed': 0})


# Set a global seed
set_global_seed(0)

# Here we directly load NFSP models from /models module
dqn_agents = models.load('whist-dqn').agents
dqn_agents_1 = models.load('whist-dqn').agents

rule_agents = models.load('whist-rule-v1').agents

random_agent_0 = RandomAgent(action_num=env_1.action_num)
random_agent_1 = RandomAgent(action_num=env_1.action_num)

timestr = time.strftime("%Y%m%d-%H%M%S")

log_dir = './experiments/whist_dqn_result/Model_Tests/' + timestr +'/'

logger = Logger(log_dir)

game_log_dir = log_dir + 'game_log.txt'

file = open(game_log_dir,"w")
file.close()

#Evaluate the performance. Play with random agents.
start_time = time.time()
evaluate_num = 100000
env_1.set_agents([dqn_agents, random_agent_0, dqn_agents, random_agent_1])
reward, win_rate = tournament(env_1, evaluate_num)
logger.log_performance(evaluate_num, reward[0], win_rate)
run_time = time.time() - start_time
env_1.run_example(game_log_dir, is_training=False)

print('Average reward against random agent: ', reward)
print('Runtime: ', run_time)

start_time = time.time()
evaluate_num = 100000
env_2.set_agents([dqn_agents_1, rule_agents[0], dqn_agents_1, rule_agents[1]])
reward, win_rate = tournament(env_2, evaluate_num)
logger.log_performance(evaluate_num, reward[0], win_rate)
run_time = time.time() - start_time
env_2.run_example(game_log_dir, is_training=False)

print('Average reward against rule agent: ', reward)
print('Runtime: ', run_time)
logger.close_files()