import time
import random
import psycopg2
import db_config


def main():
    conn = psycopg2.connect(host=db_config.host, 
                            port=db_config.port,
                            user=db_config.user,
                            password=db_config.password,
                            database=db_config.database,)
    cur = conn.cursor()

    temperature_time = time.time_ns()
    temperature = random.randint(1, 100)
    #print(f'{temperature_time=} {temperature=}')
    
    cur.execute("INSERT INTO data (time, temp) VALUES (%s, %s)", (temperature_time, temperature))

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
