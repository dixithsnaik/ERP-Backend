from flask import Flask
import logging

# internal imports
from dataModels.datbaseSetup import init_db
from controllers import greet, users, PurchaseOrdersIn, Quotations, Rfq, company

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

# Company routes
app.add_url_rule('/company/details','companyDetails',company.getCompanyDetails, methods=["GET"])
app.add_url_rule('/company/update','updateCompanyDetails',company.updateCompanyDetails, methods=["POST"])


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
