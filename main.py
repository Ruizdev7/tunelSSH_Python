from db import SecureConection

test = SecureConection()
test.openSSHTunnel()
test.mysqlConnect()
test.getCatalog()
test.mysqldisconnect()
test.closeSSHTunnel()