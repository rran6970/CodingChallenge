import json

from models import Product
from models import Listing

def processProducts(productsFile):
    #process productsFile and load every line into a class Product
    results = []
    with open(productsFile, 'r') as products:

        line = 0

        for product in products:
            line += 1

            jsonResult = json.loads(product)

            if 'product_name' not in jsonResult:
                raise KeyError('Invalid product on line %d, missing product_name.' % line)
            if 'manufacturer' not in jsonResult:
                raise KeyError('Invalid product on line %d, missing manufacturer.' % line)
            if 'model' not in jsonResult:
                raise KeyError('Invalid product on line %d, missing model.' % line)
            if 'announced-date' not in jsonResult:
                raise KeyError('Invalid product on line %d, missing announced-date.' % line)

            productName = jsonResult['product_name']
            productManufacturer = jsonResult['manufacturer']
            model = jsonResult['model']
            announcedDate = jsonResult['announced-date']
            family = jsonResult.get('family', None) 

            if 'olympus' == productManufacturer.lower() and model[:4] == 'PEN ':
                family = 'PEN'
                model = model[4:]

            if 'panasonic' == productManufacturer.lower() and model[:4] == 'DMC-':
                family = 'DMC'
                model = model[4:]

            if 'sony' == productManufacturer.lower() and model[:5] == 'DSLR-':
                model = model[5:]

            results.append(Product(productName, productManufacturer, family, model, announcedDate))

    return results

def processListings(listingsFile):
    # process listingsFile and load every line into a class Listing
    
    result = []
    with open(listingsFile, 'r') as listings:

        line = 0

        for listing in listings:
            line += 1

            jsonResult = json.loads(listing)

            if 'title' not in jsonResult:
                raise KeyError('Invalid listing on line %d, missing title.' % line)
            if 'manufacturer' not in jsonResult:
                raise KeyError('Invalid listing on line %d, missing manufacturer.' % line)
            if 'currency' not in jsonResult:
                raise KeyError('Invalid listing on line %d, missing currency.' % line)
            if 'price' not in jsonResult:
                raise KeyError('Invalid listing on line %d, missing price.' % line)

            result.append(Listing(jsonResult['title'], 
                                  jsonResult['manufacturer'], 
                                  jsonResult['currency'], 
                                  jsonResult['price']))
    return result

def matchProducts(listing, products):
    # match a listing in all products
    matchProducts = []

    title = ' %s ' % listing.titleLower
    title_nodash = ' %s ' % listing.titleLower_nodash
  
    withFamily = []
    withoutFamily = []

    for product in products:
        manufacturer = product.productManufacturerLower

        if manufacturer in title or manufacturer in listing.listManufacturerLower:
            if product.regexExact.search(title) \
                or product.regexExact.search(title_nodash):

                if product.family and product.familyLower in title:
                    withFamily.append(product)
                else:
                    withoutFamily.append(product)

    if len(withFamily) > 0:
        return withFamily 

    if len(withoutFamily) > 0:
        return withoutFamily

    for product in products:
        manufacturer = product.productManufacturerLower

        if manufacturer in title or manufacturer in listing.listManufacturerLower:
            if product.regexTrail.search(title) \
                or product.regexTrail.search(title_nodash):

                if product.family and product.familyLower in title:
                    withFamily.append(product)
                else:
                    withoutFamily.append(product)

    if len(withFamily) > 0:
        return withFamily 

    if len(withoutFamily) > 0:
        return withoutFamily

    for product in products:
        manufacturer = product.productManufacturerLower

        if manufacturer in title or manufacturer in listing.listManufacturerLower:
            if product.regexLeadTrail.search(title) \
                or product.regexLeadTrail.search(title_nodash):

                if product.family and product.familyLower in title:
                    withFamily.append(product)
                else:
                    withoutFamily.append(product)

    if len(withFamily) > 0:
        return withFamily 

    if len(withoutFamily) > 0:
        return withoutFamily

    if ' for ' in title:
        for product in products:

            if not product.family:
                continue

            manufacturer = product.productManufacturerLower
            family = product.familyLower
            if family in title and manufacturer in title:
                matchProducts.append(product)

    return matchProducts
   
def matching(products, listings):
    matchResults = {}

    for listing in listings:
        matchedProducts = matchProducts(listing, products)

        for product in matchedProducts:
            name = product.productName

            if name not in matchResults:
                matchResults[name] = []

            matchResults[name].append(listing.listDict())

    return matchResults
#==================================Main Program Start=====================================================
def main():
    # the main program just do with writing
    productsFile = 'products.txt'
    listingsFile = 'listings.txt'
    resultsFile = 'results.txt'

    products = processProducts(productsFile)
    listings = processListings(listingsFile)

    matchResults = matching(products, listings)

    with open(resultsFile, 'w') as results:
        for product in products:
            matchedListings = matchResults.get(product.productName, [])
            
            jsonDict = {'product_name': product.productName,
                        'listings': matchedListings}
            jsonResults = json.dumps(jsonDict)
            
            resultsData = ''
            for product_name, listings in jsonDict.iteritems():
                resultsData = resultsData + '{"product_name":' + product_name + '", "listings":' + json.dumps(listings) +'}\n'

            results.write('%s' % resultsData)

if __name__ == '__main__':
    main()
#==================================Main Program End=====================================================
