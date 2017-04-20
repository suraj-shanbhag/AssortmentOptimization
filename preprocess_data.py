from database_helper import Database_Helper


class Preprocess(object):
    def __init__(self):
        self.__database_helper = Database_Helper()

    def get_id_against_brand_sc_dict(self):
        id_against_brand_sc = {}
        for row in self.__database_helper.get_brand_subcommodity_tupe_for_department_commodity():
            brand, sub_commodity_desc = row[0], row[1]
            id_set = []
            for product_id in self.__database_helper.product_ids_of_subcommodity(brand=brand,
                                                                                 sub_commodity_desc=sub_commodity_desc):
                id_set.append(product_id[0])
            id_against_brand_sc[str(brand) + "_" + str(sub_commodity_desc)] = id_set
        return id_against_brand_sc

    def get_sku_against_people(self):
        sku_against_people = {}
        for brand_sub_commodity, product_ids in self.get_id_against_brand_sc_dict().iteritems():
            # print brand_sub_commodity
            household_id_set = []
            for id in self.__database_helper.house_hold_ids_from_product_id(product_ids):
                household_id_set.append(id[0])
            sku_against_people[brand_sub_commodity] = household_id_set
        return sku_against_people

    def demandForEachProduct(self):
        __sku_against_demand = {}
        for brand_sub_commodity, product_ids in self.get_id_against_brand_sc_dict().iteritems():
            number_of_transactions = self.__database_helper.count_of_transactions_per_product_from_product_id(product_ids)
            __sku_against_demand[brand_sub_commodity] = number_of_transactions
        return __sku_against_demand
# pp=Preprocess()
# print pp.demandForEachProduct()