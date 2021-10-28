import networkx as nx
from networkx.generators.random_graphs import *
import os
import pickle
import random
from copy import deepcopy
import math

def generate_TS(time_span, background_G):
    edges = list(background_G.edges())   
    TS_0 = []
    for i in range(len(edges)):
        TS_0.append((random.randint(0, time_span), edges[i%len(edges)]))  
    return TS_0
    
def generate_TS_out(time_span, background_G): 
    ##### Create an optimal path in the solution
    TS_OP = []; edges_OP=[]
    for i in range(0,color):
      if i==0:
          i1=0
      elif i>0:    
          i1=i2+1
      i2=(i1+math.floor(time_span/color))-1
      if i < color-1:
        edges_OP.append((i,i+1))
        TS_OP.append((random.randint(i1,i2), edges_OP[i%len(edges_OP)]))           
    
    TS_00 = generate_TS(time_span, background_G)  
    TS_0=TS_OP + TS_00 
    TS_0.sort()
    TS = {}    

    for i in TS_0:
        if i[0] not in TS:
            TS[i[0]] = []
        TS[i[0]].append(i[1])
    return TS

def generate_RG(n, edges_p, nodes):
    #### Erdős-Rényi ####
    background_G = fast_gnp_random_graph(n, edges_p, seed=None, directed=False)
    #### Barabási–Albert ####
    #background_G = barabasi_albert_graph(n, m, seed=None)
    
    gnodes = list(background_G.nodes())
    color_map=[]; color_map_dict={}
    color_list_not_rep= deepcopy(color_list)  
    for ii in gnodes:
        if ii<= color-1:            
            color_map.append(color_list_not_rep[ii])
        else:
            random_color=random.choice(color_list)
            color_map.append(random_color)
    return background_G, color_map

def color_map_dict(color_map):
    col_map = {}
    for i in range(0,len(color_map)):
        col_map[i] = color_map[i]
        
    return col_map
    
#def generate(generator_pars):
if __name__ == '__main__':    
    
    ###########Erdős-Rényi    Parameter-----------------------
    edges_p = 0.4       #edge_probability of background graph
    ###########Barabási–Albert    Parameter-----------------------
    m=10
    ###########    
    n = 500 #  number of Nodes of background graph
    time_span = 90 #time horizon
    color=50   # number of colors in bachground graph
    
    color_list=list(range(0,color))
    time_span=time_span - 1 
    for i in range(0,1000):
        print('iteration:',i)
        background_G, color_map = generate_RG(n, edges_p, range(n))                                   
        col_map = color_map_dict(color_map) 
        TS = generate_TS_out(time_span, background_G)
        ######## SAVE the data
        os.chdir("/Users/mehdi/Desktop/python/ColorPath_TG/synthetic_data/ER/color50_ts90/p0.4") 
        b=[]; b_G=[]
        a = (str(i).zfill(2))
        filename = "data.py"
        filename_G= "data_G.py"
        b.append(filename[:4] + a + filename[4:])
        b_G.append(filename_G[:6] + a + filename[4:])
        fout = open(b[0],'w') 
        fout_G = open(b_G[0],'wb') 
        pickle.dump(background_G,fout_G)
        fout_G.close()
        fout.write("TS = ")
        fout.write(str(TS))
        fout.write("\n") 
        fout.write("col_map = ")
        fout.write(str(col_map))
        fout.write("\n")
        fout.write("color_list = ")
        fout.write(str(color_list))
        fout.write("\n")
        fout.write("\n" + "#= done =" + "\n")
        fout.close() 
 