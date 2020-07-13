from flow.networks import Network


class Traffic_Network(Network):
    pass


ADDITIONAL_NET_PARAMS = {
    "length": 150,
    "lanes": 1,
    "speed_limit": 30,
    "resolution": 40,
}


class Traffic_Network(Traffic_Network):  # update my network class

    def specify_nodes(self, net_params):
        # one of the elements net_params will need is a "radius" value
        net_params.additional_params = ADDITIONAL_NET_PARAMS.copy()
        r = net_params.additional_params["length"]

        # specify the name and position (x,y) of each node
        nodes = [  # {"id": "LU", "x": -r,  "y": +r},  # 1
            # {"id": "RU",  "x": +r,  "y": +r},  # 2
            # {"id": "LD",    "x": -r,  "y": -r},  # 3
            # {"id": "RD",   "x": +r, "y": -r},  # 4
            {"id": "CL",   "x": -r, "y": 0},  # 5
            {"id": "CR",   "x": +r, "y": 0},  # 6
            {"id": "CU",   "x": 0, "y": r},  # 7
            {"id": "CD",   "x": 0, "y": -r},  # 8
            {"id": "IT",   "x": 0, "y": 0}]  # 9

        return nodes

    def specify_edges(self, net_params):
        net_params.additional_params = ADDITIONAL_NET_PARAMS.copy()
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
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge17",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CR",
                "to": "IT",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge18",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CD",
                "to": "IT",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge19",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "CU",
                "to": "IT",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge20",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CR",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge21",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CL",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge22",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CU",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            },
            {
                "id": "edge23",
                "numLanes": lanes,
                "speed": speed_limit,
                "from": "IT",
                "to": "CD",
                "length": edgelen,
                # "shape": [(r*cos(t), r*sin(t)) for t in linspace(pi, 3*pi/2, 40)]
            }

        ]

        return edges

    def specify_routes(self, net_params):
        rts = {"edge16": [(["edge16", "edge20"], 0.5), (["edge16", "edge22"], 0.5)],
               "edge17": [(["edge17", "edge21"], 0.5), (["edge16", "edge23"], 0.5)],
               "edge18": [(["edge18", "edge22"], 0.5), (["edge18", "edge21"], 0.5)],
               "edge19": [(["edge19", "edge23"], 0.5), (["edge19", "edge20"], 0.5)],
               "edge20": [(["edge20"])],
               "edge21": [(["edge21"])],
               "edge22": [(["edge22"])],
               "edge23": [(["edge23"])],

               }

        return rts
