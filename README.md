# flow-autonomous-driving

### Requirement(Installment)

- anaconda : https://anaconda.com/
- flow-project : https://github.com/flow-project/flow
- ray-project(rllib) : https://github.com/ray-project/ray (need at least 0.8.6 is needed)
- pytorch : https://pytorch.org/
## How to Use


## RL examples
### RLlib (for multiagent and single agent)

```shell script
python train_rllib.py EXP_CONFIG
```

where `EXP_CONFIG` is the name of the experiment configuration file, as located in `exp_configs/rl/singleagent` or `exp_configs/rl/multiagent.`
### Visualizing Training Results
If you want to visualizing after training by rllib(ray), 
- First, ```conda activate flow``` to activate flow environment.
- Second,
```shell script
    python ~/flow-autonomous-driving/visualizer_rllib.py 
    ~/home/user/ray_results/EXP_CONFIG/experiment_name/ number_of_checkpoints
```
### Results for training Ring Network and Figure-Eight Network
#### PPO (Proximal Policy Optimization)

#### DDPG (Deep Deterministic Policy Gradient)
![DDPG img test](https://user-images.githubusercontent.com/59332148/91112418-0d53ec80-e6be-11ea-9ba5-40dfce5b9caf.png)



## non-RL examples

```shell script
python simulate.py EXP_CONFIG
```

where `EXP_CONFIG` is the name of the experiment configuration file, as located in `exp_configs/non_rl.`

If you want to run with options, use
```shell script
    python simulate.py EXP_CONFIG --num_runs n --no_render --gen_emission
```

## OSM - Output (Open Street Map)
![OSMtest_origin](https://user-images.githubusercontent.com/59332148/91113367-66248480-e6c0-11ea-8267-8dbef04475a5.png)
![OSMTest_Result](https://user-images.githubusercontent.com/59332148/91113369-66bd1b00-e6c0-11ea-878f-46735d543609.png)

[OpenStreetMap]https://www.openstreetmap.org/ 
If you want to use osm file for making network, _map.osm_ file should **replace** the same name of file in 'Network' directory.
You want to see their results, run this code.

```shell script
python simulate.py osm_test
```

After that, If you want to see those output file(XML), you could find in `~/flow/flow/core/kernel/debug/cfg/.net.cfg`




## Contributors
_BMIL in Soongsil Univ._
Prof. Kwon (Minhae Kwon), 
Minsoo Kang, 
Gihong Lee, 
Hyeonju Lim
