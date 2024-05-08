import sys
sys.path.append("..")
from DAO.productsDAO import productsDAOImpl
class productsServiceImpl:
    def __init__(self):
        self.productsDAO = productsDAOImpl()
    def getProductNameById(self, productid):
        product = self.productsDAO.getProductById(productid)
        if len(product) == 0:
            return None
        return product[0]["productname"]
    def getAllProducts(self):
        all = self.productsDAO.getAllProducts()
        return all
    def addProduct(self, productname, price):
        res = self.productsDAO.addProduct(productname, price)
        return res == 1
    def deleteProductById(self, productid):
        res = self.productsDAO.deleteProductById(productid)
        return res == 1
    def updateProduct(self, productid, productname, price):
        res = self.productsDAO.updateProduct(productid, productname, price)
        return res == 1