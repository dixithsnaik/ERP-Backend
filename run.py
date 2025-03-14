from flask import Flask
import controllers.users
from dataModels.datbaseSetup import init_db
import logging
from controllers import greet, users, PurchaseOrdersIn, Quotations


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

#greeting routes
app.add_url_rule('/hello', 'hello', greet.hello)
app.add_url_rule('/users', 'users', users.getUsers)

# PO routes
app.add_url_rule('/pendingpos', 'pendingpos', controllers.PurchaseOrdersIn.getPendingPOs, methods=['GET'])

# Quotations routes
app.add_url_rule('/quotations/unapproved', 'unapproved_quotations', controllers.Quotations.getUnapprovedQuotations, methods=['GET'])
app.add_url_rule('/quotations/all', 'all_quotations', controllers.Quotations.getAllQuotations, methods=['GET'])
app.add_url_rule('/quotations/pending-approval', 'pending_approval_quotations', controllers.Quotations.getPendingApprovalQuotations, methods=['GET'])
app.add_url_rule('/quotations/approved', 'approved_quotation', controllers.Quotations.approvedQuotation, methods=['GET'])
app.add_url_rule('/quotations/rejected', 'rejected_quotation', controllers.Quotations.rejectedQuotation, methods=['GET'])
app.add_url_rule('/quotations/approvalstatus', 'approval_status', controllers.Quotations.approvalStatus, methods=['POST'])
app.add_url_rule('/quotations/create', 'create_quotation', controllers.Quotations.createQuotation, methods=['POST'])
app.add_url_rule('/quotations/update', 'update_quotation', controllers.Quotations.updateQuotation, methods=['POST'])



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
