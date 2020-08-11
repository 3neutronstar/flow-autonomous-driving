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

    parser.add_argument(  # for rllib
        '--algorithm', type=str, default="DDPG",
    )  # choose algorithm in order to use
    parser.add_argument(
        '--num_cpus', type=int, default=1,
    )  # How many CPUs to use
    parser.add_argument(  # how many times you want to learn
        '--num_steps', type=int, default=10000,
    )  # How many total steps to perform learning over
    parser.add_argument(  # batch size
        '--rollout_size', type=int, default=100,
    )  # How many steps are in a training batch.
    parser.add_argument(
        '--checkpoint_path', type=str, default=None,
    )  # Directory with checkpoint to restore training from.
    parser.add_argument(
        '--no_render',
        action='store_true',
    )  # Specifies whether to run the simulation during runtime.
    return parser.parse_known_args(args)[0]
# rllib


def setup_exps_rllib(flow_params,
                     n_cpus,
                     n_rollouts,
                     policy_graphs=None,
                     policy_mapping_fn=None,
                     policies_to_train=None,
                     flags=None):
    from ray import tune
    from ray.tune.registry import register_env
    try:
        from ray.rllib.agents.agent import get_agent_class
    except ImportError:
        from ray.rllib.agents.registry import get_agent_class
    import torch

    from ray.rllib.agents.ddpg.ddpg import DEFAULT_CONFIG
    alg_run = "DDPG"
    agent_cls = get_agent_class(alg_run)
    config = deepcopy(agent_cls._default_config)
    config['framework'] = "torch"
    config['n_step'] = 1
    # model
    config['actor_hiddens'] = [400, 300]
    config['actor_lr'] = 0.0001  # in article 'ddpg'
    config['critic_hiddens'] = [400, 300]
    config['gamma'] = 0.99
    config['model']['fcnet_hiddens'] = [64, 64]
    # exploration
    config['exploration_config']['final_scale'] = 0.2
    config['exploration_config']['scale_timesteps'] = 1000000
    config['exploration_config']['ou_base_scale'] = 0.1
    config['exploration_config']['ou_theta'] = 0.15
    config['exploration_config']['ou_sigma'] = 0.2
    # optimization
    config['tau'] = 0.001
    config['l2_reg'] = 1e-2
    config['train_batch_size'] = 1024
    config['learning_starts'] = 3000
    # evaluation
    #config['evaluation_interval'] = 5
    config['buffer_size'] = 100000
    config['timesteps_per_iteration'] = 500
    # config["opt_type"]= "adam" for impala and APPO, default is SGD
    # TrainOneStep class call SGD -->execution_plan function can have policy update function
    print("cuda is available: ", torch.cuda.is_available())
    print('Beginning training.')
    print("==========================================")
    print("running algorithm: ", alg_run)  # "Framework: ", "torch"

    # save the flow params for replay
    flow_json = json.dumps(
        flow_params, cls=FlowParamsEncoder, sort_keys=True, indent=4)
    horizon = flow_params['env'].horizon
    config['horizon'] = horizon
    config['env_config']['flow_params'] = flow_json
    config['env_config']['run'] = alg_run

    # multiagent configuration
    if policy_graphs is not None:
        print("policy_graphs", policy_graphs)
        config['multiagent'].update({'policies': policy_graphs})
    if policy_mapping_fn is not None:
        config['multiagent'].update(
            {'policy_mapping_fn': tune.function(policy_mapping_fn)})
    if policies_to_train is not None:
        config['multiagent'].update({'policies_to_train': policies_to_train})

    create_env, gym_name = make_create_env(params=flow_params)

    # Register as rllib env
    register_env(gym_name, create_env)
    return alg_run, gym_name, config


def train_rllib(submodule, flags):
    """Train policies using the PPO algorithm in RLlib."""
    import ray
    from ray.tune import run_experiments
    start_time = timeit.default_timer()
    flow_params = submodule.flow_params
    print("the number of cpus: ", submodule.N_CPUS)
    n_cpus = submodule.N_CPUS
    n_rollouts = submodule.N_ROLLOUTS
    policy_graphs = getattr(submodule, "POLICY_GRAPHS", None)
    policy_mapping_fn = getattr(submodule, "policy_mapping_fn", None)
    policies_to_train = getattr(submodule, "policies_to_train", None)

    alg_run, gym_name, config = setup_exps_rllib(
        flow_params, n_cpus, n_rollouts,
        policy_graphs, policy_mapping_fn, policies_to_train, flags)

    ray.init(num_cpus=n_cpus + 1, object_store_memory=200 * 1024 * 1024)
    exp_config = {
        "run": alg_run,
        "env": gym_name,
        "config": {
            **config
        },
        "checkpoint_freq": 20,
        "checkpoint_at_end": True,
        "max_failures": 999,
        "stop": {
            "training_iteration": flags.num_steps,
        },
    }
    print(exp_config["config"]["framework"])
    if flags.checkpoint_path is not None:
        exp_config['restore'] = flags.checkpoint_path
    print("=================Configs=================")
    for key in exp_config["config"].keys():
        if key == "env_config":  # you can check env_config in exp_configs directory.
            continue
        # no checking None or 0 value at all.
        # elif exp_config["config"][key] == None or exp_config["config"][key] == 0:
        #    continue
        elif key == "model":  # model checking
            print("----model config----")
            for key_model in exp_config["config"]["model"].keys():
                print(key_model, ":", exp_config["config"]["model"][key_model])
                # no checking None or 0 value at all.
                # if exp_config["config"][key] == None or exp_config["config"][key] == 0:
                #    continue
        else:
            print(key, ":", exp_config["config"][key])
    print("=========================================")
    run_experiments({flow_params["exp_tag"]: exp_config})
    stop_time = timeit.default_timer()
    run_time = stop_time-start_time
    print("Training is Finished")
    print("total runtime: ", run_time)


def main(args):
    """Perform the training operations."""
    # Parse script-level arguments (not including package arguments).
    flags = parse_args(args)

    # Import relevant information from the exp_config script.
    module = __import__(
        "exp_configs.rl.singleagent", fromlist=[flags.exp_config])
    module_ma = __import__(
        "exp_configs.rl.multiagent", fromlist=[flags.exp_config])

    # rl part
    if hasattr(module, flags.exp_config):
        submodule = getattr(module, flags.exp_config)
        multiagent = False
    elif hasattr(module_ma, flags.exp_config):
        submodule = getattr(module_ma, flags.exp_config)
        multiagent = True
    else:
        raise ValueError("Unable to find experiment config.")

    # Perform the training operation.
    train_rllib(submodule, flags)


if __name__ == "__main__":
    main(sys.argv[1:])
