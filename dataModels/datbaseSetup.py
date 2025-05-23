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
PORT = os.getenv("DB_PORT", 3306)

# Create Database if it doesn't exist
def create_database():
    try:
        print("Creating database...")
        connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, port=PORT)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
        connection.close()
        print(f"Database '{DB_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Initialize Database Tables
def init_db():
    # create_database()
    try:
        connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DB_NAME , port=PORT)
        cursor = connection.cursor()
        print("Initializing database tables...")
        table_queries = [
             """
            CREATE TABLE IF NOT EXISTS companyDetails (
                company_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                email_address VARCHAR(255) UNIQUE NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                address_line1 VARCHAR(255) NOT NULL,
                address_line2 VARCHAR(255),
                gst_number VARCHAR(50) UNIQUE NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                pin_code VARCHAR(20) NOT NULL,
                gst_registration_number VARCHAR(50) UNIQUE NOT NULL,
                gst_registration_type VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """,
            
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
                DateOfJoining DATE, 
                DateOfLeaving DATE DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

            """,
            """
            CREATE TABLE IF NOT EXISTS purchase_order (
                workordernumber INT AUTO_INCREMENT PRIMARY KEY,
                customerid INT NOT NULL,
                quotationid INT,
                employeeid INT,
                po_number VARCHAR(50) UNIQUE NOT NULL,
                customer VARCHAR(255) NOT NULL,
                po_date DATE NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                project_engineers JSON,
                quality_engineers JSON,
                delivery_date DATE NOT NULL,
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
            CREATE TABLE IF NOT EXISTS production_slip (
                slip_number INT AUTO_INCREMENT PRIMARY KEY,
                workordernumber INT NOT NULL,
                project_name VARCHAR(255),
                customer VARCHAR(255),
                slip_date DATE,
                project_engineer VARCHAR(255),
                quality_engineer VARCHAR(255),
                store VARCHAR(255),
                account VARCHAR(255),
                customer_acceptance_status BOOLEAN DEFAULT NULL,
                reason_for_rejection TEXT,
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
            CREATE TABLE IF NOT EXISTS annexure (
                annexureid INT AUTO_INCREMENT PRIMARY KEY,
                annexure_type VARCHAR(50),
                employeeid INT,
                workordernumber INT,
                vendorsid INT,
                statusManagerId INT NULL DEFAULT NULL,
                statusManager BOOLEAN NULL DEFAULT NULL,
                statusAdminId INT NULL DEFAULT NULL,
                statusAdmin BOOLEAN NULL DEFAULT NULL,
                item_details JSON, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (employeeid) REFERENCES EmployeeRecords(employeeid) ON DELETE SET NULL,
                FOREIGN KEY (vendorsid) REFERENCES vendors(vendorsid) ON DELETE CASCADE,
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber) ON DELETE CASCADE,
                FOREIGN KEY (statusManagerId) REFERENCES EmployeeRecords(employeeid) ON DELETE SET NULL,
                FOREIGN KEY (statusAdminId) REFERENCES EmployeeRecords(employeeid) ON DELETE SET NULL
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            ,
            """
            CREATE TABLE IF NOT EXISTS po_outwards (
                pooutid INT AUTO_INCREMENT PRIMARY KEY,
                poout_date DATE,
                employeeid INT NOT NULL,
                typeofgoods VARCHAR(255),
                delivery_date DATE,
                status BOOLEAN,
                approval_status BOOLEAN NOT NULL DEFAULT FALSE,
                itemDetails JSON,
                remarks TEXT,
                vendorsid INT NULL,
                annexureid INT NULL,
                workordernumber INT NULL,
                jobwork BOOLEAN NOT NULL DEFAULT FALSE,
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
            CREATE TABLE IF NOT EXISTS meterial (
                meterialid INT AUTO_INCREMENT PRIMARY KEY,
                meterial_name VARCHAR(255) NOT NULL UNIQUE,
                meterial_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS goods (
                goodid INT AUTO_INCREMENT PRIMARY KEY,
                good_name VARCHAR(255) NOT NULL UNIQUE,
                good_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS items (
                itemid INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(255) NOT NULL UNIQUE,
                item_description TEXT,
                hsncode VARCHAR(50),
                unit VARCHAR(50) NOT NULL Check(unit <> ""),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS inventory (
                meterialid INT,
                goodid INT,
                itemid INT,
                quantity INT CHECK (quantity >= 0),
                average_price DECIMAL(15,2),
                PRIMARY KEY (meterialid, goodid, itemid),
                FOREIGN KEY (meterialid) REFERENCES meterial(meterialid),
                FOREIGN KEY (goodid) REFERENCES goods(goodid),
                FOREIGN KEY (itemid) REFERENCES items(itemid)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS inlog (
                meterialid INT,
                goodid INT,
                itemid INT,
                pooutid INT,
                quantity INT CHECK (quantity >= 0),
                price DECIMAL(15,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (meterialid, goodid, itemid, pooutid),
                FOREIGN KEY (pooutid) REFERENCES po_outwards(pooutid)
            );    
            """,
            """
            CREATE TABLE IF NOT EXISTS outlog (
                meterialid INT,
                goodid INT,
                itemid INT,
                quantity INT CHECK (quantity >= 0),
                workordernumber INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (meterialid, goodid, itemid, workordernumber),
                FOREIGN KEY (workordernumber) REFERENCES purchase_order(workordernumber)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS bom(
                bomid INT AUTO_INCREMENT PRIMARY KEY,
                workordernumber INT,
                gcp_bucket VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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