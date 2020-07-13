from flow.networks import Network
from flow.core.params import InitialConfig
from flow.core.params import TrafficLightParams
from collections import defaultdict

ADDITIONAL_NET_PARAMS = {
    # dictionary of traffic light grid array data
    "grid_array": {
        # number of horizontal rows of edges
        "row_num": 2,
        # number of vertical columns of edges
        "col_num": 2,
        # length of inner edges in the traffic light grid network
        "inner_length": None,
        # length of edges where vehicles enter the network
        "short_length": None,
        # length of edges where vehicles exit the network
        "long_length": None,
        # number of cars starting at the edges heading to the top
        "cars_top": 20,
        # number of cars starting at the edges heading to the bottom
        "cars_bot": 20,
        # number of cars starting at the edges heading to the left
        "cars_left": 20,
        # number of cars starting at the edges heading to the right
        "cars_right": 20,
    },
    # number of lanes in the horizontal edges
    "horizontal_lanes": 1,
    # number of lanes in the vertical edges
    "vertical_lanes": 1,
    # speed limit for all edges, may be represented as a float value, or a
    # dictionary with separate values for vertical and horizontal lanes
    "speed_limit": {
        "horizontal": 35,
        "vertical": 35
    }
}


class myEnvNetwork(Network):
    """Traffic Light Grid network class.
    The traffic light grid network consists of m vertical lanes and n
    horizontal lanes, with a total of nxm intersections where the vertical
    and horizontal edges meet.
    Requires from net_params:
    * **grid_array** : dictionary of grid array data, with the following keys
      * **row_num** : number of horizontal rows of edges
      * **col_num** : number of vertical columns of edges
      * **inner_length** : length of inner edges in traffic light grid network
      * **short_length** : length of edges that vehicles start on
      * **long_length** : length of final edge in route
      * **cars_top** : number of cars starting at the edges heading to the top
      * **cars_bot** : number of cars starting at the edges heading to the
        bottom
      * **cars_left** : number of cars starting at the edges heading to the
        left
      * **cars_right** : number of cars starting at the edges heading to the
        right
    * **horizontal_lanes** : number of lanes in the horizontal edges
    * **vertical_lanes** : number of lanes in the vertical edges
    * **speed_limit** : speed limit for all edges. This may be represented as a
      float value, or a dictionary with separate values for vertical and
      horizontal lanes."""

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

        # retrieve all additional parameters
        # refer to the ADDITIONAL_NET_PARAMS dict for more documentation
        self.vertical_lanes = net_params.additional_params["vertical_lanes"]
        self.horizontal_lanes = net_params.additional_params[
            "horizontal_lanes"]
        self.speed_limit = net_params.additional_params["speed_limit"]
        if not isinstance(self.speed_limit, dict):
            self.speed_limit = {
                "horizontal": self.speed_limit,
                "vertical": self.speed_limit
            }

        self.grid_array = net_params.additional_params["grid_array"]
        self.row_num = self.grid_array["row_num"]
        self.col_num = self.grid_array["col_num"]
        self.inner_length = self.grid_array["inner_length"]
        self.short_length = self.grid_array["short_length"]
        self.long_length = self.grid_array["long_length"]
        self.cars_heading_top = self.grid_array["cars_top"]
        self.cars_heading_bot = self.grid_array["cars_bot"]
        self.cars_heading_left = self.grid_array["cars_left"]
        self.cars_heading_right = self.grid_array["cars_right"]

        # specifies whether or not there will be traffic lights at the
        # intersections (True by default)
        self.use_traffic_lights = net_params.additional_params.get(
            "traffic_lights", True)

        # radius of the inner nodes (ie of the intersections)
        self.inner_nodes_radius = 2.9 + 3.3 * max(self.vertical_lanes,
                                                  self.horizontal_lanes)

        # total number of edges in the network
        self.num_edges = 4 * ((self.col_num + 1) * self.row_num + self.col_num)

        # name of the network (DO NOT CHANGE)
        self.name = "BobLoblawsLawBlog"

        super().__init__(name, vehicles, net_params, initial_config,
                         traffic_lights)

    def specify_nodes(self, net_params):
        """See parent class."""
        return self._inner_nodes + self._outer_nodes

    def specify_edges(self, net_params):
        """See parent class."""
        return self._inner_edges + self._outer_edges

    def specify_routes(self, net_params):
        """See parent class."""
        routes = defaultdict(list)

        # build row routes (vehicles go from left to right and vice versa)
        for i in range(self.row_num):
            bot_id = "bot{}_0".format(i)
            top_id = "top{}_{}".format(i, self.col_num)
            for j in range(self.col_num + 1):
                routes[bot_id] += ["bot{}_{}".format(i, j)]
                routes[top_id] += ["top{}_{}".format(i, self.col_num - j)]

        # build column routes (vehicles go from top to bottom and vice versa)
        for j in range(self.col_num):
            left_id = "left{}_{}".format(self.row_num, j)
            right_id = "right0_{}".format(j)
            for i in range(self.row_num + 1):
                routes[left_id] += ["left{}_{}".format(self.row_num - i, j)]
                routes[right_id] += ["right{}_{}".format(i, j)]

        return routes

    def specify_types(self, net_params):
        """See parent class."""
        types = [{
            "id": "horizontal",
            "numLanes": self.horizontal_lanes,
            "speed": self.speed_limit["horizontal"]
        }, {
            "id": "vertical",
            "numLanes": self.vertical_lanes,
            "speed": self.speed_limit["vertical"]
        }]

        return types

    def _inner_nodes(self):
        """Build out the inner nodes of the network.
        The inner nodes correspond to the intersections between the roads. They
        are numbered from bottom left, increasing first across the columns and
        then across the rows.
        For example, the nodes in a traffic light grid with 2 rows and 3 columns
        would be indexed as follows:
            |     |     |
        --- 3 --- 4 --- 5 ---
            |     |     |
        --- 0 --- 1 --- 2 ---
            |     |     |
        The id of a node is then "center{index}", for instance "center0" for
        node 0, "center1" for node 1 etc.
        Returns
        -------
        list <dict>
            List of inner nodes
        """
        node_type = "traffic_light" if self.use_traffic_lights else "priority"

        nodes = []
        for row in range(self.row_num):
            for col in range(self.col_num):
                nodes.append({
                    "id": "center{}".format(row * self.col_num + col),
                    "x": col * self.inner_length,
                    "y": row * self.inner_length,
                    "type": node_type,
                    "radius": self.inner_nodes_radius
                })

        return nodes

    def _outer_nodes(self):
        """Build out the outer nodes of the network.
        The outer nodes correspond to the extremities of the roads. There are
        two at each extremity, one where the vehicles enter the network
        (inflow) and one where the vehicles exit the network (outflow).
        Consider the following network with 2 rows and 3 columns, where the
        extremities are marked by 'x', the rows are labeled from 0 to 1 and the
        columns are labeled from 0 to 2:
                 x     x     x
                 |     |     |
        (1) x----|-----|-----|----x (*)
                 |     |     |
        (0) x----|-----|-----|----x
                 |     |     |
                 x     x     x
                (0)   (1)   (2)
        On row i, there are two nodes at the left extremity of the row, labeled
        "left_row_short{i}" and "left_row_long{i}", as well as two nodes at the
        right extremity labeled "right_row_short{i}" and "right_row_long{i}".
        On column j, there are two nodes at the bottom extremity of the column,
        labeled "bot_col_short{j}" and "bot_col_long{j}", as well as two nodes
        at the top extremity labeled "top_col_short{j}" and "top_col_long{j}".
        The "short" nodes correspond to where vehicles enter the network while
        the "long" nodes correspond to where vehicles exit the network.
        For example, at extremity (*) on row (1):
        - the id of the input node is "right_row_short1"
        - the id of the output node is "right_row_long1"
        Returns
        -------
        list <dict>
            List of outer nodes
        """
        nodes = []

        def new_node(x, y, name, i):
            return [{"id": name + str(i), "x": x, "y": y, "type": "priority"}]

        # build nodes at the extremities of columns
        for col in range(self.col_num):
            x = col * self.inner_length
            y = (self.row_num - 1) * self.inner_length
            nodes += new_node(x, - self.short_length,
                              "bot_col_short", col)  # short
            nodes += new_node(x, - self.long_length, "bot_col_long", col)
            nodes += new_node(x, y + self.short_length,
                              "top_col_short", col)  # short
            nodes += new_node(x, y + self.long_length, "top_col_long", col)

        # build nodes at the extremities of rows
        for row in range(self.row_num):
            x = (self.col_num - 1) * self.inner_length
            y = row * self.inner_length
            nodes += new_node(- self.short_length, y,
                              "left_row_short", row)  # short
            nodes += new_node(- self.long_length, y, "left_row_long", row)
            nodes += new_node(x + self.short_length, y,
                              "right_row_short", row)  # short
            nodes += new_node(x + self.long_length, y, "right_row_long", row)

        return nodes

    def _inner_edges(self):
        """Build out the inner edges of the network.
        The inner edges are the edges joining the inner nodes to each other.
        Consider the following network with n = 2 rows and m = 3 columns,
        where the rows are indexed from 0 to 1 and the columns from 0 to 2, and
        the inner nodes are marked by 'x':
                |     |     |
        (1) ----x-----x-----x----
                |     |     |
        (0) ----x-----x-(*)-x----
                |     |     |
               (0)   (1)   (2)
        There are n * (m - 1) = 4 horizontal inner edges and (n - 1) * m = 3
        vertical inner edges, all that multiplied by two because each edge
        consists of two roads going in opposite directions traffic-wise.
        On an horizontal edge, the id of the top road is "top{i}_{j}" and the
        id of the bottom road is "bot{i}_{j}", where i is the index of the row
        where the edge is and j is the index of the column to the right of it.
        On a vertical edge, the id of the right road is "right{i}_{j}" and the
        id of the left road is "left{i}_{j}", where i is the index of the row
        above the edge and j is the index of the column where the edge is.
        For example, on edge (*) on row (0): the id of the bottom road (traffic
        going from left to right) is "bot0_2" and the id of the top road
        (traffic going from right to left) is "top0_2".
        Returns
        -------
        list <dict>
            List of inner edges
        """
        edges = []

        def new_edge(index, from_node, to_node, orientation, lane):
            return [{
                "id": lane + index,
                "type": orientation,
                "priority": 78,
                "from": "center" + str(from_node),
                "to": "center" + str(to_node),
                "length": self.inner_length
            }]

        # Build the horizontal inner edges
        for i in range(self.row_num):
            for j in range(self.col_num - 1):
                node_index = i * self.col_num + j
                index = "{}_{}".format(i, j + 1)
                edges += new_edge(index, node_index + 1, node_index,
                                  "horizontal", "top")
                edges += new_edge(index, node_index, node_index + 1,
                                  "horizontal", "bot")

        # Build the vertical inner edges
        for i in range(self.row_num - 1):
            for j in range(self.col_num):
                node_index = i * self.col_num + j
                index = "{}_{}".format(i + 1, j)
                edges += new_edge(index, node_index, node_index + self.col_num,
                                  "vertical", "right")
                edges += new_edge(index, node_index + self.col_num, node_index,
                                  "vertical", "left")

        return edges

    def _outer_edges(self):
        """Build out the outer edges of the network.
        The outer edges are the edges joining the inner nodes to the outer
        nodes.
        Consider the following network with n = 2 rows and m = 3 columns,
        where the rows are indexed from 0 to 1 and the columns from 0 to 2, the
        inner nodes are marked by 'x' and the outer nodes by 'o':
                o    o    o
                |    |    |
        (1) o---x----x----x-(*)-o
                |    |    |
        (0) o---x----x----x-----o
                |    |    |
                o    o    o
               (0)  (1)  (2)
        There are n * 2 = 4 horizontal outer edges and m * 2 = 6 vertical outer
        edges, all that multiplied by two because each edge consists of two
        roads going in opposite directions traffic-wise.
        On row i, there are four horizontal edges: the left ones labeled
        "bot{i}_0" (in) and "top{i}_0" (out) and the right ones labeled
        "bot{i}_{m}" (out) and "top{i}_{m}" (in).
        On column j, there are four vertical edges: the bottom ones labeled
        "left0_{j}" (out) and "right0_{j}" (in) and the top ones labeled
        "left{n}_{j}" (in) and "right{n}_{j}" (out).
        For example, on edge (*) on row (1): the id of the bottom road (out)
        is "bot1_3" and the id of the top road is "top1_3".
        Edges labeled by "in" are edges where vehicles enter the network while
        edges labeled by "out" are edges where vehicles exit the network.
        Returns
        -------
        list <dict>
            List of outer edges
        """
        edges = []

        def new_edge(index, from_node, to_node, orientation, length):
            return [{
                "id": index,
                "type": {"v": "vertical", "h": "horizontal"}[orientation],
                "priority": 78,
                "from": from_node,
                "to": to_node,
                "length": length
            }]

        for i in range(self.col_num):
            # bottom edges
            id1 = "right0_{}".format(i)
            id2 = "left0_{}".format(i)
            node1 = "bot_col_short{}".format(i)  # short left to right
            node2 = "center{}".format(i)
            node3 = "bot_col_long{}".format(i)
            edges += new_edge(id1, node1, node2, "v", self.short_length)
            edges += new_edge(id2, node2, node3, "v", self.long_length)

            # top edges
            id1 = "left{}_{}".format(self.row_num, i)
            id2 = "right{}_{}".format(self.row_num, i)
            node1 = "top_col_short{}".format(i)  # short right to left
            node2 = "center{}".format((self.row_num - 1) * self.col_num + i)
            node3 = "top_col_long{}".format(i)
            edges += new_edge(id1, node1, node2, "v", self.short_length)
            edges += new_edge(id2, node2, node3, "v", self.long_length)

        for j in range(self.row_num):
            # left edges
            id1 = "bot{}_0".format(j)
            id2 = "top{}_0".format(j)
            node1 = "left_row_short{}".format(j)
            node2 = "center{}".format(j * self.col_num)
            node3 = "left_row_long{}".format(j)
            edges += new_edge(id1, node1, node2, "h", self.short_length)
            edges += new_edge(id2, node2, node3, "h", self.long_length)

            # right edges
            id1 = "top{}_{}".format(j, self.col_num)
            id2 = "bot{}_{}".format(j, self.col_num)
            node1 = "right_row_short{}".format(j)
            node2 = "center{}".format((j + 1) * self.col_num - 1)
            node3 = "right_row_long{}".format(j)
            edges += new_edge(id1, node1, node2, "h", self.short_length)
            edges += new_edge(id2, node2, node3, "h", self.long_length)

        return edges

    def specify_connections(self, net_params):
        """Build out connections at each inner node.
        Connections describe what happens at the intersections. Here we link
        lanes in straight lines, which means vehicles cannot turn at
        intersections, they can only continue in a straight line.
        """
        con_dict = {}

        def new_con(side, from_id, to_id, lane, signal_group):
            return [{
                "from": side + from_id,
                "to": side + to_id,
                "fromLane": str(lane),
                "toLane": str(lane),
                "signal_group": signal_group
            }]

        # build connections at each inner node
        for i in range(self.row_num):
            for j in range(self.col_num):
                node_id = "{}_{}".format(i, j)
                right_node_id = "{}_{}".format(i, j + 1)
                top_node_id = "{}_{}".format(i + 1, j)

                conn = []
                for lane in range(self.vertical_lanes):
                    conn += new_con("bot", node_id, right_node_id, lane, 1)
                    conn += new_con("top", right_node_id, node_id, lane, 1)
                for lane in range(self.horizontal_lanes):
                    conn += new_con("right", node_id, top_node_id, lane, 2)
                    conn += new_con("left", top_node_id, node_id, lane, 2)

                node_id = "center{}".format(i * self.col_num + j)
                con_dict[node_id] = conn

        return con_dict
