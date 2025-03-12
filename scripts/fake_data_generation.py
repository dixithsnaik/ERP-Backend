import mysql.connector
import random
from datetime import datetime, timedelta
import json
from faker import Faker
import string

# Database Credentials (Use environment variables)
DB_NAME = os.getenv("DB_NAME", "ERPDB")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "root")
HOST = os.getenv("DB_HOST", "localhost")

# Initialize Faker
fake = Faker()

# Connect to MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None

# Generate fake data for users table
def insert_users(cursor, num_records=30):
    user_ids = []
    roles = ['Admin', 'User']
    
    for i in range(num_records):
        username = fake.user_name()
        password = fake.password(length=12)
        role = 'Admin' if i < 5 else 'User'  # First 5 are admins, rest are users
        
        query = """
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
        """
        
        try:
            cursor.execute(query, (username, password, role))
            user_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting user: {error}")
    
    return user_ids

# Generate fake data for customer table
def insert_customers(cursor, num_records=30):
    customer_ids = []
    
    for i in range(num_records):
        customer_name = fake.company()
        email = fake.company_email()
        phone = fake.phone_number()[:15]
        address1 = fake.street_address()
        address2 = fake.secondary_address() if random.random() > 0.3 else None
        gst_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) if random.random() > 0.2 else None
        city = fake.city()
        state = fake.state()
        pin_code = fake.postcode()[:10]
        
        query = """
        INSERT INTO customer (customerName, emailAddress, phoneNumber, addressLine1, addressLine2, gstNumber, city, state, pinCode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (customer_name, email, phone, address1, address2, gst_number, city, state, pin_code))
            customer_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting customer: {error}")
    
    return customer_ids

# Generate fake data for rfq table
def insert_rfqs(cursor, customer_ids, num_records=30):
    rfq_ids = []
    request_via_options = ['Email', 'Phone', 'Website', 'In-person']
    
    for i in range(num_records):
        customer_id = random.choice(customer_ids)
        location = fake.city()
        country = fake.country()
        request_via = random.choice(request_via_options)
        request_ref_number = f"RFQ-{fake.uuid4()[:8].upper()}"
        type_of_goods = fake.bs()
        last_date = fake.date_between(start_date='-30d', end_date='+60d')
        contact_person = fake.name()
        contact_number = fake.phone_number()[:15]
        contact_email = fake.email()
        status = random.choice([True, False, None])
        
        query = """
        INSERT INTO rfq (customerid, location, country, requestVia, requestReferenceNumber, typeOfGoods, lastDateToSubmit, 
                        contactPerson, contactPersonNumber, contactPersonEmail, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (customer_id, location, country, request_via, request_ref_number, type_of_goods, 
                                 last_date, contact_person, contact_number, contact_email, status))
            rfq_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting RFQ: {error}")
    
    return rfq_ids

# Generate fake data for employee records
def insert_employees(cursor, num_records=30):
    employee_ids = []
    work_types = ['Full-time', 'Part-time', 'Contract', 'Seasonal', 'Intern']
    
    for i in range(num_records):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()[:20]
        permanent_work = random.choice(work_types) if random.random() > 0.3 else None
        temp_work = random.choice(work_types) if random.random() > 0.6 else None
        till_time = fake.date_between(start_date='+30d', end_date='+365d') if temp_work else None
        reason = fake.text(max_nb_chars=100) if random.random() > 0.7 else None
        contribution = fake.text(max_nb_chars=200) if random.random() > 0.5 else None
        address1 = fake.street_address()
        address2 = fake.secondary_address() if random.random() > 0.4 else None
        work_type = random.choice(work_types)
        city = fake.city()
        state = fake.state()
        pin_code = fake.postcode()[:20]
        join_date = fake.date_between(start_date='-1000d', end_date='-1d')
        
        query = """
        INSERT INTO EmployeeRecords (Name, EmailAddress, PhoneNumber, PermanentWorkType, TemporaryWorkType, TillTime, 
                                    ReasonForLayoff, ContributionToCompany, AddressLine1, AddressLine2, WorkType, 
                                    City, State, PinCode, DateOfJoining)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (name, email, phone, permanent_work, temp_work, till_time, reason, contribution, 
                                 address1, address2, work_type, city, state, pin_code, join_date))
            employee_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting employee: {error}")
    
    return employee_ids

# Generate fake data for vendors
def insert_vendors(cursor, num_records=30):
    vendor_ids = []
    
    for i in range(num_records):
        vendor_name = fake.company()
        email = fake.company_email()
        phone = fake.phone_number()[:15]
        address1 = fake.street_address()
        address2 = fake.secondary_address() if random.random() > 0.3 else None
        gst_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) if random.random() > 0.2 else None
        city = fake.city()
        state = fake.state()
        pin_code = fake.postcode()[:10]
        
        query = """
        INSERT INTO vendors (vendorName, emailAddress, phoneNumber, addressLine1, addressLine2, gstNumber, city, state, pinCode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (vendor_name, email, phone, address1, address2, gst_number, city, state, pin_code))
            vendor_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting vendor: {error}")
    
    return vendor_ids

