from flow.controllers import IDMController, ContinuousRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams, SumoCarFollowingParams, SumoLaneChangeParams
from flow.core.params import VehicleParams, InFlows
from flow.envs import WaveAttenuationPOEnv
from Network.custom_network import Custom_Network

FLOW_RATE = 200
vehicles = VehicleParams()
vehicles.add(veh_id="human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(ContinuousRouter, {}),
             car_following_params=SumoCarFollowingParams(
                 speed_mode="obey_safe_speed",  # for safer behavior at the merges
                 tau=1.5  # larger distance between cars
             ),
             lane_change_params=SumoLaneChangeParams(lane_change_mode=1621),

             )
inflow = InFlows()
inflow.add(
    veh_type="human",
    edge="inflow_highway",
    vehs_per_hour=FLOW_RATE,
    departLane="free",
    departSpeed=8)
inflow.add(
    veh_type="human",
    edge="inflow_outmerge",
    vehs_per_hour=150,
    departLane="free",
    departSpeed=7.5)
sim_params = SumoParams(sim_step=0.1, render=True, )

initial_config = InitialConfig(spacing="uniform", bunching=40,
                               min_gap=5, perturbation=5.0,
                               )

ADDITIONAL_ENV_PARAMS = {
}

env_params = EnvParams(horizon=3600,
                       additional_params=ADDITIONAL_ENV_PARAMS
                       )

ADDITIONAL_NET_PARAMS = {

}
additional_net_params = ADDITIONAL_NET_PARAMS.copy()
net_params = NetParams(additional_params=additional_net_params)


flow_params = dict(
    # name of the experiment
    exp_tag='custom_network',
    # name of the flow environment the experiment is running on
    env_name=WaveAttenuationPOEnv,
    # name of the network class the experiment is running on
    network=Custom_Network,  # RingNetwork_custom
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
    initial=initial_config
)
