import json 

TYPE_NONE = 0
TYPE_PRODUCTS = 1
TYPE_LICENSES = 2

class DepotCataFile(object):

    def __init__(self, path):
        with open(path, 'r') as text:
            cata = json.load(text)
            
            self.type = TYPE_NONE
            self.data = {}
            self.byLicense = {}
            self.byProduct = {}
            self.licenseData = {}

            if 'm_products' in cata:
                self.type = self.type | TYPE_PRODUCTS
                self.data = cata['m_products']

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

            if 'm_licenses' in cata:
                self.type = self.type | TYPE_LICENSES
                self.licenseData = cata['m_licenses']
                self.byLicenseData = {}
            
                for licenseIndex in range(len(self.licenseData)):
                    self.byLicenseData[self.licenseData[licenseIndex]['m_id']] = licenseIndex

            if self.type == TYPE_NONE:
                print(cata.keys())
                exit(200)
            elif len(cata.keys()) > 1:
                print(cata.keys())
    
    def findLicenses(self, licenseId):
        if not licenseId in self.byLicense: return None

        l = list()
        for productIndex in self.byLicense[licenseId]:
            l.append(self.data[productIndex])
        return l

    def findProducts(self, productId):
        if not productId in self.byProduct: return None
        return self.data[self.byProduct[productId]]

    def findLicensesData(self, licenseId):
        if not licenseId in self.byLicenseData: return None
        return self.licenseData[self.byLicenseData[licenseId]]