# Generate fake data for quotation table
def insert_quotations(cursor, customer_ids, rfq_ids, user_ids, num_records=30):
    quotation_ids = []
    
    for i in range(min(num_records, len(rfq_ids))):
        customer_id = random.choice(customer_ids)
        rfq_id = rfq_ids[i]  # Each RFQ gets a quotation
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()[:15]
        terms = fake.paragraphs(nb=3)
        payment_terms = random.choice(["Net 30", "Net 60", "50% Advance", "100% Advance", "COD"])
        tax_duties = fake.paragraph()
        description = fake.text(max_nb_chars=200)
        delivery_date = fake.date_between(start_date='+30d', end_date='+180d')
        packaging = fake.paragraph()
        created_by = random.choice(user_ids)
        admin_approved = random.choice([True, False, None])
        
        # Create item details as JSON
        items = []
        for j in range(random.randint(1, 5)):
            item = {
                "itemId": j + 1,
                "description": fake.product_name(),
                "quantity": random.randint(1, 100),
                "unitPrice": round(random.uniform(10, 1000), 2),
                "totalPrice": 0
            }
            item["totalPrice"] = item["quantity"] * item["unitPrice"]
            items.append(item)
        
        # Create log as JSON
        logs = []
        for j in range(random.randint(1, 3)):
            log = {
                "timestamp": fake.date_time_this_year().isoformat(),
                "action": random.choice(["Created", "Updated", "Reviewed", "Approved", "Rejected"]),
                "userId": random.choice(user_ids),
                "notes": fake.sentence()
            }
            logs.append(log)
        
        item_details_json = json.dumps(items)
        log_json = json.dumps(logs)
        
        query = """
        INSERT INTO quotation (customerid, rfqid, name, emailAddress, phoneNumber, termsAndConditions, paymentTerms, 
                            taxAndDuties, briefDescription, deliveryDate, packageAndForwarding, createdBy, 
                            AdminApproved, log, itemDetails)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (customer_id, rfq_id, name, email, phone, str(terms), payment_terms, tax_duties, 
                                 description, delivery_date, packaging, created_by, admin_approved, log_json, 
                                 item_details_json))
            quotation_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting quotation: {error}")
    
    return quotation_ids

# Generate fake data for purchase_order table
def insert_purchase_orders(cursor, customer_ids, quotation_ids, employee_ids, num_records=30):
    purchase_order_ids = []
    status_options = ['Pending', 'Delivered', 'Shipped', 'Cancelled']
    
    for i in range(min(num_records, len(quotation_ids))):
        customer_id = random.choice(customer_ids)
        quotation_id = quotation_ids[i]  # Each quotation gets a purchase order
        employee_id = random.choice(employee_ids) if random.random() > 0.2 else None
        po_number = f"PO-{fake.uuid4()[:8].upper()}"
        customer_name = fake.company()
        po_date = fake.date_between(start_date='-60d', end_date='-1d')
        amount = round(random.uniform(1000, 100000), 2)
        
        # Create project engineers as JSON
        project_engineers = []
        for j in range(random.randint(1, 3)):
            engineer = {
                "id": random.choice(employee_ids),
                "name": fake.name(),
                "role": "Project Engineer"
            }
            project_engineers.append(engineer)
        
        # Create quality engineers as JSON
        quality_engineers = []
        for j in range(random.randint(1, 2)):
            engineer = {
                "id": random.choice(employee_ids),
                "name": fake.name(),
                "role": "Quality Engineer"
            }
            quality_engineers.append(engineer)
        
        delivery_date = fake.date_between(start_date='+30d', end_date='+180d')
        status = random.choice(status_options)
        remarks = fake.text(max_nb_chars=100) if random.random() > 0.5 else None
        contact_name = fake.name()
        contact_email = fake.email()
        contact_phone = fake.phone_number()[:20]
        project_name = fake.catch_phrase()
        
        # Create item details as JSON
        items = []
        for j in range(random.randint(1, 5)):
            item = {
                "itemId": j + 1,
                "description": fake.product_name(),
                "quantity": random.randint(1, 100),
                "unitPrice": round(random.uniform(10, 1000), 2),
                "totalPrice": 0
            }
            item["totalPrice"] = item["quantity"] * item["unitPrice"]
            items.append(item)
        
        work_order_date = fake.date_between(start_date='-30d', end_date='+30d')
        delivery_instructions = fake.paragraph() if random.random() > 0.3 else None
        critical_notes = fake.paragraph() if random.random() > 0.6 else None
        
        # Create logs as JSON
        logs = []
        for j in range(random.randint(1, 3)):
            log = {
                "timestamp": fake.date_time_this_year().isoformat(),
                "action": random.choice(["Created", "Updated", "Shipped", "Delivered", "Cancelled"]),
                "userId": random.choice(employee_ids),
                "notes": fake.sentence()
            }
            logs.append(log)
        
        project_engineers_json = json.dumps(project_engineers)
        quality_engineers_json = json.dumps(quality_engineers)
        item_details_json = json.dumps(items)
        logs_json = json.dumps(logs)
        
        query = """
        INSERT INTO purchase_order (customerid, quotationid, employeeid, po_number, customer, po_date, amount, project_engineers, 
                                quality_engineers, delivery_date, status, remarks, contact_person_name, contact_person_email, 
                                contact_person_phone, project_name, item_details, work_order_issue_date, instructions_for_delivery, 
                                critical_notes, logs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (customer_id, quotation_id, employee_id, po_number, customer_name, po_date, amount, 
                                 project_engineers_json, quality_engineers_json, delivery_date, status, remarks, 
                                 contact_name, contact_email, contact_phone, project_name, item_details_json, 
                                 work_order_date, delivery_instructions, critical_notes, logs_json))
            purchase_order_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting purchase order: {error}")
    
    return purchase_order_ids

