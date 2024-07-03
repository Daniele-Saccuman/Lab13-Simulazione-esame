from database.DB_connect import DBConnect
from model.edge import Edge
from model.state import State


class DAO():
    @staticmethod
    def getAllYears():

        conn = DBConnect.get_connection()
        if conn is not None:
            result = []

            cursor = conn.cursor(dictionary=True)
            query = """select distinct year (`datetime`) as anno
                        from sighting s """
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            conn.close()
            return result
        else:
            print("Errore nella connessione")
            return None

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape
                from sighting s"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                       from state s"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1, n.state2
                    from neighbor n   """

        cursor.execute(query)

        for row in cursor:
            result.append(Edge(idMap[row["state1"]], idMap[row["state2"]]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesi(year, shape, stato1, stato2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor()
        query = """select count(*) as peso
                        from sighting s 
                        where s.shape = %s
                        and Year(s.`datetime`) = %s
                        and (s.state = %s or s.state = %s)"""

        cursor.execute(query, (shape, year, stato1, stato2))

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return result
