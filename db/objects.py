# -*- coding: utf-8 -*-
"""
@author: Federico Malizia
"""

import pandas as pd
import csv


with open('db/comuni_italiani_con_probabilita.csv', mode='r') as infile:
    reader = csv.reader(infile)
    cities_dict = {rows[1]:rows[0] for rows in reader}

with open('db/partiti.csv', mode='r') as infile:
    reader = csv.reader(infile)
    parties_dict = {rows[0]:rows[3] for rows in reader}

names_df = pd.read_csv("db/Nomi italiani.csv", sep="\t")
names = list(names_df["Nomi"])
cities_df = pd.read_csv("db/comuni_italiani_con_probabilita.csv")
cities_prob = list(cities_df["p"])
cities = list(cities_df["Province"])
parties_df = pd.read_csv("db/partiti.csv")
parties = list(parties_df["Partito"])
parties_probs = list(parties_df["p"])    