# Generate fake data for BMO table
def insert_bmos(cursor, purchase_order_ids, num_records=15):
    bmo_ids = []
    
    # Select a subset of purchase orders to create BMOs
    selected_po_ids = random.sample(purchase_order_ids, min(num_records, len(purchase_order_ids)))
    
    for po_id in selected_po_ids:
        query = """
        INSERT INTO bmo (workordernumber)
        VALUES (%s)
        """
        
        try:
            cursor.execute(query, (po_id,))
            bmo_ids.append(po_id)
        except mysql.connector.Error as error:
            print(f"Error inserting BMO: {error}")
    
    return bmo_ids

# Generate fake data for annexure table
def insert_annexures(cursor, vendor_ids, num_records=30):
    annexure_ids = []
    annexure_types = ['Type A', 'Type B', 'Type C', 'Special', 'Standard']
    processes = ['Manufacturing', 'Assembly', 'Testing', 'Packaging', 'Quality Control']
    goods_types = ['Electronics', 'Mechanical', 'Chemical', 'Textile', 'Food']
    status_options = ['Approve', 'Reject', 'Pending']
    
    for i in range(num_records):
        annexure_number = f"ANX-{fake.uuid4()[:8].upper()}"
        annexure_type = random.choice(annexure_types)
        process = random.choice(processes)
        type_of_goods = random.choice(goods_types)
        vendor_id = random.choice(vendor_ids) if random.random() > 0.2 else None
        status = random.choice(status_options)
        
        # Create AOSN details as JSON
        aosn_details = []
        for j in range(random.randint(1, 3)):
            detail = {
                "id": j + 1,
                "name": fake.word(),
                "specification": fake.sentence(),
                "quantity": random.randint(1, 100),
                "remarks": fake.sentence() if random.random() > 0.5 else ""
            }
            aosn_details.append(detail)
        
        logs = fake.paragraphs(nb=2) if random.random() > 0.3 else None
        
        aosn_details_json = json.dumps(aosn_details)
        
        query = """
        INSERT INTO annexure (annexure_number, annexure_type, process, type_of_goods, vendorsid, status, aosn_details, logs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (annexure_number, annexure_type, process, type_of_goods, vendor_id, status, aosn_details_json, logs))
            annexure_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting annexure: {error}")
    
    return annexure_ids

# Generate fake data for production_slip table
def insert_production_slips(cursor, purchase_order_ids, num_records=20):
    production_slip_ids = []
    
    # Select a subset of purchase orders to create production slips
    selected_po_ids = random.sample(purchase_order_ids, min(num_records, len(purchase_order_ids)))
    
    for po_id in selected_po_ids:
        slip_number = f"SLIP-{fake.uuid4()[:8].upper()}"
        project_name = fake.catch_phrase()
        customer = fake.company()
        slip_date = fake.date_between(start_date='-30d', end_date='+30d')
        project_engineer = fake.name()
        quality_engineer = fake.name()
        store = random.choice(["Main Store", "Secondary Store", "External Warehouse"])
        account = random.choice(["Account A", "Account B", "Account C", "Special Account"])
        special_instruction = fake.paragraph() if random.random() > 0.4 else None
        logs = fake.paragraphs(nb=2) if random.random() > 0.3 else None
        
        query = """
        INSERT INTO production_slip (workordernumber, slip_number, project_name, customer, slip_date, project_engineer, 
                                   quality_engineer, store, account, special_instruction, logs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (po_id, slip_number, project_name, customer, slip_date, project_engineer, 
                                 quality_engineer, store, account, special_instruction, logs))
            production_slip_ids.append(po_id)
        except mysql.connector.Error as error:
            print(f"Error inserting production slip: {error}")
    
    return production_slip_ids

