#This file is just for looking at network

from flow.envs import TestEnv
# the Experiment class is used for running simulations
from flow.core.experiment import Experiment

# all other imports are standard
from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams
from flow.core.params import SumoParams
# map data
from Network.osm_network import OsmNetwork

net_params = NetParams(
    osm_path='./Network/map.osm'
)
env_params = EnvParams()
sim_params = SumoParams(render=True)
initial_config = InitialConfig()
vehicles = VehicleParams()
vehicles.add('human', num_vehicles=1,)

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
)

#Env���� TestEnv �� baseEnv�� �θ��� base_env���� traci network�� ȣ��
# �ű⼭ ���� �ʵ����͸� ������ �� ���� 