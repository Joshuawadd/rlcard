''' An example of learning a Deep-Q Agent on UNO
'''

import tensorflow as tf
import os

import rlcard
from rlcard.agents import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils.utils import set_global_seed, tournament
from rlcard.utils import Logger

import time

# Make environment
env = rlcard.make('whist', config={'seed': 0})
eval_env = rlcard.make('whist', config={'seed': 0})

start = time.time()

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 100000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir = './experiments/whist_dqn_result/'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_size=20000,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 512])
    agent_0 = RandomAgent(action_num=eval_env.action_num)
    agent_1 = RandomAgent(action_num=eval_env.action_num)
    agent_2 = RandomAgent(action_num=eval_env.action_num)

    #env.set_agents([agent, agent_0, agent_1, agent_2])
    eval_env.set_agents([agent, agent_0, agent, agent_1])

    env.set_agents([agent, agent, agent, agent])
    # eval_env.set_agents([agent, agent, agent, agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    file = open("./experiments/whist_dqn_result/game_log.txt","w")
    file.close()

    eval_env.run_example(is_training=False)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        # for trajectory in trajectories:
        #     for ts in trajectory:
        #         agent.feed(ts)

        for ts in trajectories[0]:
            #print(ts)
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(
                env.timestep, tournament(eval_env, evaluate_num)[0])
        
        if episode % (evaluate_every*10) == 0:
            current_time = (time.time() - start)/60
            print()
            print(episode, current_time, episode/current_time)
            print()
            eval_env.run_example(is_training=False)

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
