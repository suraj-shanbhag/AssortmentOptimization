import cPickle

import pandas as pd
import numpy as np
from normalize import get_demand_for_each_product
from preprocess_data import Preprocess
from collections import OrderedDict
from operator import itemgetter
import matplotlib.pyplot as plt

# preprocess and database setup
# prepare peoples data frame
# prepare probabilistic data frame
# prepare demand data frame
# obtain cannible spectrum
class Sales_Analyser(object):
    def __init__(self):
        self.preprocessed_data = Preprocess()
        self.sku_name_list = []
        self.column_mapping = {}

    def intersect(self, a, b):
        return list(set(a) & set(b))

    def peoples_data_frame(self):
        people_grid = []
        sku_against_people = self.preprocessed_data.get_sku_against_people()
        for b_sc, household_id in sku_against_people.iteritems():
            people_row = []
            for _b_sc, _household_id in sku_against_people.iteritems():
                intersection_result = self.intersect(household_id, _household_id)
                people_row.append(intersection_result)
            self.sku_name_list.append(b_sc)
            people_grid.append(people_row)
        people_data_frame = pd.DataFrame(people_grid, index=self.sku_name_list, columns=self.sku_name_list)
        return people_data_frame

    def get_probability_data_frame(self):

        step_3_grid = get_demand_for_each_product(self.peoples_data_frame())
        self.create_column_mapping()
        probablity_data_frame = pd.DataFrame(step_3_grid, index=self.sku_name_list, columns=self.sku_name_list)
        return probablity_data_frame

    def demand_data_frame(self):
        demand_grid = []
        sku_against_demand = self.preprocessed_data.demandForEachProduct()
        probability_data_frame = self.get_probability_data_frame()
        for i in range(len(probability_data_frame.index)):
            multiplier = sku_against_demand[self.column_mapping[i]]
            demand_row = []
            for value in probability_data_frame.iloc[i]:
                demand_row.append(value * multiplier)
            demand_grid.append(demand_row)
        demand_data_frame = pd.DataFrame(demand_grid, index=self.sku_name_list, columns=self.sku_name_list)
        with open("demand_data_frame.pkl", "wb") as peo:
            cPickle.dump(demand_data_frame, peo)
        return demand_data_frame

    def create_column_mapping(self):
        for i in range(len(self.sku_name_list)):
            self.column_mapping[i] = str(self.sku_name_list[i])

    def softmax(self,x):
        e_x = np.exp(x)
        return (e_x / e_x.sum(axis=0))

    def cannibleSpectrum(self):
        sku_against_demand = self.preprocessed_data.demandForEachProduct()
        demand_data_frame = self.demand_data_frame()
        with open("price_against_sc_dict.pkl", "r") as dk:
            price_against_sc = cPickle.load(dk)
        binary_difference_progress = [[False for i in range(len(demand_data_frame.index))] for i in
                                      range(len(demand_data_frame.index))]
        cannibal_spectrum = [0] * len(demand_data_frame.index)
        for i in range(len(demand_data_frame.index)):
            for j in range(len(demand_data_frame.columns)):
                if (not (i == j or binary_difference_progress[i][j])):
                    # print i,j
                    if (demand_data_frame.iloc[i][j] > demand_data_frame.iloc[j][i]):
                        value = demand_data_frame.iloc[i][j] - demand_data_frame.iloc[j][i]
                        binary_difference_progress[i][j], binary_difference_progress[j][i] = True, True
                        cannibal_spectrum[j] += value
                        cannibal_spectrum[i] -= value
                    else:
                        value = demand_data_frame.iloc[j][i] - demand_data_frame.iloc[i][j]
                        binary_difference_progress[i][j], binary_difference_progress[j][i] = True, True
                        cannibal_spectrum[i] += value
                        cannibal_spectrum[j] -= value
        normalized = np.asarray(cannibal_spectrum) / np.linalg.norm(np.asarray(cannibal_spectrum))
        print normalized[8],normalized[22]
        print normalized.sum()
        normalized_cannibal_spectrum_dict = {}
        for i in range(len(demand_data_frame.index)):
            normalized_cannibal_spectrum_dict[demand_data_frame.index[i]] = normalized[i]
        sorted_cannible_spectrum_dict = OrderedDict(sorted(normalized_cannibal_spectrum_dict.items(), key=itemgetter(1)))
        normalized_demand_share = {}
        inital_demand_share={}
        for k, v in sorted_cannible_spectrum_dict.iteritems():
            result = sku_against_demand[k] * v
            normalized_demand_share[k] = (result + sku_against_demand[k]) * price_against_sc[k]
            inital_demand_share[k]=sku_against_demand[k]*price_against_sc[k]
        # with open("final_demand.pkl","wb") as dd:
        #     cPickle.dump((inital_demand_share,normalized_demand_share),dd)
sa = Sales_Analyser()
sa.cannibleSpectrum()
