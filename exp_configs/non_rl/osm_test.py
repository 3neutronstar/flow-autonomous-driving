# This file is just for looking at network

from flow.envs import TestEnv
# the Experiment class is used for running simulations
from flow.core.experiment import Experiment

# all other imports are standard
from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams
from flow.core.params import SumoParams
from flow.core.params import TrafficLightParams

# map data
from Network.osm_network import OsmNetwork
from flow.envs.base import Env
import gym
from abc import ABCMeta
tl_logic = TrafficLightParams(baseline= False)
net_params = NetParams(
    osm_path='./Network/map.osm'

)
env_params = EnvParams()
sim_params = SumoParams(render=True)
initial_config = InitialConfig()
vehicles = VehicleParams()
vehicles.add('human', num_vehicles=80,)
 

flow_params = dict(
    exp_tag='osm_test',
    env_name=TestEnv,
    network=OsmNetwork,
    simulator='traci',
    sim=sim_params,
    env=env_params,
    net=net_params,
    veh=vehicles,
    initial=initial_config,
    tls = tl_logic
)

# Env에서 TestEnv 는 baseEnv를 부르고 base_env에서 traci network도 호출 # 거기서 이제 맵데이터를 꺼내올 수 있음
