import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Credentials (Use environment variables)
DB_NAME = os.getenv("DB_NAME", "ERPDB")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "root")
HOST = os.getenv("DB_HOST", "localhost")

# Create Database if it doesn't exist
def create_database():
    try:
        print("Creating database...")
        connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
        connection.close()
        print(f"Database '{DB_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Initialize Database Tables
def init_db():
    create_database()
    try:
        connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DB_NAME)
        cursor = connection.cursor()
        print("Initializing database tables...")
        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
            userid INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'User') DEFAULT 'User',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            ,
            """
            CREATE TABLE IF NOT EXISTS customer (
            customerid INT AUTO_INCREMENT PRIMARY KEY,
            customerName VARCHAR(255) NOT NULL,
            emailAddress VARCHAR(255) NOT NULL UNIQUE,
            phoneNumber VARCHAR(15) NOT NULL UNIQUE,
            addressLine1 VARCHAR(255) NOT NULL,
            addressLine2 VARCHAR(255),
            gstNumber VARCHAR(20) UNIQUE,
            city VARCHAR(100) NOT NULL,
            state VARCHAR(100) NOT NULL,
            pinCode VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_city (city),
            INDEX idx_state (state)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS rfq (
            rfqid INT AUTO_INCREMENT PRIMARY KEY,
            customerid INT,
            location VARCHAR(255) NOT NULL,
            country VARCHAR(100) NOT NULL,
            requestVia VARCHAR(100) NOT NULL,
            requestReferenceNumber VARCHAR(100) UNIQUE NOT NULL,
            typeOfGoods TEXT NOT NULL,
            lastDateToSubmit DATE NOT NULL,
            contactPerson VARCHAR(255) NOT NULL,
            contactPersonNumber VARCHAR(15) NOT NULL,
            contactPersonEmail VARCHAR(255) NOT NULL,
            status BOOLEAN DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (customerid) REFERENCES customer(customerid) ON DELETE CASCADE,
            INDEX idx_country (country),
            INDEX idx_lastDate (lastDateToSubmit)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS quotation (
                quotationid INT AUTO_INCREMENT PRIMARY KEY,
                customerid INT,
                rfqid INT,
                name VARCHAR(255) NOT NULL,
                emailAddress VARCHAR(255) NOT NULL,
                phoneNumber VARCHAR(15) NOT NULL,
                termsAndConditions TEXT NOT NULL,
                paymentTerms TEXT NOT NULL,
                taxAndDuties TEXT NOT NULL,
                briefDescription TEXT NOT NULL,
                deliveryDate DATE NOT NULL,
                packageAndForwarding TEXT NOT NULL,
                createdBy INT NULL,
                AdminApproved BOOLEAN DEFAULT NULL,
                log JSON NOT NULL DEFAULT ('[]'),
                itemDetails JSON NOT NULL DEFAULT ('[]'),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customerid) REFERENCES customer(customerid) ON DELETE CASCADE,
                FOREIGN KEY (rfqid) REFERENCES rfq(rfqid) ON DELETE CASCADE,
                FOREIGN KEY (createdBy) REFERENCES users(userid) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
           CREATE TABLE IF NOT EXISTS EmployeeRecords (
                EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                EmailAddress VARCHAR(255) UNIQUE,
                PhoneNumber VARCHAR(20),
                PermanentWorkType VARCHAR(255),
                TemporaryWorkType VARCHAR(255),
                TillTime DATE,
                ReasonForLayoff TEXT,
                ContributionToCompany TEXT,
                AddressLine1 VARCHAR(255),
                AddressLine2 VARCHAR(255),
                WorkType VARCHAR(255),
                City VARCHAR(100),
                State VARCHAR(100),
                PinCode VARCHAR(20),
                DateOfJoining DATE
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS purchase_order (
                workordernumber INT AUTO_INCREMENT PRIMARY KEY,
                customerid INT,
                quotationid INT,
                employeeid INT,
                po_number VARCHAR(50) UNIQUE NOT NULL,
                customer VARCHAR(255) NOT NULL,
                po_date DATE NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                project_engineers JSON,
                quality_engineers JSON,
                delivery_date DATE,
                status VARCHAR(50) DEFAULT 'Pending',
                remarks TEXT,
                contact_person_name VARCHAR(255),
                contact_person_email VARCHAR(255),
                contact_person_phone VARCHAR(20),
                project_name VARCHAR(255),
                item_details JSON,
                work_order_issue_date DATE,
                instructions_for_delivery TEXT,
                critical_notes TEXT,
                logs JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (customerid) REFERENCES customer(customerid) ON DELETE CASCADE,
                FOREIGN KEY (quotationid) REFERENCES quotation(quotationid) ON DELETE CASCADE,
                FOREIGN KEY (employeeid) REFERENCES EmployeeRecords(employeeid) ON DELETE SET NULL
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS bmo (
                workordernumber INT PRIMARY KEY,
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber) ON DELETE CASCADE
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS annexure (
                annexureid INT AUTO_INCREMENT PRIMARY KEY,
                annexure_number VARCHAR(50),
                annexure_type VARCHAR(50),
                process VARCHAR(255),
                type_of_goods VARCHAR(255),
                vendorsid INT,
                status ENUM('Approve', 'Reject', 'Pending') DEFAULT 'Pending',
                aosn_details JSON, 
                logs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS production_slip (
                workordernumber INT PRIMARY KEY,
                slip_number VARCHAR(50),
                project_name VARCHAR(255),
                customer VARCHAR(255),
                slip_date DATE,
                project_engineer VARCHAR(255),
                quality_engineer VARCHAR(255),
                store VARCHAR(255),
                account VARCHAR(255),
                special_instruction TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                logs TEXT,
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber) ON DELETE CASCADE
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS vendors (
                vendorsid INT AUTO_INCREMENT PRIMARY KEY,
                vendorName VARCHAR(255) NOT NULL,
                emailAddress VARCHAR(255) NOT NULL UNIQUE,
                phoneNumber VARCHAR(15) NOT NULL UNIQUE,
                addressLine1 VARCHAR(255) NOT NULL,
                addressLine2 VARCHAR(255),
                gstNumber VARCHAR(20) UNIQUE,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                pinCode VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_city (city),
                INDEX idx_state (state)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS po_outwards (
                pooutid INT AUTO_INCREMENT PRIMARY KEY,
                poout_date DATE,
                employeeid INT NOT NULL,
                typeofgoods VARCHAR(255),
                delivery_date DATE,
                status BOOLEAN,
                approval_status BOOLEAN,
                itemDetails JSON,
                remarks TEXT,
                vendorsid INT NULL,
                annexureid INT NULL,
                workordernumber INT NULL,
                FOREIGN KEY (employeeid) REFERENCES EmployeeRecords(employeeid) ON DELETE CASCADE,
                FOREIGN KEY (vendorsid) REFERENCES vendors(vendorsid) ON DELETE CASCADE,
                FOREIGN KEY (annexureid) REFERENCES annexure(annexureid) ON DELETE CASCADE,
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS dc (
                dcid INT AUTO_INCREMENT PRIMARY KEY,
                vendorsid INT,
                pooutid INT,
                place_to_supply VARCHAR(255),
                order_date DATE,
                dispatch_date DATE,
                driver_name VARCHAR(255),
                phone_number VARCHAR(15),
                vehicle_number VARCHAR(50),
                itemDetails JSON,
                dc_status BOOLEAN,
                FOREIGN KEY (vendorsid) REFERENCES vendors(vendorsid) ON DELETE CASCADE,
                FOREIGN KEY (pooutid) REFERENCES po_outwards(pooutid) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS inventory (
                meterialid INT,
                goodid INT,
                itemid INT,
                Available_Quantity INT,
                
                PRIMARY KEY (meterialid, goodid, itemid)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS inlog (
                meterialid INT,
                goodid INT,
                itemid INT,
                pooutid INT,
                PRIMARY KEY (meterialid, goodid, itemid, pooutid),
                FOREIGN KEY (meterialid, goodid, itemid) REFERENCES inventory(meterialid, goodid, itemid) ON DELETE CASCADE,
                FOREIGN KEY (pooutid) REFERENCES po_outwards(pooutid) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS outlog (
                meterialid INT,
                goodid INT,
                itemid INT,
                workordernumber INT,
                PRIMARY KEY (meterialid, goodid, itemid, workordernumber),
                FOREIGN KEY (meterialid, goodid, itemid) REFERENCES inventory(meterialid, goodid, itemid) ON DELETE CASCADE,
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber) ON DELETE CASCADE
            )
            """
        ]

        for query in table_queries:
            cursor.execute(query)

        connection.commit()
        connection.close()
        cursor.close()
        print("Database & Tables Initialized Successfully!")

        return True
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        return False