from flask import Flask
import logging

# internal imports
from dataControllers import Customers
from dataModels.datbaseSetup import init_db
import logging
from controllers import greet, users, PurchaseOrdersIn, Quotations, Rfq, Vendors, Customer, company, PurchaseOrdersOut, Employees
from Utils import employeeName, vendorName

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

#greeting routes
app.add_url_rule('/hello', 'hello', greet.hello)
app.add_url_rule('/users', 'users', users.getUsers)

# PO routes
app.add_url_rule('/pendingpos', 'pendingpos', PurchaseOrdersIn.getPendingPOs, methods=['GET'])

# Quotations routes
app.add_url_rule('/quotations/unapproved', 'unapproved_quotations', Quotations.getUnapprovedQuotations, methods=['GET'])
app.add_url_rule('/quotations/all', 'all_quotations', Quotations.getAllQuotations, methods=['GET'])
app.add_url_rule('/quotations/pending-approval', 'pending_approval_quotations', Quotations.getPendingApprovalQuotations, methods=['GET'])
app.add_url_rule('/quotations/approved', 'approved_quotation', Quotations.approvedQuotation, methods=['GET'])
app.add_url_rule('/quotations/rejected', 'rejected_quotation', Quotations.rejectedQuotation, methods=['GET'])
app.add_url_rule('/quotations/approvalstatus', 'approval_status', Quotations.approvalStatus, methods=['POST'])
app.add_url_rule('/quotations/create', 'create_quotation', Quotations.createQuotation, methods=['POST'])
app.add_url_rule('/quotations/update', 'update_quotation', Quotations.updateQuotation, methods=['POST'])


# RFQ routes
app.add_url_rule('/rfq/create','createRfq',Rfq.createRfq, methods=["POST"])
app.add_url_rule('/rfq/all','fetchAllRfqs',Rfq.fetchAllRfqs, methods=["GET"])
app.add_url_rule('/rfq/pending','getPendingRfqs',Rfq.getPendingRfqs, methods=["GET"])

# Vendors routes
app.add_url_rule('/vendors/all', 'getVendors', Vendors.getVendors, methods=['GET'])
app.add_url_rule('/vendors/add', 'addVendor', Vendors.addVendors, methods=['POST'])
app.add_url_rule('/vendors/update', 'updateVendor', Vendors.updateVendor, methods=['POST'])

# Customer routes
app.add_url_rule('/customers/all', 'getCustomers', Customer.getCustomers, methods=['GET'])
app.add_url_rule('/customers/add', 'addCustomer', Customer.addCustomer, methods=['POST'])
app.add_url_rule('/customers/update', 'updateCustomer', Customer.updateCustomer, methods=['POST'])

# Company routes
app.add_url_rule('/company/details','companyDetails',company.getCompanyDetails, methods=["GET"])
app.add_url_rule('/company/update','updateCompanyDetails',company.updateCompanyDetails, methods=["POST"])

# Employees routes
app.add_url_rule('/employees/all', 'getEmployees', Employees.getEmployees, methods=['GET'])
app.add_url_rule('/employees/recruit', 'recruitEmployee', Employees.recruitEmployee, methods=['POST'])
app.add_url_rule('/employees/layoff', 'layoffEmployee', Employees.layoffEmployee, methods=['POST'])
app.add_url_rule('/employees/update-role', 'updateRoleEmployee', Employees.updateRoleEmployee, methods=['POST'])

if __name__ == '__main__':
    try:
        # Initialize the database
        logging.info("Initializing database...")
        res = init_db()
        if res:
            print("Database initialized successfully.")
        else:
            print("Database initialization failed.")
            logging.error("Database initialization failed.")
            exit(1)
        logging.info("Database initialized successfully.")
        
        app.run(debug=True, host='0.0.0.0', port=5000) 
    except Exception as e:
        logging.error(f"An error occurred during startup: {e}")
