

def get_params(alg, config):
    if alg == "ppo":
        return config

    elif alg == "ddpg":
        config['n_step'] = 5
        return config