# Generate fake data for po_outwards table
def insert_po_outwards(cursor, employee_ids, vendor_ids, annexure_ids, purchase_order_ids, num_records=30):
    po_outward_ids = []
    good_types = ['Raw Material', 'Finished Goods', 'Semi-finished', 'Equipment', 'Packaging']
    
    for i in range(num_records):
        po_date = fake.date_between(start_date='-60d', end_date='-1d')
        employee_id = random.choice(employee_ids)
        type_of_goods = random.choice(good_types)
        delivery_date = fake.date_between(start_date='+1d', end_date='+60d')
        status = random.choice([True, False, None])
        approval_status = random.choice([True, False, None])
        
        # Create item details as JSON
        items = []
        for j in range(random.randint(1, 5)):
            item = {
                "itemId": j + 1,
                "description": fake.product_name(),
                "quantity": random.randint(1, 100),
                "unitPrice": round(random.uniform(10, 1000), 2),
                "totalPrice": 0
            }
            item["totalPrice"] = item["quantity"] * item["unitPrice"]
            items.append(item)
        
        remarks = fake.paragraph() if random.random() > 0.5 else None
        vendor_id = random.choice(vendor_ids) if random.random() > 0.3 else None
        annexure_id = random.choice(annexure_ids) if random.random() > 0.5 else None
        workorder_number = random.choice(purchase_order_ids) if random.random() > 0.5 else None
        
        item_details_json = json.dumps(items)
        
        query = """
        INSERT INTO po_outwards (poout_date, employeeid, typeofgoods, delivery_date, status, approval_status, 
                              itemDetails, remarks, vendorsid, annexureid, workordernumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (po_date, employee_id, type_of_goods, delivery_date, status, approval_status, 
                                 item_details_json, remarks, vendor_id, annexure_id, workorder_number))
            po_outward_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting PO outward: {error}")
    
    return po_outward_ids

# Generate fake data for DC table
def insert_dcs(cursor, vendor_ids, po_outward_ids, num_records=25):
    dc_ids = []
    
    # Select a subset of PO outwards to create DCs
    selected_po_outward_ids = random.sample(po_outward_ids, min(num_records, len(po_outward_ids)))
    
    for po_outward_id in selected_po_outward_ids:
        vendor_id = random.choice(vendor_ids)
        place_to_supply = fake.city()
        order_date = fake.date_between(start_date='-60d', end_date='-30d')
        dispatch_date = fake.date_between(start_date='-29d', end_date='-1d')
        driver_name = fake.name()
        phone_number = fake.phone_number()[:15]
        vehicle_number = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10, 99)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000, 9999)}"
        
        # Create item details as JSON
        items = []
        for j in range(random.randint(1, 5)):
            item = {
                "itemId": j + 1,
                "description": fake.product_name(),
                "quantity": random.randint(1, 100),
                "unitPrice": round(random.uniform(10, 1000), 2),
                "totalPrice": 0
            }
            item["totalPrice"] = item["quantity"] * item["unitPrice"]
            items.append(item)
        
        dc_status = random.choice([True, False, None])
        
        item_details_json = json.dumps(items)
        
        query = """
        INSERT INTO dc (vendorsid, pooutid, place_to_supply, order_date, dispatch_date, driver_name, 
                      phone_number, vehicle_number, itemDetails, dc_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (vendor_id, po_outward_id, place_to_supply, order_date, dispatch_date, driver_name, 
                                 phone_number, vehicle_number, item_details_json, dc_status))
            dc_ids.append(cursor.lastrowid)
        except mysql.connector.Error as error:
            print(f"Error inserting DC: {error}")
    
    return dc_ids

