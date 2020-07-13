# new file

"""Grid example."""
from flow.controllers import GridRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams
from flow.core.params import TrafficLightParams
from flow.core.params import SumoCarFollowingParams
from flow.core.params import InFlows
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.networks import TrafficLightGridNetwork
from flow.networks import Network


class IntersectionNetwork(Network):
    pass


ADDITIONAL_NET_PARAMS = {
    "length": 150,
    "lanes": 1,
    "speed_limit": 30,
    "resolution": 40,
}
USE_INFLOWS = False
v_enter = 10
inner_length = 300
long_length = 300
short_length = 300
n_rows = 1
n_columns = 1
num_cars_left = 20
num_cars_right = 20
num_cars_top = 20
num_cars_bot = 20
tot_cars = (num_cars_left + num_cars_right) * n_columns \
    + (num_cars_top + num_cars_bot) * n_rows
grid_array = {
    "short_length": short_length,
    "inner_length": inner_length,
    "long_length": long_length,
    "row_num": n_rows,
    "col_num": n_columns,
    "cars_left": num_cars_left,
    "cars_right": num_cars_right,
    "cars_top": num_cars_top,
    "cars_bot": num_cars_bot
}


class IntersectionNetwork(IntersectionNetwork):  # update my network class
    def __init__(self,
                 name,
                 vehicles,
                 net_params,
                 initial_config=InitialConfig(),
                 traffic_lights=TrafficLightParams()):
        """Initialize an n*m traffic light grid network."""
        optional = ["tl_logic"]
        for p in ADDITIONAL_NET_PARAMS.keys():
            if p not in net_params.additional_params and p not in optional:
                raise KeyError('Network parameter "{}" not supplied'.format(p))

        for p in ADDITIONAL_NET_PARAMS["grid_array"].keys():
            if p not in net_params.additional_params["grid_array"]:
                raise KeyError(
                    'Grid array parameter "{}" not supplied'.format(p))
    def specify_nodes(self, net_params):
        # one of the elements net_params will need is a "radius" value
        r = net_params.additional_params["length"]
        # specify the name and position (x,y) of each node
        nodes = [{"id": "CL",   "x": -r, "y": 0},  # 5
                 {"id": "CR",   "x": +r, "y": 0},  # 6
                 {"id": "CU",   "x": 0, "y": r},  # 7
                 {"id": "CD",   "x": 0, "y": -r},  # 8
                 {"id": "IT",   "x": 0, "y": 0}]  # 9
        return nodes

    def specify_edges(self, net_params):
        r = net_params.additional_params["length"]
        edgelen = r
        # this will let us control the number of lanes in the network
        lanes = net_params.additional_params["lanes"]
        # speed limit of vehicles in the network
        speed_limit = net_params.additional_params["speed_limit"]
        # L: left, R: right, U: Up D:Down
        edges = [
            {
                "id": "edge16",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CL",
                "to": "IT",
                "length": edgelen
            },
            {
                "id": "edge17",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CR",
                "to": "IT",
                "length": edgelen
            },
            {
                "id": "edge18",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CD",
                "to": "IT",
                "length": edgelen
            },
            {
                "id": "edge19",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CU",
                "to": "IT",
                "length": edgelen
            },
            {
                "id": "edge20",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CR",
                "length": edgelen
            },
            {
                "id": "edge21",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CL",
                "length": edgelen
            },
            {
                "id": "edge22",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CU",
                "length": edgelen
            },
            {
                "id": "edge23",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CD",
                "length": edgelen
            }
        ]
        return edges

    def specify_routes(self, net_params):
        rts = {"edge0": ["edge0", "edge1", "edge2", "edge3"],
               "edge1": ["edge1", "edge2", "edge3", "edge0"],
               "edge2": ["edge2", "edge3", "edge0", "edge1"],
               "edge3": ["edge3", "edge0", "edge1", "edge2"],
               "edge4": ["edge4", "edge7", "edge6", "edge5"],
               "edge5": ["edge5", "edge4", "edge7", "edge6"],
               "edge6": ["edge6", "edge5", "edge4", "edge7"],
               "edge7": ["edge7", "edge6", "edge5", "edge4"],
               "edge10": ["edge10", "edge15", "edge16", "edge17", "edge18"],
               "edge15": ["edge15", "edge16", "edge17", "edge17", "edge18"],
               "edge16": ["edge16", "edge17", "edge18", "edge17", "edge18"],
               "edge17": ["edge17", "edge18", "edge10", "edge17", "edge18"],
               "edge18": ["edge18", "edge10", "edge15", "edge17", "edge18"],
               "edge11": ["edge11", "edge19", "edge12", "edge13", "edge14"],
               "edge19": ["edge19", "edge12", "edge13", "edge14", "edge11"],
               "edge12": ["edge12", "edge13", "edge14", "edge11", "edge19"],
               "edge13": ["edge13", "edge14", "edge11", "edge19", "edge12"],
               "edge14": ["edge14", "edge11", "edge19", "edge12", "edge13"],
               }
        return rts

initial = InitialConfig(
    spacing='custom', lanes_distribution=float('inf'), shuffle=True)
inflow = InFlows()
inflow.add(
    veh_type='human_up',
    edge="edge19",
    probability=0.25,
    departLane='free',
    departSpeed=20)
inflow.add(
    veh_type='human_down',
    edge="edge18",
    probability=0.25,
    departLane='free',
    departSpeed=20)
inflow.add(
    veh_type='human_left',
    edge="edge16",
    probability=0.25,
    departLane='free',
    departSpeed=20)
inflow.add(
    veh_type='human_right',
    edge="edge17",
    probability=0.25,
    departLane='free',
    departSpeed=20)
net_params = NetParams(
    inflows=inflow,
    additional_params=additional_net_params)




vehicles = VehicleParams()
vehicles.add(
    veh_id="human",
    routing_controller=(GridRouter, {}),
    car_following_params=SumoCarFollowingParams(
        min_gap=2.5,
        decel=7.5,  # avoid collisions at emergency stops
    ),
    num_vehicles=tot_cars)
env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)
tl_logic = TrafficLightParams(baseline=False)
phases = [{
    "duration": "31",
    "minDur": "8",
    "maxDur": "45",
    "state": "GrGrGrGrGrGr"
}, {
    "duration": "6",
    "minDur": "3",
    "maxDur": "6",
    "state": "yryryryryryr"
}, {
    "duration": "31",
    "minDur": "8",
    "maxDur": "45",
    "state": "rGrGrGrGrGrG"
}, {
    "duration": "6",
    "minDur": "3",
    "maxDur": "6",
    "state": "ryryryryryry"
}]
tl_logic.add("center0", phases=phases, programID=1)
#tl_logic.add("center1", phases=phases, programID=1)
#tl_logic.add("center2", phases=phases, programID=1, tls_type="actuated")
additional_net_params = {
    "grid_array": grid_array,
    "speed_limit": 35,
    "horizontal_lanes": 1,
    "vertical_lanes": 1
}

flow_params = dict(
    # name of the experiment
    exp_tag='grid-intersection',
    # name of the flow environment the experiment is running on
    env_name=AccelEnv,
    # name of the network class the experiment is running on
    network=TrafficLightGridNetwork,
    # simulator that is used by the experiment
    simulator='traci',
    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        sim_step=0.1,
        render=True,
    ),
    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=1500,
        additional_params=ADDITIONAL_ENV_PARAMS.copy(),
    ),
    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=net_params,
    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,
    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=initial_config,
    # traffic lights to be introduced to specific nodes (see
    # flow.core.params.TrafficLightParams)
    tls=tl_logic,
)
