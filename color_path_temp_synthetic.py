from copy import deepcopy
import numpy as np
import networkx as nx
from generate import *
import os
import pickle
import math
import time

res = np.zeros((1000,4))
for data_ite in range(0,1000):
    print('data iteration:',data_ite)
    a = (str(data_ite).zfill(2))
    ##import data
    os.chdir("/Users/mehdi/Desktop/python/ColorPath_TG/github/synthetic_data/ER/color50_ts90/p0.1")  
    b=[]; b_G=[]      
    filename = "data.py"    
    b.append(filename[:4] + a + filename[4:])   
    exec(open(b[0]).read())
    del a, b_G, filename
    import time
    t1=time.time()
    n=[]
    path=[]; path1_localSearch= []; path2_localSearch= []; del_nod=path
    TS_current=deepcopy(TS) 
    visited_color=[]; visited_color1_localSearch=[]
    keys_TS = list(TS.keys())
    current_time=-1   
    epsilon=1*(round((keys_TS[-1]+1)/(len(color_list)))) 
    def G_for_interval(TS_current,current_time,del_nod):                  
        edge_start=[]; interval=[]
        for i in range(epsilon):
            current_time +=1
            if  current_time > keys_TS[-1]:
                current_time -=1
                break    
            if current_time not in keys_TS:
                while current_time not in keys_TS:
                    current_time +=1
            print ('current_time:',current_time) 
            interval.append(current_time)
            edge_start.append(TS_current[current_time])   
    
        G = nx.Graph()
        for j in range(len(edge_start)):    
            for (n1, n2) in edge_start[j]:
                G.add_edge(n1, n2)
        if del_nod !=[]:
           G.remove_nodes_from(del_nod)        
        return G, current_time, interval        
            
    def largeDeg_node(G,col_map,n,visited_color):   
       
        if number_interval > 1:
            degrees = [sorted(G.degree(n), key=lambda x: x[1], reverse=True)]
        elif number_interval == 1:  
            degrees = [sorted(G.degree, key=lambda x: x[1], reverse=True)]
        if  degrees[0] !=[]:
            s1=0
            selected_node=deepcopy(degrees[0][s1][0]) 
            if selected_node!=[]:    
               selected_node_col=col_map[selected_node]
               while selected_node_col in (visited_color):
                  s1+=1 
                  if len(degrees[0]) > s1:
                    selected_node=deepcopy(degrees[0][s1][0])
                  elif len(degrees[0]) <= s1:  
                    selected_node=[]
                    selected_node_col=[]  
    
            if selected_node!=[] :  
              if selected_node  in G:  
               nn=list(G.neighbors(selected_node))
              elif selected_node  not in G:
                nn=[] 
            elif selected_node==[] :  
              nn=[]  
        elif degrees[0] ==[] and n!=[]: 
            selected_node_col=col_map[n[0]] 
            if selected_node_col not in visited_color:
               selected_node=n[0]
            elif selected_node_col in visited_color:
               selected_node=[]
        elif degrees[0] ==[] and n==[]:   
            selected_node=[]
        if selected_node in G:        
                s=0
                for x in nn: 
                  if visited_color !=[]:
                    if col_map[x]== selected_node_col or col_map[x] in (visited_color):
                       G.remove_node(x) 
                       nn.remove(x)
                       s+=1
                  elif visited_color ==[]:
                    if col_map[x]== selected_node_col:
                       G.remove_node(x) 
                       nn.remove(x)
                       s+=1     
                if s!=0:
                   largeDeg_node(G,col_map,n,visited_color)  
        elif  selected_node not in G: 
             if current_time == keys_TS[-1]:     
                selected_node=selected_node
        return selected_node      
      
    def TS_updated(TS_current, visited_color, col_map,epsilon,current_time,path):  
        for i in interval: 
            del TS_current[i]
        del_nod=deepcopy(path)
        for name, value in col_map.items():  
            if value in  visited_color:   
               del_nod.append(name)
        del_nod=list(set(del_nod))  
        return TS_current, del_nod
    
    def local_search_edge(TS, path_edges_ts, col_map, path, visited_color, interval_span,path1_localSearch, visited_color1_localSearch):
      path1_localSearch=deepcopy(path)
      visited_color1_localSearch=deepcopy(visited_color)
      
      def neighbors_ofEachEdgePath(TS,path_edges_ts,path_edges_ts_LS1,i,path,path1_localSearch,visited_color,col_map):      
            
            ii=deepcopy(path_edges_ts[i])                 
            ii_next=deepcopy(path_edges_ts[i+1])
            n11=path[i]; n12=path[i+1]   
            index=path1_localSearch.index (n11)
            Ls1_added_node=[]  ; path_edges_ts_new=[] 
            edges_of_TS=[]
            neigh_1={}; neigh_2={}
            res=[]; new_path_ts=[]
            if i < 1:  
                for j in range(ii,ii_next):
                    if j in list(TS.keys()):
                      edges_of_TS=deepcopy(TS[j])
                    G2 = nx.Graph()
                    for (n1, n2) in edges_of_TS:
                        G2.add_edge(n1, n2)
                    if n11 in G2:    
                        neigh_1.update({j:list(G2.neighbors(n11))})
                    if n12 in G2:
                        neigh_2.update({j:list(G2.neighbors(n12))})
                lst =[]        
                for jj in list(neigh_1.keys()):
                 if Ls1_added_node!=[]:
                        break   
                 for jjj in range(jj+1,ii_next):
                    if Ls1_added_node!=[]:
                        break
                    if jjj in list(neigh_2.keys()):
                      lst = list(set(neigh_2[jjj]) & set(neigh_1[jj]))
                      if lst!=[]:
                         Ls1_added_node=[] 
                         for i1 in range(len(lst)): 
                           if Ls1_added_node==[]:
                             n=lst[i1] 
                             if n not in path :  
                              if n2 not in path1_localSearch:
                                if col_map[n] not in visited_color:
                                  if col_map[n] not in visited_color1_localSearch:
                                     Ls1_added_node=n
                                     path_edges_ts_new=deepcopy(path_edges_ts)
                                     del  path_edges_ts_new[i]
                                     path_edges_ts_new.append(jj)
                                     path_edges_ts_new.append(jjj)
                                     path_edges_ts_new=sorted(path_edges_ts_new)
                                     break
            elif i >= 1:
                ii_back=path_edges_ts_LS1[path_edges_ts_LS1.index(ii)-1]
                for j in range(ii_back+1,ii_next):    
                    if j in list(TS.keys()):
                      edges_of_TS=deepcopy(TS[j])
                    G2 = nx.Graph()
                    for (n1, n2) in edges_of_TS:
                        G2.add_edge(n1, n2)
                    if n11 in G2:    
                        neigh_1.update({j:list(G2.neighbors(n11))})
                    if n12 in G2:
                        neigh_2.update({j:list(G2.neighbors(n12))})
                lst =[]        
                for jj in list(neigh_1.keys()):
                 if Ls1_added_node!=[]:
                        break   
                 for jjj in range(jj+1,ii_next):
                    if Ls1_added_node!=[]:
                        break    
                    if jjj in list(neigh_2.keys()):
                      lst = list(set(neigh_2[jjj]) & set(neigh_1[jj]))
                      if lst!=[]:
                         Ls1_added_node=[] 
                         for i1 in range(len(lst)): 
                           if Ls1_added_node==[]:
                             n=lst[i1] 
                             if n not in path : 
                              if n2 not in path1_localSearch:
                                if col_map[n] not in visited_color:
                                  if col_map[n] not in visited_color1_localSearch:
                                     Ls1_added_node=n
                                     path_edges_ts_new=deepcopy(path_edges_ts)
                                     del  path_edges_ts_new[:i+1]
                                     path_edges_ts_new.append(jj)
                                     path_edges_ts_new.append(jjj)
                                     path_edges_ts11=path_edges_ts_LS1[:path_edges_ts_LS1.index(ii)]
                                     path_edges_ts_new=path_edges_ts_new+path_edges_ts11
                                     path_edges_ts_new=sorted(path_edges_ts_new)
                                     break
            res=deepcopy(Ls1_added_node)                        
            return res,new_path_ts, index, path_edges_ts_new  
      path_edges_ts_LS1=deepcopy(path_edges_ts)
      ite1=len(path_edges_ts)-1 
      for i in range(ite1):    
         res,new_path_ts,index,path_edges_ts_new = neighbors_ofEachEdgePath(TS,path_edges_ts,path_edges_ts_LS1,i,path,path1_localSearch,visited_color,col_map)        
         if res!=[]:           
            node_be_add=deepcopy(res)
            path1_localSearch = path1_localSearch[:index+1] + [node_be_add] + path1_localSearch[index+1:]               
            visited_color1_localSearch=  visited_color1_localSearch[:index+1] + [col_map[node_be_add]] + visited_color1_localSearch[index+1:]    
            path_edges_ts_LS1=deepcopy(path_edges_ts_new)
    
      return path1_localSearch, visited_color1_localSearch, path_edges_ts_LS1 
    ####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$####$$
    def local_search_node(TS, col_map,interval_span, path_edges_ts_LS1,path1_localSearch, visited_color1_localSearch):
        
        def  find_new_path_LS2(path_input,visited_color_input,path_edges_input,path_edges_ts_LS2,i_back,j,i):
         
         path_edges_input=deepcopy(path_input)
         path_edges_ts_LS22=deepcopy(path_edges_ts_LS2)
         new_path_edges_ts_LS2=[]
         neigh_1=[]; neigh_2=[]   
         new_path_edges_ts_neigh_1=[]; new_path_edges_ts_neigh_2=[]
         neigh_connection=[]
         if j==0:
           path1=[]  
           tsPath_1=0
           path2=path_input[j+1]
           tsPath_2=path_edges_ts_LS2[j+1]
           NN=[path2]
         elif j>0:             
           path1=path_input[j-1]
           if j==1:
              tsPath_1=path_edges_ts_LS2[0]
           elif j!=1:   
              tsPath_1=path_edges_ts_LS2[j-2]
           if j!=path_input.index(path_input[-1]):  
               path2=path_input[j+1]
               if path2==path_input[-1]:
                  tsPath_2=path_edges_ts_LS2[j]
               elif path2!=path_input[-1]:   
                  tsPath_2=path_edges_ts_LS2[j+1]
           elif j==path_input.index(path_input[-1]): 
               path2=[]  
               tsPath_2=keys_TS[-1]+1
           NN=[path1,path2]
         check_path=deepcopy(path_edges_input)
         check_path1=deepcopy(path_edges_input)
         check_path1.remove(path_edges_input[j])
         check_color=deepcopy(visited_color_input)
         color_of_del_nod=visited_color_input[j]
         check_color.remove(visited_color_input[j])
         if j==0:
          del path_edges_ts_LS22[j:j+1]  
          NNN=[path2,path_input[j]]
         elif j>0:    
          del path_edges_ts_LS22[j-1:j+1]
          if j==path_input[-1]:          
              NNN=[path1,path_input[j]]   
          elif j!=path_input[-1]:
              NNN=[path1,path2,path_input[j]]
         for jj in range(tsPath_1+1,tsPath_2):
            if jj in list(TS.keys()):
              for (n1, n2) in TS[jj]:
                if n1 in NN and n2 not in NNN: 
                  if n2 not in check_path :
                      if col_map[n2] not in check_color:  
                          if n1==path1:
                             neigh_1.append(n2) 
                             new_path_edges_ts_neigh_1.append(jj)
                          elif n1==path2:
                             neigh_2.append(n2) 
                             new_path_edges_ts_neigh_2.append(jj)
                if n2 in NN and n1 not in NNN: 
                  if n1 not in check_path :
                      if col_map[n1] not in check_color:   
                          if n2==path1:
                             neigh_1.append(n1) 
                             new_path_edges_ts_neigh_1.append(jj)
                          elif n2==path2:
                             neigh_2.append(n1)
                             new_path_edges_ts_neigh_2.append(jj)
         if j==0:
           neigh_connection=[]  
           if neigh_2!=[]:  
            neig_of_neig=[]; ts_neig_of_neig=[]
            for j2 in range(len(neigh_2)):
             if  neig_of_neig!=[]:  
                 break
             elif  neig_of_neig==[]:   
              neig=neigh_2[j2]
              neig_ts=new_path_edges_ts_neigh_2[j2]
              for jj11 in range(tsPath_1,neig_ts):
                if jj11 in list(TS.keys()):
                 for (n1, n2) in TS[jj11]:   
                  if n1==neig:
                     if n2 not in check_path : 
                       if col_map[n2] not in check_color: 
                        if col_map[n2] != col_map[neig]:  
                          neig_of_neig.append(n2)                          
                          ts_neig_of_neig.append(jj11)
                  elif n2==neig:
                      if n1 not in check_path : 
                       if col_map[n1] not in check_color:
                         if col_map[n1] != col_map[neig]: 
                          neig_of_neig.append(n1)
                          ts_neig_of_neig.append(jj11)
              if  neig_of_neig!=[]:
               neigh_connection.append((neig_of_neig[0],neigh_2[j2]))
               new_path_edges_ts_LS2.append(ts_neig_of_neig[0])
               new_path_edges_ts_LS2.append(neig_ts)
         elif j>0 and j!=path_input.index(path_input[-1]):       
          if neigh_1!=[] and neigh_2!=[]:
            neig_of_neig=[]; ts_neig_of_neig=[]
            neigh_connection=[]; ts_neig_of_path1=[]
            for j2 in range(len(neigh_2)):
             if  neig_of_neig!=[]:  
                 break
             elif  neig_of_neig==[]:   
              neig=neigh_2[j2]
              neig_ts=new_path_edges_ts_neigh_2[j2]
              for jjj11 in range(tsPath_1,neig_ts):
                if jjj11 in list(TS.keys()):
                 for (n1, n2) in TS[jjj11]:   
                  if n1==neig:
                     if n2 not in check_path: 
                       if col_map[n2] not in check_color: 
                         if col_map[n2] != col_map[neig]:
                           if n2 in neigh_1:
                             ind=deepcopy( neigh_1.index(n2) )
                             if new_path_edges_ts_neigh_1[ind] < jjj11:
                                  neig_of_neig.append(n2)                     
                                  ts_neig_of_neig.append(jjj11) 
                                  ts_neig_of_path1.append(new_path_edges_ts_neigh_1[ind])
                  if n2==neig:
                     if n1 not in check_path: 
                       if col_map[n1] not in check_color: 
                         if col_map[n2] != col_map[neig]:
                          if n1 in neigh_1:
                            ind=deepcopy(neigh_1.index(n1))  
                            if new_path_edges_ts_neigh_1[ind] < jjj11:
                               neig_of_neig.append(n1)                     
                               ts_neig_of_neig.append(jjj11) 
                               ts_neig_of_path1.append(new_path_edges_ts_neigh_1[ind])
    
              if neig_of_neig!=[]:
               neigh_connection.append((neig_of_neig[0],neigh_2[j2]))
               new_path_edges_ts_LS2.append(ts_neig_of_path1[0])
               new_path_edges_ts_LS2.append(ts_neig_of_neig[0])
               new_path_edges_ts_LS2.append(neig_ts) 
    
         elif j>0 and j==path_input.index(path_input[-1]):       
          if neigh_1!=[]:
            neig_of_neig=[]; ts_neig_of_neig=[]
            neigh_connection=[]; ts_neig_of_path1=[]
            for j2 in range(len(neigh_1)):
             if  neig_of_neig!=[]:  
                 break
             elif  neig_of_neig==[]:   
              neig=neigh_1[j2]
              neig_ts=new_path_edges_ts_neigh_1[j2]
              for jjj11 in range(neig_ts,tsPath_2+1):
                if jjj11 in list(TS.keys()):  
                 for (n1, n2) in TS[jjj11]:   
                  if n1==neig:
                     if n2 not in check_path:
                       if col_map[n2] not in check_color: 
                         if col_map[n2] != col_map[neig]:
                                  neig_of_neig.append(n2)                     
                                  ts_neig_of_neig.append(jjj11) 
                  if n2==neig:
                     if n1 not in check_path: 
                       if col_map[n1] not in check_color: 
                         if col_map[n2] != col_map[neig]:
                               neig_of_neig.append(n1)                     
                               ts_neig_of_neig.append(jjj11) 
                               
    
              if neig_of_neig!=[]:
               neigh_connection.append((neigh_1[j2],neig_of_neig[0]))
               new_path_edges_ts_LS2.append(neig_ts)
               new_path_edges_ts_LS2.append(ts_neig_of_neig[0])
         if neigh_connection!=[]:           
              node_be_add1=neigh_connection[0][0]
              node_be_add2=neigh_connection[0][1]
              path2_localSearch = check_path1[:j] + [node_be_add1]+ [node_be_add2] + check_path1[j:]               
              visited_color2_localSearch = check_color[:j] + [col_map[node_be_add1]]+ [col_map[node_be_add2]] + check_color[j:]    
              path_edges_ts_LS2=deepcopy(sorted(new_path_edges_ts_LS2+path_edges_ts_LS22))
    
              if col_map[node_be_add1]==color_of_del_nod: 
                 l=0
              elif col_map[node_be_add2]==color_of_del_nod:   
                 l=0
              elif col_map[node_be_add2]!=color_of_del_nod:    
                 if col_map[node_be_add1]!=color_of_del_nod: 
                    l=1
                 elif col_map[node_be_add1]==color_of_del_nod: 
                    l=0   
                    
         elif neigh_connection==[]:
             path2_localSearch=path_input            
             visited_color2_localSearch=visited_color_input
             l=0
         return  path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l
           
        def LS2(path2_localSearch,visited_color2_localSearch,path_edges_input,path_edges_ts_LS2):
            j=0;l=0
            for i in (path_edges_input):  
              if len(visited_color2_localSearch)==len(color_list):
                  break
              if l==0:            
                  if i==0:
                    j=1
                  elif i!=0:  
                    i_back=i-1   
                    path_input=path2_localSearch
                    visited_color_input=visited_color2_localSearch  
                    path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l = find_new_path_LS2(path_input,visited_color_input,path_edges_input,path_edges_ts_LS2,i_back,j,i)
    
                    j+=1  
                    if i==path_edges_input[-1]:
                      path_input=path2_localSearch
                      visited_color_input=visited_color2_localSearch  
                      path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l = find_new_path_LS2(path_input,visited_color_input,path_edges_input,path_edges_ts_LS2,i_back,j,i)
              elif l==1:
                  j=0
                  list1=deepcopy(path_edges_ts_LS2)
                  path_edges_input=deepcopy(list1)              
                  path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l=LS2(path2_localSearch,visited_color2_localSearch,path_edges_input,path_edges_ts_LS2)
            return path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l
    
        path2_localSearch=deepcopy(path1_localSearch)
        path_edges_ts_LS2=deepcopy(path_edges_ts_LS1)
        visited_color2_localSearch=deepcopy(visited_color1_localSearch)
        
        path_edges_input=deepcopy(path_edges_ts_LS2)
        path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch,l=LS2(path2_localSearch,visited_color2_localSearch,path_edges_input,path_edges_ts_LS2)
    
        return path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch
        
    if __name__ == '__main__':        
            step=[]; number_interval=0; interval_span=[]; path_interval=[];interval_1=[]       
            while  current_time <= keys_TS[-1] and step!=0: 
                number_interval +=1
                current_node=[]
                if step==1:
                   step=0
                if current_time != keys_TS[-1]:
                   G, current_time, interval = G_for_interval(TS_current,current_time,del_nod)
                   interval_span.append(interval)        
                if current_time < keys_TS[-1]: 
                    if path!=[]:
                        current_node=deepcopy(path[-1])
                        if current_node in G and n==[]:
                            lo=1
                            n=list(G.neighbors(current_node))
                            interval_1=deepcopy(interval)
                            if n!=[]:
                              for x in n:
                                col_x=col_map[x]
                                if col_x in visited_color:
                                  n.remove(x)
                            while lo==1 and current_time < keys_TS[-1]: 
                                TS_current, del_nod= TS_updated(TS_current, visited_color, col_map,epsilon,current_time,path)            
                                if n!=[]:
                                  lo=0  
                                elif n==[]:
                                  del_nod1=deepcopy(del_nod)  
                                  del_nod1.remove(current_node) 
                                  G, current_time, interval = G_for_interval(TS_current,current_time,del_nod1)
                                  interval_span.append(interval)
                                  if current_node in G:
                                     n=list(G.neighbors(current_node))
                                     interval_1=deepcopy(interval)
                                  if n!=[]:
                                      for x in n:
                                        col_x=col_map[x]
                                        if col_x in visited_color:
                                          n.remove(x)
                                  if n!=[]:
                                       lo=0
                            G, current_time, interval = G_for_interval(TS_current,current_time,del_nod) 
                            interval_span.append(interval)
                    current_node =largeDeg_node(G,col_map,n,visited_color)    
                    TS_current, del_nod= TS_updated(TS_current, visited_color, col_map,epsilon,current_time,path)        
                elif current_time == keys_TS[-1] and n!=[]:
                    if step==[]:
                       step=1
                    current_node =largeDeg_node(G,col_map,n,visited_color)
                elif current_time == keys_TS[-1] and n==[]:
                    if step==[]:
                       step=1
                if current_node !=[]:
                    path.append(current_node) 
                    if interval_1!=[]:
                      path_interval.append(interval_1)
                    visited_color.append(col_map[current_node])
                    n=[]
                    if current_node in G:
                        n=list(G.neighbors(current_node)) 
                        interval_1=deepcopy(interval)
                        if n!=[]:
                           for x in n:
                             col_x=col_map[x]
                             if col_x in visited_color:
                                n.remove(x)
            def path_edges_ts(interval_span,path,path_interval):
              edges_ts=[]  
              for ii in range (len(path)-1):
                  n11=path[ii]; n12=path[ii+1]   
                  s=0   
                  for j in path_interval[ii]:  
                     if s==1:
                        break
                     if j in list(TS.keys()):
                        for (x1, x2) in TS[j]:
                          if s==1:
                             break                
                          X=[x1,x2]
                          if n11 in X:
                            if n12 in X:
                              edges_ts.append(j)   
                              s=1
              return  edges_ts   
            path_edges_ts=  path_edges_ts(interval_span,path,path_interval) 
            if len(visited_color) < len(color_list):
                path1_localSearch, visited_color1_localSearch, path_edges_ts_LS1 = local_search_edge(TS, path_edges_ts, col_map, path, visited_color, interval_span,path1_localSearch, visited_color1_localSearch)
                if len(visited_color1_localSearch) < len(color_list):
                   path2_localSearch, path_edges_ts_LS2, visited_color2_localSearch = local_search_node(TS, col_map,interval_span, path_edges_ts_LS1,path1_localSearch, visited_color1_localSearch)
                elif len(visited_color1_localSearch) == len(color_list):
                    path2_localSearch=[]
                    path_edges_ts_LS2=[]
                    visited_color2_localSearch=[]
                    
            t2 = time.time()
            time=t2-t1
            del t1, t2
            ################# results all together        
            res[data_ite][0] = len(path)
            res[data_ite][1] = len(path1_localSearch)
            res[data_ite][2] = len(path2_localSearch)
            res[data_ite][3] = time    
            #################



            