# -*- coding: utf-8 -*-
"""
@author: Federico Malizia
"""
import numpy as np
import random 

class User():
    def __init__(self,name,age,district,party,hostility,preferences,unique_id,shyness,loquacity,foolishness):
        self.name = name
        self.age = age
        self.district = district
        self.party = party
        self.preferences = preferences
        self.unique_id = unique_id
        self.shyness = shyness
        self.friends_count = 0
        self.friends_dict = {}
        self.subscriptions_count = 0
        self.subscriptions_dict = {}
        self.demand = random.random()
        self.sympaties_dict = {} 
        self.hate_list = []
        self.opinion = np.random.choice([-1,1])
        self.loquacity = loquacity
        self.hostility = hostility
        self.foolishness = foolishness
        self.interaction = 0
        self.polarities = []
        self.polarization = 0
        self.state = "seg" #segregated
        
        
    def features(self,features_vec):
        self.features = features_vec
        
     
    def who_are_u(self):
        return(self.name,self.age,self.district,self.party)
    
    
    def get_id(self):
        return(self.unique_id)
    
    
    def get_features(self):
        return(self.features)     
    
        
    def get_user_state(self):
        return(self.state)
    
    
    def look_around(self,N):
        if self.friends_count <= 2:
            randomsteps = [i for i in range(int(-N/10),int(N/10))] 
            self.step = np.random.choice(randomsteps)
        if self.friends_count > 2 and self.friends_count <=5:
            randomsteps = [i for i in range(int(-N/5),int(N/5))] 
            self.step = np.random.choice(randomsteps)
        if self.friends_count > 5:
            randomsteps = [i for i in range(int(-N),int(N))]
            self.step = np.random.choice(randomsteps)
        return(self.step)
   

    def make_your_decision(self,friend):
        decision = False
        if friend.state == "p":
            if friend.get_id() in self.friends_dict.keys():
                decision = "t" # talk
            else:
                decision = "s" #submit subscription
            
        else:    
            if self.friends_count != 0:

                if random.random() <= self.loquacity:
                    decision = "t" #talk
                else:
                    if random.random() >= self.shyness:
                        decision = True
            else:
                if random.random() >= self.shyness:
                    decision = True

        return(decision)
   

    def sympathy(self,friend):       
        v_1 = np.array(self.features, dtype = "int")
        v_2 = np.array(friend.features, dtype = "int")
        sympathy_degree = np.linalg.norm(v_1 - v_2)
        self.sympaties_dict[friend.get_id()] = sympathy_degree
        return(sympathy_degree)
    
    
    def approach(self,friend,threshold,decision):
        success = False
        if decision == True:
            
            if friend.get_id() in self.friends_dict.keys() and friend.state != "p" and len(friend.friends_dict) != 0 and friend.get_id() != self.get_id():
                success = self.check_friend_list(friend) #"friend"   
                
            if friend.get_id() not in self.friends_dict.keys() and friend.state != "p" and friend.get_id() not in self.hate_list and friend.get_id() != self.get_id():

                if self.sympathy(friend) <= (threshold*100):
                    success = True
                    self.add_friend(friend)
                else:
                    self.hate_list.append(friend)
                    #return(success)
                    #pass
                    
        elif decision == "t" and friend.get_id() in self.friends_dict.keys() and friend.get_id() != self.get_id() or  friend.get_id() in self.subscriptions_dict :
            if friend.state != "p":
                success = self.talk_to_friends(friend,threshold)
            else:
                success = self.content_interaction(friend)
                    
             #return(success) 
            
        elif decision == "s": 
            success = self.submit_subscription(friend)
            
        return(success)

    def talk_to_friends(self,friend,threshold):
        success = False
        
        if friend.get_id() in self.friends_dict.keys() and friend.state != "p" and friend.get_id() != self.get_id():
            self.interaction += 1
            if self.opinion != friend.opinion:
                if self.sympathy(friend)/100 > random.random():#(friend.loquacity - friend.hostility)*100:
                    self.remove_friend(friend)
                    self.hate_list.append(friend)
                    success = None
                elif self.foolishness > random.random():
                    self.opinion = friend.opinion
            self.polarities.append(self.opinion)
            self.polarization = sum(self.polarities)/self.interaction
        return(success)
    
    def content_interaction(self,superuser):
        success = False
        if superuser.get_id() in self.subscriptions_dict.keys():
            self.interaction += 1 
            content = np.random.choice([-1,1])
            if content != superuser.opinion:
                if self.hostility >= random.random():
                    self.remove_subscription(superuser)
                    self.hate_list.append(superuser)
                    success = None
            else:
                if self.foolishness > random.random():
                    self.opinion  = content
            self.polarities.append(self.opinion)
            self.polarization = sum(self.polarities)/self.interaction
        return(success)
            
    
    def submit_subscription(self,friend):
        success = False
        if friend.get_id() not in self.subscriptions_dict.keys():
            if (any([item in friend.topic for item in self.preferences])) == True and self.demand <= friend.quality:
                success = True
                self.add_subscription(friend)
        return(success)
        

        
    def pick_from_friend_list(self,friend):
        friend_r = random.choice(list(friend.friends_dict.values()))
        return(friend_r)
                
        
    def check_friend_list(self,friend):
        if any([item in self.hate_list for item in friend.friends_dict.values()]) == True or any([item in self.hate_list for item in friend.subscriptions_dict.values()]) == True:
            success = None 
            self.remove_friend(friend)
            self.hate_list.append(friend)                  
        else:
            success = "friend"
        return(success)
              
        
    def got_approached(self,friend,success):
        if success == True:
            self.add_friend(friend)
        if success == None:
            self.remove_friend(friend)
            
            
    def add_subscription(self,friend):
        self.subscriptions_count += 1
        self.subscriptions_dict[friend.get_id()] = friend
        
        
    def remove_subscription(self,friend):
        self.subscriptions_count += -1
        del self.subscriptions_dict[friend.get_id()]
        
    
    def add_friend(self,friend):
        self.friends_count += 1
        self.friends_dict[friend.get_id()] = friend
    
    def remove_friend(self,friend):
        if friend.get_id() in self.friends_dict.keys() and friend.get_id() != self.get_id():
            self.friends_count += -1
            del self.friends_dict[friend.get_id()]        
        else:
            pass


    
    def mood(self,N,k_25,average_k, k_75):
        if self.friends_count == 0:
            self.state = "seg" #segregated
        if self.friends_count > 0 and self.friends_count <= k_25:           
            self.state = "a" #asocial
        if self.friends_count > k_25 and self.friends_count <= average_k:
            self.state = "s" #sociable
        if self.friends_count > average_k and self.friends_count < k_75:      
            self.state ="c" #cool
        if self.friends_count != 0 and self.friends_count >= k_75:           
            self.state = "i" #influencer
        return(self.state)
    

class SuperUser():
    def __init__(self,topic,unique_id,quality):
        self.topic = topic
        self.unique_id = unique_id
        self.subscribers_count = 0
        self.subscribers_dict = {}
        self.ban_list = []
        self.quality = random.random()# quality
        #self.democraciness = democraciness
        self.opinion = np.random.choice([-1,1])
        self.state = "p" #superuser
    
    def get_id(self):
        return(self.unique_id)
    
    def get_user_state(self):
        return(self.state)

    def get_topic(self):
        return(self.topic)
    
    
    def got_approached(self,subscriber,success):
        if success == True:
            self.add_subscriber(subscriber)
        if success == None:
            self.remove_subscriber(subscriber)
            
            
    def add_subscriber(self,subscriber):
        self.subscribers_count += 1
        self.subscribers_dict[subscriber.get_id()] = subscriber
    
    def remove_subscriber(self,subscriber):
        if subscriber.get_id() in self.subscribers_dict.keys() and subscriber.get_id() != self.get_id():
            self.subscribers_count -= 1
            del self.subscribers_dict[subscriber.get_id()]
            self.ban_list.append(subscriber)
        else:
            pass
    
    
    