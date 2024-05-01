import sys
sys.path.append("..")
from DAO.productsDAO import productsDAOImpl
import json
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
        self.productsDAO.addProduct(productname, price)
    def deleteProductById(self, productid):
        return self.productsDAO.deleteProductById(productid)