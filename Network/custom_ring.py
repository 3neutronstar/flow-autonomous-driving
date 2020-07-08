from flow.controllers import IDMController, ContinuousRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.params import VehicleParams
from flow.envs.ring.accel import AccelEnv, ADDITIONAL_ENV_PARAMS
from flow.networks.ring import RingNetwork, ADDITIONAL_NET_PARAMS
from flow.networks import Network
import numpy as np
import sys
from numpy import pi, sin, cos, linspace


class ringring(Network):
    pass

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
      
