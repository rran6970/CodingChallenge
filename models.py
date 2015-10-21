import re
import json

class Product(object):
    # a class represent a product loaded from productsFile
    def __init__(self, productName, productManufacturer, family, model, announcedDate):
        self.productName = productName
        self.productManufacturer = productManufacturer
        self.family = family
        self.model = model
        self.announcedDate = announcedDate
        
        # represent the lower case manufacturer and family if has a family
        self.productManufacturerLower = productManufacturer.lower()
      
        if family:
            self.familyLower = family.lower()
       
        # three regex from lower case: exact regex, enable trail, enable lead and trail
        modelLower = model.lower()
        modelEscape = re.escape(modelLower)
        modelEscape_nospace = re.escape(modelLower.replace(' ', ''))
        modelEscape_nodash = re.escape(modelLower.replace('-', ''))
        modelEscape_dashspace = re.escape(modelLower.replace('-', ' '))
        modelEscape_spacedash = re.escape(modelLower.replace(' ', '-'))

        regex = '\W(?:%s|%s|%s|%s|%s)\W' % (
            modelEscape, 
            modelEscape_nospace,
            modelEscape_nodash,
            modelEscape_dashspace,
            modelEscape_spacedash)

        self.regexExact = re.compile(regex)
        
        regex = '\W(?:%s|%s|%s|%s|%s)\D' % (
            modelEscape, 
            modelEscape_nospace,
            modelEscape_nodash,
            modelEscape_dashspace,
            modelEscape_spacedash)
        
        self.regexTrail = re.compile(regex)

        regex = '\D(?:%s|%s|%s|%s|%s)\D' % (
            modelEscape, 
            modelEscape_nospace,
            modelEscape_nodash,
            modelEscape_dashspace,
            modelEscape_spacedash)

        self.regexLeadTrail = re.compile(regex)

    def __str__(self):
        
        proDict = {'product_name' : self.productName, 
                   'productManufacturer' : self.productManufacturer, 
                   'model'        : self.model, 
                   'announced-date': self.announcedDate}
    
        if self.family:
            proDict['family'] = self.family

        return json.dumps(proDict)

class Listing(object):
    # a class represent a listing loaded from listingsFile
    def __init__(self, title, manufacturer, currency, price):
        self.title = title
        self.manufacturer = manufacturer
        self.currency = currency
        self.price = price

        self.titleLower = title.lower()
        self.titleLower_nodash = self.titleLower.replace('-', '')
        self.manufacturerLower = manufacturer.lower()

    def __str__(self):
        return json.dumps({'title'       : self.title, 
                           'manufacturer': self.manufacturer, 
                           'currency'    : self.currency, 
                           'price'       : self.price})

    def listDict(self):
        return {'title'        : self.title,
                'manufacturer' : self.manufacturer,
                'currency'     : self.currency,
                'price'        : self.price}
