import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite Database connected: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    database = "data/patients.db"

    sql_create_patients_table = """ CREATE TABLE IF NOT EXISTS patients (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        age integer,
                                        gender text,
                                        address text,
                                        phone_number text,
                                        email text,
                                        bmi real
                                    ); """

    sql_create_records_table = """ CREATE TABLE IF NOT EXISTS records (
                                       id integer PRIMARY KEY,
                                       patient_id integer NOT NULL,
                                       visit_date text NOT NULL,
                                       diagnosis text,
                                       treatment text,
                                       medication text,
                                       FOREIGN KEY (patient_id) REFERENCES patients (id)
                                   ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_records_table)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
