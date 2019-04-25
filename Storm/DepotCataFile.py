import json 

class DepotCataFile(object):

    def __init__(self, path):
        with open(path, 'r') as text:
            self.data = json.load(text)["m_products"]
            self.byLicense = {}
            self.byProduct = {}

            for productIndex in range(len(self.data)):
                productId = -1
                licenseIds = []
                product = self.data[productIndex]
                try:
                    productId = product['m_productId']
                    licenseIds = product['m_licenses']
                except: continue
                
                self.byProduct[productId] = productIndex
                for licenseId in licenseIds:
                    if not licenseId in self.byLicense:
                        self.byLicense[licenseId] = []
                    self.byLicense[licenseId].append(productIndex)
    
    def findLicenses(self, licenseId):
        if not licenseId in self.byLicense: return None

        l = list()
        for productIndex in self.byLicense[licenseId]:
            l.append(self.data[productIndex])
        return l

    def findProducts(self, productId):
        if not productId in self.byProduct: return None
        return self.data[self.byProduct[productId]]