# Generate fake data for inventory, inlog, and outlog tables
def insert_inventory_and_logs(cursor, po_outward_ids, purchase_order_ids, num_records=30):
    # Create inventory items
    inventory_items = []
    
    for i in range(num_records):
        material_id = random.randint(1, 100)
        good_id = random.randint(1, 50)
        item_id = random.randint(1, 200)
        available_quantity = random.randint(10, 1000)
        
        # Add to list for later use
        inventory_items.append((material_id, good_id, item_id))
        
        query = """
        INSERT INTO inventory (meterialid, goodid, itemid, Available_Quantity)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (material_id, good_id, item_id, available_quantity))
        except mysql.connector.Error as error:
            print(f"Error inserting inventory: {error}")
    
    # Create inlogs for some inventory items
    for i in range(min(len(inventory_items), len(po_outward_ids))):
        material_id, good_id, item_id = inventory_items[i]
        po_outward_id = po_outward_ids[i]
        
        query = """
        INSERT INTO inlog (meterialid, goodid, itemid, pooutid)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (material_id, good_id, item_id, po_outward_id))
        except mysql.connector.Error as error:
            print(f"Error inserting inlog: {error}")
    
    # Create outlogs for some inventory items
    for i in range(min(len(inventory_items), len(purchase_order_ids))):
        material_id, good_id, item_id = inventory_items[i]
        workorder_number = purchase_order_ids[i]
        
        query = """
        INSERT INTO outlog (meterialid, goodid, itemid, workordernumber)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (material_id, good_id, item_id, workorder_number))
        except mysql.connector.Error as error:
            print(f"Error inserting outlog: {error}")

# Main function to run everything
def main():
    connection = connect_to_db()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Insert data into all tables
        print("Inserting users...")
        user_ids = insert_users(cursor)
        
        print("Inserting customers...")
        customer_ids = insert_customers(cursor)
        
        print("Inserting RFQs...")
        rfq_ids = insert_rfqs(cursor, customer_ids)
        
        print("Inserting employees...")
        employee_ids = insert_employees(cursor)
        
        print("Inserting vendors...")
        vendor_ids = insert_vendors(cursor)
        
        print("Inserting quotations...")
        quotation_ids = insert_quotations(cursor, customer_ids, rfq_ids, user_ids)
        
        print("Inserting purchase orders...")
        purchase_order_ids = insert_purchase_orders(cursor, customer_ids, quotation_ids, employee_ids)
        
        print("Inserting BMOs...")
        bmo_ids = insert_bmos(cursor, purchase_order_ids)
        
        print("Inserting annexures...")
        annexure_ids = insert_annexures(cursor, vendor_ids)
        
        print("Inserting production slips...")
        production_slip_ids = insert_production_slips(cursor, purchase_order_ids)
        
        print("Inserting PO outwards...")
        po_outward_ids = insert_po_outwards(cursor, employee_ids, vendor_ids, annexure_ids, purchase_order_ids)
        
        print("Inserting DCs...")
        dc_ids = insert_dcs(cursor, vendor_ids, po_outward_ids)
        
        print("Inserting inventory and logs...")
        insert_inventory_and_logs(cursor, po_outward_ids, purchase_order_ids)
        
        # Commit the changes
        connection.commit()
        print("Data insertion completed successfully.")
        
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if _name_ == "_main_":
    main()