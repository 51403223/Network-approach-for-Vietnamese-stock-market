periods = [
    {'start': '20141030', 'end': '20160313'},
    {'start': '20141219', 'end': '20160502'},
    {'start': '20150207', 'end': '20160621'},
    {'start': '20150329', 'end': '20160810'},
    {'start': '20150518', 'end': '20160929'},
    {'start': '20150707', 'end': '20161118'},
    {'start': '20150826', 'end': '20170107'},
    {'start': '20151015', 'end': '20170226'},
    {'start': '20151204', 'end': '20170417'},
    {'start': '20160123', 'end': '20170606'},
    {'start': '20160313', 'end': '20170726'},
]

import formula as myFunc
import GraphMethod as gm
import pandas as pd
num_of_periods = len(periods)
#data_path = 'E:/DoAn2/tdt_2017_do-an2/source code/test/'
data_path = 'E:/DoAn2/tdt_2017_do-an2/source code/data/'
csv_list = gm.create_dataframe_list(data_path)
# analyze mean and deviation of coefficient
mean_dev_table = pd.DataFrame(columns=['Mean', 'Deviation'])
coeff_list_of_all_period = []
for period_index in range(0, num_of_periods):
    print '=================================================='
    print 'PERIOD_', period_index
    current_period = periods[period_index]
    returns_list_of_current_period = []
    start_date = current_period['start']
    end_date = current_period['end']
    for csv in csv_list:
        returns_list_of_current_period.append(myFunc.create_returns_list(csv, start_date, end_date))
    mean,dev,coeff_list = myFunc.mean_and_deviation2(returns_list_of_current_period)
    mean_dev_table = mean_dev_table.append({'Mean': mean, 'Deviation': dev}, ignore_index=True)
    coeff_list_of_all_period.append(coeff_list)
mean_dev_table.plot(y=['Mean','Deviation'])
# plot distribution of coefficient
import seaborn as sns
for period_index in range(0, num_of_periods):
    coeff_list = coeff_list_of_all_period[period_index]
    label = 'Period {}'.format(period_index)
    sns.distplot(coeff_list, hist=False, label=label)
sns.plt.show()

# graph making
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ,0.9]
graph_list_of_all_periods = [] # list of list of graph for different period
for period_index in range(0, num_of_periods):
    print '=================================================='
    print 'PERIOD_', period_index
    current_period = periods[period_index]
    returns_list_of_current_period = []
    start_date = current_period['start']
    end_date = current_period['end']
    for csv in csv_list:
        returns_list_of_current_period.append(myFunc.create_returns_list(csv, start_date, end_date))
    graph_list_of_current_period = [] # list of graph for different threshold
    for threshold in thresholds:
        print 'Making graph at threshold ', threshold
        graph_list_of_current_period.append(gm.make_graph(returns_list_of_current_period, threshold))
    graph_list_of_all_periods.append(graph_list_of_current_period)
# analyze size of maximum clique
maximum_clique_table = pd.DataFrame(columns=thresholds)
import networkx as nx
for graph_list_of_current_period in graph_list_of_all_periods:
    maximum_clique_sizes = []
    for graph in graph_list_of_current_period:
        if(len(graph.nodes) != 0):
            max_cliq_size = nx.graph_clique_number(graph)
            maximum_clique_sizes.append(max_cliq_size)
        else:
            maximum_clique_sizes.append(1)
    # add value to table
    df = pd.DataFrame(data=[maximum_clique_sizes], columns=thresholds)
    maximum_clique_table = maximum_clique_table.append(df)

# analyze structure of maximum clique
import numpy as np
structure_list_of_all_periods = []
for period_index in range(0, num_of_periods):
    graph_of_threshold02 = graph_list_of_all_periods[period_index][1] # graph of threshold o.2
    if(len(graph_of_threshold02.nodes) != 0):
        max_cliques = gm.find_maximum_cliques(graph_of_threshold02)
        num_of_max_cliques = len(max_cliques)
        size_of_max_clique = len(max_cliques[0])
        union = np.unique(max_cliques)
        size_union = len(union)
        stock_in_union = gm.get_node_name_list(list_clique=union, list_dataframe=csv_list)
        structure_list_of_all_periods.append([num_of_max_cliques, size_of_max_clique, size_union, str(stock_in_union)])
structure_table = pd.DataFrame(data=structure_list_of_all_periods, columns=['Num of max cliques', 'Size of max clique', 'size union', 'name'])

# find intersect of stock in union
# stocks = []
# for structure in structure_list_of_all_periods:
#     list = structure[3]
#     list = list.replace('[','')
#     list = list.replace(']','')
#     stocks.append(list.split(', '))
# intersect = stocks[0].inter
# for i in range(1, len(stocks) - 1):
#     intersect = int

# for period_index in range(0, num_of_periods):
#     test = structure_table['name'][period_index]
#     if (test.find('DLG') != -1 and test.find('FLC') != -1 and test.find('HAG') != -1
#         and test.find('HAI') != -1  and test.find('HAR') != -1  and test.find('HHS') != -1
#         and test.find('HQC') != -1 and test.find('SHS') != -1 and test.find('TSC') != -1
#         and test.find('VHG') != -1):
#         print period_index

structure_list_of_all_periods06 = []
for period_index in range(0, num_of_periods):
    graph_of_threshold06 = graph_list_of_all_periods[period_index][5] # graph of threshold o.6
    if(len(graph_of_threshold06.nodes) != 0):
        max_cliques = gm.find_maximum_cliques(graph_of_threshold06)
        num_of_max_cliques = len(max_cliques)
        size_of_max_clique = len(max_cliques[0])
        union = np.unique(max_cliques)
        size_union = len(union)
        stock_in_union = gm.get_node_name_list(list_clique=union, list_dataframe=csv_list)
        structure_list_of_all_periods06.append([num_of_max_cliques, size_of_max_clique, size_union, str(stock_in_union)])
structure_table2 = pd.DataFrame(data=structure_list_of_all_periods06, columns=['Num of max cliques', 'Size of max clique', 'size union', 'name'])