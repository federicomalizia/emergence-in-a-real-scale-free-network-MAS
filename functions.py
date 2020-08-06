# -*- coding: utf-8 -*-
"""
@author: Federico Malizia
"""
import numpy as np
import pandas as pd
import random
import networkx as nx
from db.objects import*
from agents import *
import matplotlib.pyplot as plt
from IPython.display import clear_output

def set_age():
    agelist = [i for i in range(14,85)] 
    age = np.random.choice(agelist)
    return age


def random_num():
    randomlist = [i for i in range(1,100)]
    random_num = np.random.choice(randomlist)
    return random_num


def generate_agents():
    agents = [] 
    N = int(input("What is the network size (number of nodes)? ")) 
    P = int(input("What is the number of superusers in the network? "))  
    shyness = float(input("Do you want to set a global agent shyness rate? (type -1 for random values or choose a value between 0 and 1)"))
    loquacity = float(input("Do you want to set a global agent loquacity rate? (type -1 for random values or choose a value between 0 and 1)"))
    foolishness = float(input("Do you want to set a global agent foolishness rate? (type -1 for random values or choose a value between 0 and 1)"))

    hostility = float(input("Do you want to set a global agent hostility rate ? (type -1 for random values or choose a value between 0 and 1)"))
    if loquacity > 1:
        return(print("Loquacity rate must be between 0 and 1!"))
    elif shyness > 1:
        return(print("Shyness rate must be between 0 and 1!"))
    else:      
        unique_id_list = list(range(10000,10000+N-P+1))
        unique_id_list_p = list(range(50000,50000+P+1))
        preferences_list = ['sport','news','attuality','gossip','politics','technology','art','music']
        for i in range(N-P):
            name = np.random.choice(names)
            age = set_age()
            city = np.random.choice(cities,p=cities_prob)
            party = np.random.choice(parties,p=parties_probs)
            unique_id = (unique_id_list[0])
            preferences = random.sample(preferences_list, k=np.random.choice(range(1,len(preferences_list))))
            del unique_id_list[0]
            if shyness == -1 :
                shyness_ = random.random()
            else:
                shyness_ = shyness
            if loquacity == -1:
                loquacity_ = random.random()
            else:
                loquacity_ = loquacity
            if hostility ==  -1:
                hostility_ = random.random()
            else:
                hostility_ = hostility
            if foolishness == -1:
                foolishness_ = random.random()
            else: 
                foolishness_ = foolishness
            a = User(name,age,city,party,hostility_,preferences,unique_id,shyness_,loquacity_,foolishness_)
            agents.append(a)
        for i in range(P):
            unique_id_p = (unique_id_list_p[0])
            del unique_id_list_p[0]
            topic = np.random.choice(preferences_list)
     
            p = SuperUser(topic,unique_id_p,random.random())

            agents.append(p)
            
        return(agents, N)
    
    
def network(agents):
    G = nx.Graph()
    for i in agents:
        G.add_node(i)
    return(G)


def attach_features(agents):
    for i in agents:
        if i.state != "p":  
            features_vector = []
            features_vector.append(int(cities_dict[i.district]))
            features_vector.append(int(parties_dict[i.party]))
            features_vector.append(i.age)
            features_vector.append(random_num())         
            i.features(features_vector)
        else:
            pass
        
def update_mood(agents,G):
    k_list =[]
    for i in G.nodes():
        if i.state != "p":
            k_list.append(G.degree(i))
        else:
            pass
    
    degreeq2 = np.ceil (max(k_list)*0.25)
    degreeq3 = np.ceil(max(k_list)*0.75)
    average_k = np.ceil(sum(k_list)/len(k_list))
    d =[]
    for i in G.nodes():
        d.append(G.degree(i))
    N = len(G.nodes())
    for node in agents:
        if node.state != "p":
            node.mood(d,degreeq2,average_k,degreeq3)
        else:
            pass
    for node in (list(G.nodes(data=True))):
        node[1]['state'] = node[0].get_user_state()


def running_interaction(threshold,node,node_r,G):
    decision = node.make_your_decision(node_r)
    if threshold == -1 :      
        success = node.approach(node_r, random.random(),decision)
    else:
        success = node.approach(node_r, threshold,decision)            
    if success == True:
        node_r.got_approached(node,True)
        G.add_edge(node, node_r)
    elif success == None:
        node_r.got_approached(node,success)
        G.remove_edge(node,node_r)
        
    elif success == "friend":
        node_t = node.pick_from_friend_list(node_r)
        if node_t != None:
            running_interaction(threshold,node,node_t,G)
        else:
            pass
        
def draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size):
    segregated =[]
    asocial = []
    social = []
    influencer = []
    cool = []
    node_color = []
    fig, plot = plt.subplots(1, 2, figsize=(20,10),gridspec_kw={'width_ratios': [1, 2]})
    update_mood(agents,G)
    echo_chambers_metric(agents)
    for node in list(G.nodes(data=True)):
        

        if 'seg' in node[1]['state']:
            node_color.append('black')

        elif 'a' in node[1]['state']:
            node_color.append('blue')

        elif 's' in node[1]['state']:
            node_color.append('green')

        elif 'c' in node[1]['state']:
            node_color.append('orange')

        elif 'i' in node[1]['state']:
            node_color.append('red')
        
        elif 'p' in node[1]['state']:
            node_color.append('yellow')
            
    for node in list(G.nodes()):
        
        if node.state =='seg':
            segregated.append(node)
            
        if node.state=='a':
            asocial.append(node)
            
        if node.state=='s':
            social.append(node)
            
        if node.state=='c':
            cool.append(node)
            
        if node.state=='i':
            influencer.append(node)
    
    segregated_size.append(len(segregated)/(len(G.nodes())))
    asocial_size.append(len(asocial)/(len(G.nodes())))
    social_size.append(len(social)/(len(G.nodes()))) 
    cool_size.append(len(cool)/(len(G.nodes()))) 
    influencer_size.append(len(influencer)/(len(G.nodes()))) 

    
    
    plot[0].plot(segregated_size,   color = 'black', label="Fraction of segregated users")
    plot[0].plot(asocial_size, color = 'blue', label="Fraction of asocial users")
    plot[0].plot(social_size,  color = 'green', label="Fraction or social users")
    plot[0].plot(cool_size,  color = 'orange', label="Fraction of cool users")
    plot[0].plot(influencer_size,  color = 'red', label="Fraction of influencers")    
    plot[0].title.set_text("Users distribution")
    plot[0].legend()        
    
            
    my_pos = nx.spring_layout(G, seed = 100)        
    plot[1] = nx.draw(G, pos= my_pos, node_size=150, with_labels=0, alpha=1, node_color=node_color, edge_color='grey')
    plt.pause(0.5)
    plt.show()
    print(len(G.edges()))
    

def echo_chambers_metric(agents):
    list_neighbors = []
    for i in agents:
        n=0
        m=0
        if i.state != "p":
            for j in list(i.friends_dict.values()):
                if j.opinion == i.opinion:
                    n+=1
                if len(list(i.friends_dict.values())) != 0:
                    m = n/len(list(i.friends_dict.values()))
                else:
                    pass
            list_neighbors.append(m)
    neighbors_chambers = sum(list_neighbors)/len(list_neighbors)
    return(neighbors_chambers)

def run_network(agents,G):    
    threshold = float(input("What is the tolerance degree between agents?? (-1 for random values or choose a value between 0 and 1) "))    
    t = int(input("How many interaction between agents do you want?"))
    segregated_size =[]
    asocial_size = []
    social_size = []
    influencer_size = []
    cool_size = []
    node_color = []    
    echo_chambers = []
    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)
    
    for i in range(t): 
        echo_chambers.append(echo_chambers_metric(agents))
        node = np.random.choice(agents)
        if node.state == "p":
            pass
        else:
            N = len(G.nodes())
            step = node.look_around(N)
            node_r_index = (agents.index(node) + step)
            if node_r_index < len(agents) and node.state != "p":            
                node_r = agents[node_r_index]
                running_interaction(threshold,node,node_r,G)

                if i == np.ceil(t*(0.01)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.03)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)
                if i == np.ceil(t*(0.05)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.08)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == t*(0.1):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.13)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.16)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == t*(0.2):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.23)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.26)): 
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == t*(0.3):       
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i== t*(0.4):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == t*(0.5):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)
                if i == np.ceil(t*(0.6)):
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.7)):     
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.8)):   
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == np.ceil(t*(0.9)): 
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

                if i == t:
                    clear_output(wait=True) 
                    draw_network(agents,G,segregated_size,asocial_size,social_size,cool_size,influencer_size)

            
            else:
                pass

    return(echo_chambers)

