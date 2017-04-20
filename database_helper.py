from database_connection import Database_Connection


class Database_Helper(object):
    def __init__(self):
        self.database_cursor = Database_Connection()

    def get_brand_subcommodity_tupe_for_department_commodity(self, department='GROCERY', commodity='COOKIES/CONES'):
        query = "select distinct brand,sub_commodity_desc from products where DEPARTMENT='%s' AND commodity_desc='%s'" % (
            department, commodity)
        return self.database_cursor.execute_query(query)

    def product_ids_of_subcommodity(self, brand, sub_commodity_desc, department='GROCERY', commodity='COOKIES/CONES'):
        query = "select product_id from products where DEPARTMENT='%s' AND commodity_desc='%s' AND brand='%s'AND sub_commodity_desc='%s'" % (
            department, commodity, brand, sub_commodity_desc)
        return self.database_cursor.execute_query(query)

    def house_hold_ids_from_product_id(self, list_parameters):
        query = "SELECT distinct household_key FROM transaction_data WHERE product_id IN (%s)"
        return self.database_cursor.execute_query_with_list_parameters(query, list_parameters)

    def count_of_transactions_per_product_from_product_id(self, list_parameters):
        query = "SELECT count(*) FROM transaction_data WHERE product_id IN (%s)"
        return self.database_cursor.execute_query_with_list_parameters(query, list_parameters)[0][0]
