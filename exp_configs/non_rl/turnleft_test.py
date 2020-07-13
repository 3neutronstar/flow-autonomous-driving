from flow.controllers import IDMController, ContinuousRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams, SumoCarFollowingParams, SumoLaneChangeParams
from flow.core.params import VehicleParams, InFlows
from flow.envs import LaneChangeAccelEnv
from Network.turnleft_network import Turnleft_Network, ADDITIONAL_NET_PARAMS

FLOW_RATE = 100
vehicles = VehicleParams()

inflow = InFlows()
inflow.add(
    veh_type="human",
    edge="e_3_2",
    vehs_per_hour=FLOW_RATE,
    departLane="free",
    departSpeed=1)
inflow.add(
    veh_type="human_merge",
    edge="e_3_2",
    vehs_per_hour=200,
    departLane="1",
    departSpeed=0.7)
sim_params = SumoParams(sim_step=0.1, render=True, )

initial_config = InitialConfig(spacing="uniform", bunching=40,
                               min_gap=5, perturbation=5.0,
                               )

ADDITIONAL_ENV_PARAMS = {
    "max_accel": 1,
    "max_decel": 3,
    "lane_change_duration": 5,
    "ring_length": [70, 100],
    "target_velocity": 30,
    "sort_vehicles": False
}

env_params = EnvParams(horizon=3600,
                       additional_params=ADDITIONAL_ENV_PARAMS,

                       )
additional_net_params = ADDITIONAL_NET_PARAMS.copy()
net_params = NetParams(additional_params=additional_net_params)


flow_params = dict(
    # name of the experiment
    exp_tag='custom_network',
    # name of the flow environment the experiment is running on
    env_name=LaneChangeAccelEnv,
    # name of the network class the experiment is running on
    network=Turnleft_Network,  # RingNetwork_custom
    # simulator that is used by the experiment
    simulator='traci',
    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=sim_params,
    # environment related parameters (see flow.core.params.EnvParams)
    env=env_params,
    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        additional_params=ADDITIONAL_NET_PARAMS.copy(),
    ),
    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,
    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=initial_config,
)
