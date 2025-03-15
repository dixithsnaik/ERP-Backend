from Utils import employeeName, vendorName, Customers

def hello():
    print(vendorName.getVendorName( "22"))
    print(employeeName.getEmployeeName("2"))
    print(Customers.getCustomerName("2"))
    return "Hello World"