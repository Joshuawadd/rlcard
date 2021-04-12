import tensorflow as tf
import os

import rlcard
from rlcard.agents import NFSPAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger
from tqdm import tqdm
import plot

import time

# Make environment
env = rlcard.make('whist', config={'seed': 0, 'allow_raw_data': True})
eval_env = rlcard.make('whist', config={'seed': 0, 'allow_raw_data': True})

start = time.time()

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 1000
evaluate_num = 3000
episode_num = 400000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 64

# The paths for saving the logs and learning curves
timestr = time.strftime("%Y%m%d-%H%M%S")

# The paths for saving the logs and learning curves
log_dir = './experiments/whist_nfsp_result/' + timestr +'/'

# Set a global seed
set_global_seed(0)

print(env.player_num)

with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents = []
    for i in range(env.player_num):
        agent = NFSPAgent(sess,
                          scope='nfsp' + str(i),
                          action_num=env.action_num,
                          state_shape=env.state_shape,
                          hidden_layers_sizes=[512,1024,2048,1024,512],
                          anticipatory_param=0.5,
                          batch_size=256,
                          rl_learning_rate=0.00005,
                          sl_learning_rate=0.00001,
                          min_buffer_size_to_learn=memory_init_size,
                          q_replay_memory_size=int(1e5),
                          q_replay_memory_init_size=memory_init_size,
                          train_every = train_every,
                          q_train_every=train_every,
                          q_batch_size=256,
                          q_mlp_layers=[512,1024,2048,1024,512])
        agents.append(agent)
    random_agent_0 = RandomAgent(action_num=eval_env.action_num)
    random_agent_1 = RandomAgent(action_num=eval_env.action_num)
    random_agent_2 = RandomAgent(action_num=eval_env.action_num)

    env.set_agents(agents)
    eval_env.set_agents([agents[0], random_agent_0, agents[2], random_agent_2])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curvefrom rlcard.agents.random_agent import RandomAgent

    logger = Logger(log_dir)

    game_log_dir = log_dir + 'game_log.txt'

    file = open(game_log_dir,"w")
    file.close()

    eval_env.run_example(game_log_dir, is_training=False)

    for episode in tqdm(range(episode_num)):

        # First sample a policy for the episode
        for agent in agents:
            agent.sample_episode_policy()

        # Generate data from the environment
        trajectories, _, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for i in range(env.player_num):
            for ts in trajectories[i]:
                agents[i].feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            reward, win_rate = tournament(eval_env, evaluate_num)
            #print(win_rate)
            logger.log_performance(
                episode, reward[0], win_rate)

        if episode % 1000 == 0:
            logger.close_files()
            logger.plot('NFSP')
            plot.dot_plot(log_dir, 'NFSP')

        if episode % 1000 == 0:
            if episode != 0:
                # current_time = (time.time() - start)/60
                # time_left = (episode_num - episode)/(episode/current_time)
                # print()
                # print(episode, current_time, episode/current_time)
                # print("Time left:", time_left)
                # print()
                # dqn = False
                eval_env.run_example(game_log_dir, is_training=False)


    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('NFSP')
    
    # Save model
    save_dir = 'models/whist_nfsp'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
    
