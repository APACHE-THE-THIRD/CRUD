import sqlite3


class sqlite3_connector:

    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.create_table()
        self.insert_init_data()

    def create_table(self):
        c = self.conn.cursor()

        c.execute("DROP TABLE IF EXISTS tasks")
        c.execute('''CREATE TABLE tasks
                     (id INT, name TEXT, surname TEXT, task TEXT)''')

        self.conn.commit()
        c.close()

    def insert_init_data(self):
        c = self.conn.cursor()

        tasks = [('1', 'name1', 'sur1', 'task1'),
                     ('2', 'name2', 'sur2', 'task2'),
                     ('3', 'name3', 'sur3', 'task3'),
                     ]
        c.executemany('INSERT INTO tasks VALUES (?,?,?,?)', tasks)

        self.conn.commit()
        c.close()

    def select_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks ORDER BY id')
        result = c.fetchall()
        c.close()
        return result

    def print_all(self):
        c = self.conn.cursor()
        for row in c.execute('SELECT * FROM tasks ORDER BY id'):
            print(row)
        c.close()

    def update_one(self, record_id, name, surname, task):
        c = self.conn.cursor()
        c.execute('UPDATE  tasks SET name=?, surname=?, task=? WHERE id = ?', (name, surname, task,record_id,))
        self.conn.commit()
        c.close()

        self.print_all()
    def insert_one(self, record_id, name, surname, task):
        c = self.conn.cursor()
        c.execute('INSERT INTO  tasks VALUES (?,?,?,?)', (record_id, name, surname, task))
        self.conn.commit()
        c.close()

    def delete_one(self, record_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?',(record_id,))
        self.conn.commit()
        c.close()

    def get_max_task_id(self):
        c = self.conn.cursor()
        res = c.execute('SELECT MAX(id) FROM tasks ORDER BY id')
        max_id = res.fetchone()[0]

        if max_id is None:
            max_id =  0

        c.close()
        return max_id

