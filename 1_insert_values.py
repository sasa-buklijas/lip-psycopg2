import argparse
import time
import random
import db_config
import psycopg2
from psycopg2.extras import execute_values


def main():
    parser = argparse.ArgumentParser(description='Number of inserts.')
    parser.add_argument('noi', type=int, nargs='?', default=5, help='Number of inserts (default is 5)')
    args = parser.parse_args()
    noi = args.noi

    conn = psycopg2.connect(host=db_config.host, 
                            port=db_config.port,
                            user=db_config.user,
                            password=db_config.password,
                            database=db_config.database,)
    cur = conn.cursor()

    to_add = []
    for _ in range(noi):
        temperature_time = time.time_ns()
        temperature = random.randint(1, 100)
        to_add.append((temperature_time, temperature))

    # if even one is wrong, none will be executed
    # it is all or none
    #to_add.append((123, 'wrong_type'))
    
    # https://www.psycopg.org/docs/extras.html#psycopg2.extras.execute_batch
    st = time.time()
    _ = execute_values(cur, "INSERT INTO data (time, temp) VALUES %s", to_add)
    # print(f'{_=}')

    # Make the changes to the database persistent
    conn.commit()
    et = time.time()
    print(f'{noi} INSERT INTO took {et-st:.4f} seconds.')


    # Close communication with the database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
