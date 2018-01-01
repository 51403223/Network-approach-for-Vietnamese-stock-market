import numpy as np
import pandas as pd
import os
import networkx as nx
from math import sqrt
import matplotlib.pyplot as plt
import formula as myFunc


def create_dataframe_list(data_path):
    list = []
    filenames = os.listdir(data_path)
    for name in filenames:
        list.append(pd.read_csv(data_path + name))
    return list

def save_graph(G, file_path):
    nx.write_edgelist(G, file_path, data=['weight'])
    return

def load_graph(file_path):
    file = pd.read_csv(file_path, names=['d1', 'd2', 'weight'], sep=' ')
    G = nx.from_pandas_dataframe(file, source='d1', target='d2', edge_attr='weight', create_using=nx.Graph())
    return G

def drawGraph(G):
    nx.draw(G)
    plt.show()
    return

def make_graph(returns_list, threshhold):
    G = nx.Graph()
    n = len(returns_list)
    num_of_day = len(returns_list[0])
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            coeff = myFunc.calc_coeff(returns_list[i], returns_list[j], num_of_day)
            if(coeff >= threshhold):
                G.add_edge(i, j, weight=coeff)
    return G

def find_maximum_cliques(G):
    maximal_cliques = list(nx.find_cliques(G))
    maximum_clique_size = len(max(maximal_cliques, key=lambda clique: len(clique))) # so dinh cua 1 maximum clique
    maximum_cliques = [clique for clique in maximal_cliques if len(clique) == maximum_clique_size]
    return maximum_cliques

def get_node_name_list(list_clique, list_dataframe):
    list_name_return = []
    for i in list_clique:
        list_name_return.append(list_dataframe[i]['<Ticker>'][0])
    return list_name_return

# def find_maximum_cliques2(G):
#     max_size = nx.graph_clique_number(g)
#     lst = nx.find_cliques(g)
#     cliques5 = [ clq for clq in lst if len(clq) >= 5]