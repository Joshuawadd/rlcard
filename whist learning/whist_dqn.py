''' An example of learning a Deep-Q Agent on UNO
'''

import tensorflow as tf
import os

import rlcard
from rlcard.agents import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils.utils import set_global_seed, tournament
from rlcard.utils import Logger
from tqdm import tqdm
import plot

import time

# Make environment
env = rlcard.make('whist', config={'seed': 0, 'allow_raw_data': True})
eval_env = rlcard.make('whist', config={'seed': 0, 'allow_raw_data': True})

#env = rlcard.make('whist', config={'seed': 0})
#eval_env = rlcard.make('whist', config={'seed': 0})

start = time.time()

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 1000
evaluate_num = 200
episode_num = 200000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

timestr = time.strftime("%Y%m%d-%H%M%S")

# The paths for saving the logs and learning curves
log_dir = './experiments/whist_dqn_result/' + timestr +'/'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents = []
    # for i in range(env.player_num):
    #     agent = DQNAgent(sess,
    #                     scope='dqn' + str(i),
    #                     action_num=env.action_num,
    #                     replay_memory_size=20000,
    #                     replay_memory_init_size=memory_init_size,
    #                     train_every=train_every,
    #                     state_shape=env.state_shape,
    #                     mlp_layers=[512, 512])
    #     agents.append(agent)

    agent = DQNAgent(sess,
                    scope='dqn',
                    action_num=env.action_num,
                    replay_memory_size=20000,
                    replay_memory_init_size=memory_init_size,
                    train_every=train_every,
                    state_shape=env.state_shape,
                    mlp_layers=[512, 512])
    
    random_agent_0 = RandomAgent(action_num=eval_env.action_num)
    random_agent_1 = RandomAgent(action_num=eval_env.action_num)
    #random_agent_2 = RandomAgent(action_num=eval_env.action_num)

    # env.set_agents(agents)
    # eval_env.set_agents([agents[0], random_agent_0, agents[2], random_agent_1])

    # env.set_agents([agent, agent_0, agent_1, agent_2])
    eval_env.set_agents([agent, agent_0, agent, agent_1])

    env.set_agents([agent, agent, agent, agent])
    # eval_env.set_agents([agent, agent, agent, agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    game_log_dir = log_dir + 'game_log.txt'

    file = open(game_log_dir,"w")
    file.close()

    eval_env.run_example(game_log_dir, is_training=False)

    for episode in tqdm(range(episode_num)):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        # for trajectory in trajectories:
        #     for ts in trajectory:
        #         agent.feed(ts)

        for i in range(env.player_num):
            for ts in trajectories[i]:
                agent.feed(ts)

        # for ts in trajectories[0]:
        #     #print(ts)
        #     agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            reward, win_rate = tournament(eval_env, evaluate_num)
            print(win_rate)
            logger.log_performance(
                env.timestep, reward[0], win_rate)

        if episode % 1000 == 0:
            logger.close_files()
            logger.plot('DQN')
            plot.dot_plot(timestr)
        
        if episode % (1000) == 0:
            if episode != 0:
                current_time = (time.time() - start)/60
                time_left = (episode_num - episode)/(episode/current_time)
                print()
                print(episode, current_time, episode/current_time)
                print("Time left:", time_left)
                print()
                eval_env.run_example(game_log_dir, is_training=False)

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')

    # Save model
    save_dir = 'models/whist_dqn'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))

    print((time.time() - start)/60)
