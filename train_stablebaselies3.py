import argparse
import json
import os
import sys
from time import strftime
from copy import deepcopy
import numpy as np
import timeit
import torch
from flow.core.util import ensure_dir
from flow.utils.registry import env_constructor
from flow.utils.rllib import FlowParamsEncoder, get_flow_params
from flow.utils.registry import make_create_env
from Experiment.experiment import Experiment

# stablebaseline_ddpg


def parse_args(args):
    """Parse training options user can specify in command line.
    Returns
    -------
    argparse.Namespace
        the output parser object
    """
    # parser = argparse.ArgumentParser(
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     description="Parse argument used when running a Flow simulation.",
    #     epilog="python simulate.py EXP_CONFIG")
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Parse argument used when running a Flow simulation.",
        epilog="python simulate.py EXP_CONFIG")
    # required input parameters
    parser.add_argument(
        'exp_config', type=str,
    )  # Name of the experiment configuration file, as located in
    # exp_configs/non_rl exp_configs/rl/singleagent or exp_configs/rl/multiagent.'

    # optional input parameters (for RL parser)
    parser.add_argument(
        '--rl_trainer', type=str, default="stable-baselines3",
    )  # the RL trainer to use. either  or Stable-Baselines3
    parser.add_argument(  # for rllib
        '--algorithm', type=str, default="PPO",
    )  # choose algorithm in order to use
    parser.add_argument(
        '--num_cpus', type=int, default=1,
    )  # How many CPUs to use
    parser.add_argument(  # how many times you want to learn
        '--num_steps', type=int, default=1500,
    )  # How many total steps to perform learning over
    parser.add_argument(  # batch size
        '--rollout_size', type=int, default=100,
    )  # How many steps are in a training batch.
    parser.add_argument(
        '--checkpoint_path', type=str, default=None,
    )  # Directory with checkpoint to restore training from.

    # for non-RL parser
    parser.add_argument(
        '--gen_emission',
        action='store_true',
    )  # Specifies whether to generate an emission file from the simulation.
    parser.add_argument(
        '--num_runs', type=int, default=1,
    )  # Number of simulations to run. Defaults to 1.
    parser.add_argument(
        '--no_render',
        action='store_true',
    )  # Specifies whether to run the simulation during runtime.
    parser.add_argument(  # after using rl rendering the result
        '--rl_render', type=str, default=None,
    )  # choose algorithm in order to use
    return parser.parse_known_args(args)[0]
# rllib


def run_model_stablebaseline3(flow_params,
                              num_cpus=1,
                              rollout_size=5,
                              num_steps=5):
    from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
    from stable_baselines3 import PPO
    from stable_baselines3.ppo import MlpPolicy
    import torch.nn as nn

    if num_cpus == 1:
        constructor = env_constructor(params=flow_params, version=0)()
        # The algorithms require a vectorized environment to run
        env = DummyVecEnv([lambda: constructor])
    else:
        env = SubprocVecEnv([env_constructor(params=flow_params, version=i)
                             for i in range(num_cpus)])

    train_model = PPO(MlpPolicy, env=env, verbose=1, n_epochs=rollout_size,
                      tensorboard_log="./PPO_tensorboard/", device="cuda")  # cpu, gpu selection
    # automatically select gpu
    train_model.learn(total_timesteps=num_steps*rollout_size)  #
    return train_model


def train_stable_baselines3(submodule, flags):
    """Train policies using the PPO algorithm in stable-baselines3."""
    from stable_baselines3.common.vec_env import DummyVecEnv
    from stable_baselines3 import PPO
    import torch
    start_time = timeit.default_timer()
    flow_params = submodule.flow_params
    # Path to the saved files
    exp_tag = flow_params['exp_tag']
    result_name = '{}/{}'.format(exp_tag, strftime("%Y-%m-%d-%H:%M:%S"))

    # Perform training.
    print("cuda is available: ", torch.cuda.is_available())
    print('Beginning training.')
    print("==========================================")
    model = run_model_stablebaseline3(
        flow_params, flags.num_cpus, flags.rollout_size, flags.num_steps)

    # Save the model to a desired folder and then delete it to demonstrate
    # loading.
    print('Saving the trained model!')
    path = os.path.realpath(os.path.expanduser('~/baseline_results'))
    ensure_dir(path)
    save_path = os.path.join(path, result_name)
    model.save(save_path)
    # dump the flow params
    # check time for choose GPU and CPU
    stop_time = timeit.default_timer()
    run_time = stop_time-start_time
    with open(os.path.join(path, result_name) + '.json', 'w') as outfile:
        json.dump(flow_params, outfile,
                  cls=FlowParamsEncoder, sort_keys=True, indent=4)

    # Replay the result by loading the model
    print('Loading the trained model and testing it out!')
    model.load(save_path)
    flow_params = get_flow_params(os.path.join(path, result_name) + '.json')

    flow_params['sim'].render = False
    flow_params['env'].horizon = 1500  # 150seconds operation
    env = env_constructor(params=flow_params, version=0)()
    # The algorithms require a vectorized environment to run
    eval_env = DummyVecEnv([lambda: env])
    obs = eval_env.reset()
    reward = 0
    for _ in range(flow_params['env'].horizon):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = eval_env.step(action)
        reward += rewards
    print("--------------------------------------------------------")
    flow_params['sim'].render = True
    simulation = Experiment(flow_params)
    simulation.run(num_runs=1)
    print('the final reward is {}'.format(reward))
    print("total run_time:", run_time, "s")


def main(args):
    """Perform the training operations."""
    # Parse script-level arguments (not including package arguments).
    flags = parse_args(args)

    # Import relevant information from the exp_config script.
    module = __import__(
        "exp_configs.rl.singleagent", fromlist=[flags.exp_config])

    if hasattr(module, flags.exp_config):
        submodule = getattr(module, flags.exp_config)
        multiagent = False
    else:
        raise ValueError("Unable to find experiment config.")

    # Perform the training operation.
    train_stable_baselines3(submodule, flags)


if __name__ == "__main__":
    main(sys.argv[1:])
