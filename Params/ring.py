

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
        config['n_step'] = 5
        return config
