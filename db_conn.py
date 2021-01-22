import psycopg2

def main():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        
        conn = psycopg2.connect(
            host="172.30.1.22",
            database="tour",
            user="postgres",
            password="!Q@W#E$R"
        )
        print("Connection established")

        # create a cursor
        cursor = conn.cursor()

        # Drop previous table of same name if one exists
        # cursor.execute("DROP TABLE IF EXISTS dish_names ;")
        # cursor.execute("DROP TABLE IF EXISTS taste_adj ;")
        # print("Finished dropping table (if existed)")
        cursor.execute("DROP TABLE IF EXISTS retrieve_nums2 ;")
        print("Finished dropping table (if existed)")

        # Create a table
        # cursor.execute("""CREATE TABLE dish_names (
        #                     name_ko TEXT PRIMARY KEY,
        #                     name_en TEXT, type VARCHAR(50), country CHAR(2)    
        #                 );""")
        # cursor.execute("""CREATE TABLE taste_adj (
        #                     taste_ko VARCHAR(50) PRIMARY KEY,
        #                     phonetic VARCHAR(50), synonyms TEXT, taste_en VARCHAR(50)    
        #                 );""")
            
        cursor.execute("""
            CREATE TABLE retrieve_nums2 (
                idx serial PRIMARY KEY,
                name_ko TEXT,
                taste_ko TEXT,
                search_word1 TEXT, 
                con_and BIGINT,
                search_word2 TEXT, 
                con_around4 BIGINT,
                update_datetime timestamp
            );""")
        print("Finished creating table")
        conn.commit()

        foods_arr = ['백반', '산채정식', '쌈밥정식', '한정식']
        eng_arr = ['Baekban', 'Sanchaejeongsik', 'Ssambapjeongsik', 'Hanjeongsik']

        # for i, nm in enumerate(foods_arr) :
        #     print(" I >> ", i, nm)
        #     # Insert some data into the table
        #     cursor.execute("""INSERT INTO dish_names (
        #                         name_ko, name_en, type, country
        #                     ) VALUES ( %s, %s, %s, %s );"""
        #                     , (nm, eng_arr[i], "상차림", "KO")
        #                 )
        # print("Inserted 4 rows of data")
        # conn.commit()


        # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        #db_version = cur.fetchone()
        #print(db_version)

        cursor.execute("SELECT * FROM dish_names WHERE name_ko='누룽지' ")
        rows = cursor.fetchone()
        # while rows is not None: 
        for row in rows:
           print(row)
        

        # close the communication with the PostgreSQL
        cursor.close()
        print('222')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

conn = None
cursor = None
def connect():
    global conn
    global cursor
    try:
        print('Connecting to the PostgreSQL database...')
        
        conn = psycopg2.connect(
            host="172.30.1.22",
            database="tour",
            user="postgres",
            password="!Q@W#E$R"
        )
        print("Connection established")

        
        cursor = conn.cursor() # create a cursor
        return cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update_result(p1, p2, p3, p4, p5):
    global conn
    global cursor
    try:
        if p1 == 2:
            cursor.execute("""
                UPDATE retrieve_nums
                SET search_word1 = %s, 
                    con_and = %s,
                    update_datetime = now()
                WHERE name_ko = %s
                AND taste_ko = %s;"""
                , (p2, p3, p4, p5)
            )
            print("update established (", p2, "=", p3, ")")
        else:
            cursor.execute("""
                UPDATE retrieve_nums
                SET search_word2 = %s, 
                    con_around4 = %s,
                    update_datetime = now()
                WHERE name_ko = %s
                AND taste_ko = %s;"""
                , (p2, p3, p4, p5)
            )
            print("update established (", p2, "=", p3, ")")
        conn.commit()
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def dbclose():
    global conn
    global cursor
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

if __name__ == '__main__':
    main() 