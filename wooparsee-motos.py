from requests_html import HTMLSession
import translators as ts
import csv
import re
import time



url = 'https://ecoxtrem.com/e-motos'

datasources =[]
datasourcesFormated =[]
imagesources =[]
stringa =''
resultFr =[]
resultFrN = []
resultEs =[]
my_dict =[]
Categories = "E-motos"
s = HTMLSession()
fullTs=''
def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def get_links(url):
    r = s.get(url)
    items = r.html.find('div.pro_outer_box.clearfix.home_default')
    links = []
    for item in items:
        links.append(item.find('a', first=True).attrs['href'])
    return links

def get_product_images(imagelink):
    r = s.get(imagelink)
    mainImages = r.html.find('div.images-container-0 picture img.pro_gallery_item')
    for item in mainImages:
        try:
           imagesources.append(item.attrs['data-src'])
        except IndexError:
           imagesources.append(item.attrs['srcset'])
    return imagesources

    


def get_productdata(link):
    r = s.get(link)
    title = r.html.find('h1', first=True).full_text
    title = ts.google(title, from_language = 'es', to_language='fr')
   
   
    try:
        price = r.html.find('div.current-price span')[0].full_text
    except IndexError:
        price = '0'
    try:
        regularprice = r.html.find('div.current-price span')[2].full_text
    except IndexError:
        regularprice = '0'
   
   
    desc = r.html.find('div.st_read_more_box p', first=True).full_text
    desc = ts.google(desc, from_language = 'es', to_language='fr')
    try:
        fulldesc = str(r.html.find('div.st_read_more_box')[1].html)
    except IndexError:
        fulldesc = str(r.html.find('div.st_read_more_box')[0].html)
    
    mainImages = r.html.find('div.images-container-0 picture img.pro_gallery_item')
    attributeNames = r.html.find('div.tab-pane-body section.product-features dt.name')
    attributeValues = r.html.find('div.tab-pane-body section.product-features dd.value')
    # my_dict[attributeNames]=attributeValues
    fulldesc = fulldesc.replace("\n", " ").strip()
    fulldesc = fulldesc.replace(";", " ")
    # sku = r.html.find('span.sku', first=True).full_text
    
    datasources =[]
    for item in mainImages:
        try:
           datasources.append(item.attrs['srcset'])
        except:
           datasources.append(item.attrs['data-src'])
        

    listToStr = ', '.join([str(elem) for elem in datasources])
    # listToStr = listToStr.replace("https://ecoxtrem.com", "http://localhost/easywpslider/wp-content/uploads/2021/06")
    stringa = listToStr.split("/", -1)
    stringa = stringa[4].split(",", -1)

    stringa = listToStr.replace( "/"+stringa[0], ".jpg")
    stringa = stringa.replace("https://ecoxtrem.com", "http://localhost/easywpslider/wp-content/uploads/2021/06")
    
   
    fulldesc = str(fulldesc)
    
    
  
    s1 = fulldesc[:len(fulldesc)//2]
    s2 = fulldesc[len(fulldesc)//2:]
    s1T = ts.google(s1, from_language = 'auto', to_language='fr', if_ignore_limit_of_length=True)
    s2T = ts.google(s2, from_language = 'auto', to_language='fr', if_ignore_limit_of_length=True) 
    Category = ts.google(Categories, from_language = 'auto', to_language='fr')
    fullTransDesc = s1T + s2T
    # fullTransDesc = fullTransDesc.replace('src = "', 'src ="')
    fullTransDesc = re.sub(r'src = "', r'src ="', fullTransDesc)

    resultEs = re.findall(r'src="(.*?)"', fulldesc)
    # resultFr = re.findall(r'src ="(.*?)"', fullTransDesc)
    resultFr = re.findall(r'src(.*?)https(.*?)"', fullTransDesc)

    # resultTags = re.findall(r'\s*(<.+?>)\s*', fullTransDesc)
    # toCorrect = ["", "", ""]

    
    for value in resultFr:
        str1 =value
        resultFrN.append(value)
   
    for fr,es in zip(resultFrN, resultEs):
    # Replace key character with value character in string
        fullTs = ''.join(fullTransDesc.replace(fr[1], es))
       
   

   
    fullTransDesc = fullTransDesc.replace("Div", "div")
    fullTransDesc = fullTransDesc.replace("la classe", "class")
    fullTransDesc = fullTransDesc.replace("col-MD-6", "col-md-6")
    fullTransDesc = fullTransDesc.replace("H2", "h2")
    fullTransDesc = fullTransDesc.replace("<P>", "<p>")
    fullTransDesc = fullTransDesc.replace("</ P>", "</p>")
    fullTransDesc = fullTransDesc.replace("</ p>", "</p>")
    fullTransDesc = fullTransDesc.replace("</ div>", "</div>")
    fullTransDesc = fullTransDesc.replace("H3", "h3")
    fullTransDesc = fullTransDesc.replace("</ h3>", "</h3>")
    fullTransDesc = fullTransDesc.replace("<UL >", "<ul>")
    fullTransDesc = fullTransDesc.replace("<Li>", "<li>")
    fullTransDesc = fullTransDesc.replace("<LI>", "<li>")
    fullTransDesc = fullTransDesc.replace("</ LI>", "</li>")
    fullTransDesc = fullTransDesc.replace("</ LI >", "<li>")
    fullTransDesc = fullTransDesc.replace("</ Li>", "</li>") 
    fullTransDesc = fullTransDesc.replace("< / Li>", "</li>")
    fullTransDesc = fullTransDesc.replace("<LI >", "<li>")
    fullTransDesc = fullTransDesc.replace("</ li>", "</li>")
    fullTransDesc = fullTransDesc.replace("</ ul>", "</ul>")
    fullTransDesc = fullTransDesc.replace("</ h2>", "</h2>")
    fullTransDesc = fullTransDesc.replace("classe", "class")
    fullTransDesc = fullTransDesc.replace("<UL>", "<ul>")
    fullTransDesc = fullTransDesc.replace("mas =", "class=")
    fullTransDesc = fullTransDesc.replace("<Li >", "<li>")
    fullTransDesc = fullTransDesc.replace("< Li>", "<li>") 
    fullTransDesc = fullTransDesc.replace("< / div>", "</div>")
    fullTransDesc = fullTransDesc.replace("</ div >", "</div>")
    fullTransDesc = fullTransDesc.replace("</ DIV>", "</div>")
    fullTransDesc = fullTransDesc.replace("< / p>", "</p>")


    # print(fullTransDesc)
    # print(fulldesc)
    

    # product = {}
    product = {'ID':'',
    'Type':'simple',
    'SKU':'',
    'Name':title.strip(),
    'Published':1,
    '"Is featured?"':0,
    '"Visibility in catalog"':'visible',
    '"Short description"':desc.strip(),
    'Description':fullTransDesc,
    '"Date sale price starts"':'',
    '"Date sale price ends"':'',
    '"Tax status"':'taxable',
    '"Tax class"':'',
    '"In stock?"':1,
    'Stock':'',
    '"Low stock amount"':'',
    '"Backorders allowed?"':0,
    '"Sold individually?"':0,
    '"Weight (kg)"':'',
    '"Length (cm)"':'',
    '"Width (cm)"':'',
    '"Height (cm)"':'',
    '"Allow customer reviews?"':1,
    '"Purchase note"':'',
    '"Sale price"':price.replace('€', '').strip(),
    '"Regular price"':regularprice.replace('€', '').strip(),
    'Categories':Category,
    'Tags':'',
    '"Shipping class"':'',
    'Images':stringa,
    '"Download limit"':'',
    '"Download expiry days"':'',
    'Parent':'',
    '"Grouped products"':'',
    'Upsells':'',
    'Cross-sells':'',
    '"External URL"':'',
    '"Button text"':'',
    'Position':0,
    'Attribute 1 name':'',
    'Attribute 1 value(s)':'',
    'Attribute 1 visible':'',
    'Attribute 1 global':'',
    
    'Attribute 2 name':'',
    'Attribute 2 value(s)':'',
    'Attribute 2 visible':'',
    'Attribute 2 global':'',
    
    'Attribute 3 name':'',
    'Attribute 3 value(s)':'',
    'Attribute 3 visible':'',
    'Attribute 3 global':'',
    
    'Attribute 4 name':'',
    'Attribute 4 value(s)':'',
    'Attribute 4 visible':'',
    'Attribute 4 global':'',
    
    'Attribute 5 name':'',
    'Attribute 5 value(s)':'',
    'Attribute 5 visible':'',
    'Attribute 5 global':'',
    
    'Attribute 6 name':'',
    'Attribute 6 value(s)':'',
    'Attribute 6 visible':'',
    'Attribute 6 global':'',
    
    'Attribute 7 name':'',
    'Attribute 7 value(s)':'',
    'Attribute 7 visible':'',
    'Attribute 7 global':'',

    'Attribute 8 name':'',
    'Attribute 8 value(s)':'',
    'Attribute 8 visible':'',
    'Attribute 8 global':'',
    
    'Attribute 9 name':'',
    'Attribute 9 value(s)':'',
    'Attribute 9 visible':'',
    'Attribute 9 global':'',
    
    'Attribute 10 name':'',
    'Attribute 10 value(s)':'',
    'Attribute 10 visible':'',
    'Attribute 10 global':'',
    
    'Attribute 11 name':'',
    'Attribute 11 value(s)':'',
    'Attribute 11 visible':'',
    'Attribute 11 global':'',
    
    'Attribute 12 name':'',
    'Attribute 12 value(s)':'',
    'Attribute 12 visible':'',
    'Attribute 12 global':'',
    
    'Attribute 13 name':'',
    'Attribute 13 value(s)':'',
    'Attribute 13 visible':'',
    'Attribute 13 global':'',
    
    'Attribute 14 name':'',
    'Attribute 14 value(s)':'',
    'Attribute 14 visible':'',
    'Attribute 14 global':'',
    
    'Attribute 15 name':'',
    'Attribute 15 value(s)':'',
    'Attribute 15 visible':'',
    'Attribute 15 global':'',
    
    'Attribute 16 name':'',
    'Attribute 16 value(s)':'',
    'Attribute 16 visible':'',
    'Attribute 16 global':'',
    
    'Attribute 17 name':'',
    'Attribute 17 value(s)':'',
    'Attribute 17 visible':'',
    'Attribute 17 global':'',
    
    }
    
      
        
    # for cle,val in zip(attributeNames, attributeValues): 
    for i in range(len(attributeNames)): 
        nameCell = 'Attribute '+str(i+1)+' name'
        valueCell = 'Attribute '+str(i+1)+' value(s)'
        visibleCell ='Attribute '+str(i+1)+' visible'
        publicCell = 'Attribute '+str(i+1)+' global'

        value = attributeNames[i]
        value = str(value.full_text)
        value = ts.google(value, from_language = 'es', to_language='fr')

        cellValue = attributeValues[i]
        cellValue =str(cellValue.full_text)
        cellValue = ts.google(cellValue, from_language = 'es', to_language='fr')

        product[nameCell]= value
        product[valueCell]= cellValue
        product[visibleCell]= ''
        product[publicCell]= ''
        
    # # print(descLinked)

    # # print(fulldesc.replace("\r", " "))
    print(product.keys())
    return product
    
    
results = []
links = get_links(url)

for link in links:
    results.append(get_productdata(link))
    time.sleep(1)


# with open('emoto.csv', 'w', encoding='utf8', newline='') as f:
#     fc = csv.DictWriter(f, fieldnames=results[0].keys(),)
#     fc.writeheader()
#     fc.writerows(results)

for item in links:
        imagelink = get_product_images(item)
        for image in imagelink:
            r = s.get(image)
            name = image.split("/")[3]
            with open("images/"+name+".jpg", "wb") as fp:
                fp.write(r.content)
        

