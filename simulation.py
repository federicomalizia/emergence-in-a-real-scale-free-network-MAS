# -*- coding: utf-8 -*-
"""
@author: Federico Malizia
"""

from agents import *
from functions import *
from db.objects import*
import pandas as pd



agents,N = generate_agents()
attach_features(agents)
G = network(agents)
echo_chambers = run_network(agents,G)

