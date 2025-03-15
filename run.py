from flask import Flask
import logging

# internal imports
from dataModels.datbaseSetup import init_db
import logging
from controllers import greet, users, PurchaseOrdersIn, Quotations, Rfq, Vendors, Customer, company, annexure

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

#greeting routes
app.add_url_rule('/hello', 'hello', greet.hello)
app.add_url_rule('/users', 'users', users.getUsers)

# PO Inwards routes
app.add_url_rule('/poInwards/pendingpos', 'pendingpos', PurchaseOrdersIn.getPendingPOs, methods=['GET'])
app.add_url_rule('/poInwards/fetchPo', 'fetchPo', PurchaseOrdersIn.fetchPo, methods=['GET'])
app.add_url_rule('/poInwards/prodcutionSlip/fetch', 'fetchProductionSlip', PurchaseOrdersIn.fetchProductionSlip, methods=['GET'])
app.add_url_rule('/poInwards/fetchWO', 'fetchWO', PurchaseOrdersIn.fetchWO, methods=['GET'])
app.add_url_rule('/poInwards/create', 'createPO', PurchaseOrdersIn.createPO, methods=['POST'])
app.add_url_rule('/poInwards/updatePO', 'updatePO', PurchaseOrdersIn.updatePO, methods=['POST'])
app.add_url_rule('/poInwards/prodcutionSlip/create', 'createProductionSlip', PurchaseOrdersIn.createProductionSlip, methods=['POST'])
app.add_url_rule('/poInwards/prodcutionSlip/update', 'updateProductionSlip', PurchaseOrdersIn.updateProductionSlip, methods=['POST'])

# Customer Acceptance routes
app.add_url_rule('/poInwards/customerAcceptance/fetchALL', 'fetchCustomerAcceptance', PurchaseOrdersIn.fetchCustomerAcceptance, methods=['GET'])
app.add_url_rule('/poInwards/customerAcceptance/update', 'updateCustomerAcceptance', PurchaseOrdersIn.updateCustomerAcceptance, methods=['POST'])


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

# annexure routes
app.add_url_rule('/annexure/create', 'createAnnexure', annexure.createAnnexure, methods=['POST'])
app.add_url_rule('/annexure/fetchAll/<employeeId>/<workOrderNumber>', 'fetchAllAnnexures', annexure.fetchAllAnneuxres, methods=['GET'])
app.add_url_rule('/annexure/fetchManagerAnnexures/<workOrderNumber>', 'fetchManagerAnnexures', annexure.fetchManagerAnnexures, methods=['GET'])
app.add_url_rule('/annexure/managerApprovalStatus', 'managerApprovalStatus', annexure.managerApprovalStatus, methods=['POST'])
app.add_url_rule('/annexure/fetchAdminAnnexures', 'fetchAdminAnnexures', annexure.fetchAdminAnnexures, methods=['GET'])
app.add_url_rule('/annexure/adminApprovalStatus', 'adminApprovalStatus', annexure.adminApprovalStatus, methods=['POST'])
app.add_url_rule('/annexure/fetchApprovedAnneuxres', 'fetchApprovedAnneuxres', annexure.fetchApprovedAnneuxres, methods=['GET'])


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
