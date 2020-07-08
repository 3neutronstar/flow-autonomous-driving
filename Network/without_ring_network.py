"""Used as an example of ring experiment.

This example consists of 22 IDM cars on a ring creating shockwaves.
"""
from flow.controllers import IDMController, ContinuousRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.networks.ring import RingNetwork, ADDITIONAL_NET_PARAMS
from flow.networks import Network
import numpy as np
from numpy import pi, sin, cos, linspace


class ringring(Network):
    pass


vehicles = VehicleParams()
vehicles.add(
    veh_id="idm",
    acceleration_controller=(IDMController, {}),
    routing_controller=(ContinuousRouter, {}),
    num_vehicles=22)


class ringring(ringring):

    def specify_nodes(self, net_params):
        r = net_params.additional_params["st_line"]
        nodes = [{"id": "0", "x": +r, "y": 0},
                 {"id": "1", "x": 0, "y": -r},
                 {"id": "2", "x": -r, "y": 0},
                 {"id": "3", "x": 0, "y": +r}
                 ]
        return nodes

    def specify_edges(self, net_params):
        damg = np.array([[0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1],
                         [1, 0, 0, 0]])
        length = net_params.additional_params["length"]
        resolution = net_params.additional_params["resolution"]
        r = length / (2 * pi)
        edgelen = length / 4.
        # this will let us control the number of lanes in the network
        lanes = net_params.additional_params["num_lanes"]
        # speed limit of vehicles in the network
        speed_limit = net_params.additional_params["speed_limit"]
        # L: left, R: right, U: Up D:Down
        edges = list()
        # if you want to connect change num lanes, chage the number of damg component
        damg_cols = damg.shape[0]
        damg_rows = damg.shape[1]
        for n_cols in range(0, damg_cols):
            for n_rows in range(0, damg_rows):
                if(np.damg[n_cols][n_rows] > 0):
                    insert_id = str("e_"+n_cols+"_"+n_rows)
                    edges.append({"id": insert_id,
                                  "from": str(n_rows),
                                  "to": str(n_cols),
                                  "numLanes": damg[n_cols][n_rows],
                                  "speed": speed_limit,
                                  "length": edgelen,
                                  "shape": [(r*cos(t), r*sin(t))
                                            for t in linspace(n_rows*pi/2, pi/2+n_rows*pi/2, resolution)
                                            ]
                                  # if you want to customize call seperately
                                  })

        return edges
    

    def specify_routes(self, net_params):
        import numpy as np
        import sys
        is_py2 = sys.version[0] == '2'
        if is_py2:
            import Queue as queue
        else:
            import queue as queue

        damg = np.array([[0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                        [1, 0, 0, 0]])
        damg_rows = damg.shape[0]
        damg_cols = damg.shape[1]

        route = np.zeros((damg_rows, damg_cols), dtype=object)
       
        for n_rows in range(0, damg_cols):
            for n_cols in range(0, damg_cols):
                if(damg[n_rows][n_cols] > 0):
                    q = queue.Queue(damg_cols)
                    route[n_rows][n_cols] = q
                    route[n_rows][n_cols].put(str("e_"+str(n_rows)+"_"+str(n_cols)))

        rts = {}
        i = 0
        for n_rows in range(0, damg_rows):
            for n_cols in range(0, damg_cols):
                # sum_row = 1
                # for idx in range(0, damg_cols):
                #     sum_row += idx
                if n_rows != n_cols:
                    route_array = []
                    if route[n_rows][n_cols] != 0:
                        #while route[n_rows][n_cols].empty() or route[n_rows][n_cols] != 0:
                        while route[n_rows][n_cols].qsize():
                            route_array.append(route[n_rows][n_cols].get_nowait())
                    start_edge = str("e_"+str(n_rows)+"_"+str(n_cols))

                    rts[start_edge]=[(route_array)]
                else:
                    continue
        return rts
      

flow_params = dict(
    # name of the experiment
    exp_tag='ring',

    # name of the flow environment the experiment is running on
    env_name=AccelEnv,

    # name of the network class the experiment is running on
    network=ringring,  # ringring

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        render=True,
        sim_step=0.1,
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=1500,
        additional_params=ADDITIONAL_ENV_PARAMS,
    ),

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
    initial=InitialConfig(
        bunching=20,
    ),
)
