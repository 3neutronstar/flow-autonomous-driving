

def get_params(alg, config):
    if alg == "ppo":
        config["gamma"] = 0.999  # discount rate
        config["use_gae"] = True  # truncated
        config["lambda"] = 0.97  # truncated value
        config["kl_target"] = 0.02  # d_target
        # M is default value -->minibatch size (sgd_minibatch_size)
        # K epoch with the number of updating theta
        config["num_sgd_iter"] = 10
        # horizon: T train time steps (T time steps fixed-length trajectory)
        config["sgd_minibatch_size"] = 128
        return config

    elif alg == "ddpg":
        config['n_step'] = 1
        # model
        config['actor_hiddens'] = [64, 64]
        config['critic_hiddens'] = [64, 64]
        config['gamma'] = 0.99
        config['train_batch_size'] = 64
        # exploration
        config['exploration_config']['final_scale'] = 0.02
        config['exploration_config']['scale_timesteps'] = 10000
        config['exploration_config']['ou_base_scale'] = 0.1
        config['exploration_config']['ou_theta'] = 0.15
        config['exploration_config']['ou_sigma'] = 0.2
        # optimization
        config['tau'] = 0.001
        # evaluation
        config['evaluation_interval'] = 5
        return config
