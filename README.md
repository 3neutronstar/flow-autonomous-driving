# flow-autonomous-driving
### Requirement
- flow-project : https://github.com/flow-project/flow
- anaconda : https://anaconda.com/

## How to Use
'''shell script
python simulate.py "test"
'''
This examples is for test the simulate.py for non-RL problem.

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
python train.py EXP_CONFIG --rl_trainer "rllib"
```
where `EXP_CONFIG` is the name of the experiment configuration file, as located in `exp_configs/rl/singleagent` or  `exp_configs/rl/multiagent.`

### stable-baselines3 (for only singel agent)
traffic light agents being trained through RL algorithms provided by OpenAI *stable-baselines3* by pytorch.

```shell script
python simulate.py EXP_CONFIG --rl_trainer "stable-baselines3"
```

## Contributors
