

def get_params(alg, config):
    if alg == "PPO":
        config["gamma"] = 0.999  # discount rate
        # in example config model#config["model"].update({"fcnet_hiddens": [32, 32, 32]})
        config["model"].update({"fcnet_hiddens": [4, 4]})
        config["use_gae"] = True  # truncated
        config["lambda"] = 0.97  # truncated value
        config["kl_target"] = 0.02  # d_target
        # M is default value -->minibatch size (sgd_minibatch_size)
        # K epoch with the number of updating theta
        config["num_sgd_iter"] = 10
        # horizon: T train time steps (T time steps fixed-length trajectory)
        config["sgd_minibatch_size"] = 128
        # ======= exploration =======
        config["exploration_config"] = {
            # TD3 uses simple Gaussian noise on top of deterministic NN-output
            # actions (after a possible pure random phase of n timesteps).
            "type": "GaussianNoise",
            # For how many timesteps should we return completely random
            # actions, before we start adding (scaled) noise?
            "random_timesteps": 100000,
            # Gaussian stddev of action noise for exploration.
            "stddev": 0.1,
            # Scaling settings by which the Gaussian noise is scaled before
            # being added to the actions. NOTE: The scale timesteps start only
            # after(!) any random steps have been finished.
            # By default, do not anneal over time (fixed 1.0).
            "initial_scale": 1.0,
            "final_scale": 0.02,
            "scale_timesteps": 1000,
        }
        return config

    elif alg == "DDPG":
        config['n_step'] = 5
        # config["l2_reg"] = 1e-2  # refer to ddpg paper(7. experiment)
        # config["tau"] = 0.001 # refer to ddpg paper(7. experiment -> for the soft target updates)
        # test based mountaincar continuous model
        # config["evaluation_interval"] = 5
        # config["exploration_config"]["final_scale"] = 0.02
        # config["exploration_config"]["scale_timesteps"] = 40000
        config['train_batch_size'] = 256
        return config
