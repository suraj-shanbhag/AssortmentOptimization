import psycopg2


class Database_Connection(object):

    def __init__(self, user="surajus", database="dunhumby", host="localhost", port=5432):
        try:
            connection = psycopg2.connect(database=database, user=user, host=host, port=port)
        except:
            print "Try again"

        self.cursor = connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def execute_query_with_list_parameters(self, query, list_parameters):
        placeholders = ', '.join(str(item) for item in list_parameters)
        query = query % placeholders
        self.cursor.execute(query, placeholders)
        result = self.cursor.fetchall()
        return result
