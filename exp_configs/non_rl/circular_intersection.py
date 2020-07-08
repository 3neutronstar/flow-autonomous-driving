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


class RingNetwork_intest(Network):
    pass


ADDITIONAL_NET_PARAMS = {
    "length": 40,
    "num_lanes": 1,
    "speed_limit": 30,
}

vehicles = VehicleParams()
vehicles.add(
    veh_id="idm",
    acceleration_controller=(IDMController, {}),
    routing_controller=(ContinuousRouter, {}),
    num_vehicles=22)
