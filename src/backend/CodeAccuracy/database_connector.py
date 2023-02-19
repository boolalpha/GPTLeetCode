import mysql.connector

class DatabaseConnector():
    def __init__(self, hostname, username, password, port):

        self.database_connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password
        )
        self.cursor = self.database_connection.cursor()
        self.wildcard = "%s"


    # TODO create table
    def create_table():
        pass


    def close(self):
        self.database_connection.close()


    def commit(self):
        self.database_connection.commit()


    def insert_into_table(self, table, cols, values, ignore = False):
        try:
            # determine if this is a single insert or an insert of many values
            if isinstance(values, list):
                # make sure all lists within the list are of equal value
                iterator = iter(values)
                length = len(next(iterator))
                if not all(len(row) == length for row in iterator):
                    raise Exception('Not all inserted rows have same length')
            elif isinstance(values, tuple):
                # be sure there is the same amount of values to columns
                if len(cols) != len(values):
                    raise Exception("Mismatch in length of columns and values")
            else:
                raise Exception("Not a valid type passed in for values")

            # setup insert or insert ignore
            if ignore:
                sql = 'INSERT IGNORE INTO ' + table
            else:
                sql = 'INSERT INTO ' + table

            # add columns
            sql += f" ({', '.join(map(str,cols))})"

            if isinstance(values, list):
                # add wildcard as value holders
                # get values[0] to get the first element length which will match all other lengths
                sql += f" VALUES ({', '.join([self.wildcard] * len(values[0]))})"
                self.cursor.executemany(sql, values)
            elif isinstance(values, tuple):
                # add wildcard as value holders
                sql += f" VALUES ({', '.join([self.wildcard] * len(values))})"
                self.cursor.execute(sql, values)

            self.database_connection.commit()
            return True

        except Exception as e:
            raise e


    def update_table(self, table, cols, values, condition):
        try:
            sql = f"UPDATE {table} SET "
            set_list = [f"{col} = {self.wildcard}" for col in cols]
            sql += f", ".join(set_list)
            if condition:
                sql += condition
            self.cursor.execute(sql, values)
            self.database_connection.commit()

        except Exception as e:
            raise e


    def select_from_table(self, table, col_choice, col=None, value=None, comparison=None):
        try:
            sql = f"SELECT {col_choice} FROM {table}"
            if col and value:
                where_list = []
                for i in range(len(col)):
                    where_list.append(f"{col[i]} {comparison[i] if comparison else '='} {self.wildcard}")
                sql +=  " WHERE " + " AND ".join(where_list)
                self.cursor.execute(sql, value)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    
    def get_last_inserted_primary_key(self):
        try:
            sql = "SELECT LAST_INSERT_ID()"
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except Exception as e:
            raise e


    def get_all_problems_for_submission(self):
        sql = """
SELECT * FROM ChatGPT.leetcode_benchmark as lb
WHERE 
	lb.openai_response IS NOT NULL
    AND
    lb.id NOT IN (
		SELECT problem_id FROM ChatGPT.leetcode_success as ls
	)
"""
        self.cursor.execute(sql)
        return self.cursor.fetchall


    def get_all_problems(self):
        sql = """
SELECT lb.*, ls.succeeded, ls.runtime, ls.runtime_beats, ls.memory, ls.memory_beats, ls.error_type, ls.error_message, ls.total_testcases, ls.testcases_passed, GROUP_CONCAT(lt.topic_tag SEPARATOR ',')
FROM ChatGPT.leetcode_tags as lt
INNER JOIN ChatGPT.leetcode_benchmark as lb ON lb.id = lt.problem_id
INNER JOIN ChatGPT.leetcode_success as ls ON lb.id = ls.problem_id
WHERE lb.locked is False
GROUP BY lt.problem_id  
"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def set_mode(self):
        sql = """
SET sql_mode=(SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''));        
"""
        self.cursor.execute(sql)


    def get_distinct_algorithm_topic_tags(self):
        sql = """
SELECT DISTINCT lt.topic_tag FROM ChatGPT.leetcode_tags as lt
INNER JOIN ChatGPT.leetcode_benchmark as lb ON lt.problem_id = lb.id
WHERE 
	lt.topic_tag NOT IN ("shell", "database")
    AND
    lb.locked = False
ORDER BY lt.topic_tag ASC;
"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()
