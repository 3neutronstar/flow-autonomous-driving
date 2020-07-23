# flow-autonomous-driving

### Requirement

- flow-project : https://github.com/flow-project/flow
- anaconda : https://anaconda.com/

## How to Use

## non-RL examples

```shell script
python simulate.py EXP_CONFIG
```

where `EXP_CONFIG` is the name of the experiment configuration file, as located in `exp_configs/non_rl.`

```shell script
 python simulate.py EXP_CONFIG --num_runs n --no_render --gen_emission
```

## RL examples

### RLlib (for multiagent and single agent)

```shell script
python train_rllib.py EXP_CONFIG
```

where `EXP_CONFIG` is the name of the experiment configuration file, as located in `exp_configs/rl/singleagent` or `exp_configs/rl/multiagent.`

### stable-baselines3 (for only singel agent)

traffic light agents being trained through RL algorithms provided by OpenAI _stable-baselines3_ by pytorch.

```shell script
python train_stablebaselines3.py EXP_CONFIG
```

## OSM - Output (Open Street Map)

If you want to use osm file for making network, _map.osm_ file should replace same name of file in 'Network' directory.
You want to see their results, run this code.

```shell script
python simulate.py osm_test
```

After that, If you want to see those output file(XML), you could find in '~/flow/flow/core/kernel/debug/cfg/~.net.cfg'

## Contributors
