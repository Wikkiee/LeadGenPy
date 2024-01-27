import mysql.connector
import  Configs.config as config

def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host=config.DATABASE_CONFIG["host"],
            user=config.DATABASE_CONFIG["user"],
            password=config.DATABASE_CONFIG["password"],
            database=config.DATABASE_CONFIG["database"]
        )
        
        if not connection.is_connected():
            print("Failed to connect to MySQL")
            return None
        
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                lead_id INT NOT NULL AUTO_INCREMENT,
                business_name VARCHAR(255) NOT NULL,
                business_address VARCHAR(255),
                business_email VARCHAR(255),
                mobile_number VARCHAR(15),
                website_url VARCHAR(255),
                business_category VARCHAR(50),
                ratings VARCHAR(4),
                review_counts int,
                top_review_1 VARCHAR(1000),
                top_review_2 VARCHAR(1000),
                top_review_3 VARCHAR(1000), 
                google_map_url VARCHAR(255),
                personalized_email_subject VARCHAR(255),
                personalized_email_content VARCHAR(5000),
                status VARCHAR(8),
                PRIMARY KEY (lead_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS allabolag (
                allabolag_id INT NOT NULL AUTO_INCREMENT,
                lead_id INT NOT NULL,
                organization_number VARCHAR(255) DEFAULT 'null',
                registered_name VARCHAR(255) DEFAULT 'null',
                ceo_name VARCHAR(255) DEFAULT 'null',
                type_of_business VARCHAR(255) DEFAULT 'null',
                revenue VARCHAR(255) DEFAULT "0",
                number_of_employees INT DEFAULT 0,
                year_of_registeration VARCHAR(255) DEFAULT 'null',
                PRIMARY KEY (allabolag_id),
                FOREIGN KEY (lead_id) REFERENCES leads(lead_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue_track(
                id INT NOT NULL AUTO_INCREMENT,
                allabolag_id INT NOT NULL,
                revenue_track_2022 VARCHAR(50) DEFAULT "null",
                revenue_track_2021 VARCHAR(50) DEFAULT "null",
                revenue_track_2020 VARCHAR(50) DEFAULT "null",
                revenue_track_2019 VARCHAR(50) DEFAULT "null",
                revenue_track_2018 VARCHAR(50) DEFAULT "null",
                revenue_track_2017 VARCHAR(50) DEFAULT "null",
                PRIMARY KEY (id),
                FOREIGN KEY (allabolag_id) REFERENCES allabolag(allabolag_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS headcounts(
                id INT NOT NULL AUTO_INCREMENT,
                allabolag_id INT NOT NULL,
                headcount_2022 INT DEFAULT 0,
                headcount_2021 INT DEFAULT 0,
                headcount_2020 INT DEFAULT 0,
                headcount_2019 INT DEFAULT 0,
                headcount_2018 INT DEFAULT 0,
                headcount_2017 INT DEFAULT 0,
                PRIMARY KEY (id),
                FOREIGN KEY (allabolag_id) REFERENCES allabolag(allabolag_id)
            )
        """)

        connection.commit()
        return connection
      
    except mysql.connector.errors.DatabaseError as error:
        # traceback.print_exc()
        print(error)

if __name__ == "__main__":
    print( get_database_connection() )
