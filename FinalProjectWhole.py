import csv
import os
from datetime import datetime

# 3 lists created to store CSV info
MainList = []
PriceList = []
ServList = []

# CSV files read and lists appended
with open('ManufacturerList.csv', 'r') as csvfile1:
    MainList_reader = csv.reader(csvfile1)
    for i in MainList_reader:
        MainList.append(i)

with open('PriceList.csv', 'r') as csvfile2:
    PriceList_reader = csv.reader(csvfile2)
    for i in PriceList_reader:
        PriceList.append(i)

with open('ServiceDatesList.csv', 'r') as csvfile3:
    ServList_reader = csv.reader(csvfile3)
    for i in ServList_reader:
        ServList.append(i)

# 1.A) Full Inventory CSV
# Combining CSVs
Full_List = MainList
for i in Full_List:
    for y in PriceList:
        if i[0] == y[0]:
            i.insert(3, y[1])
    for z in ServList:
        if i[0] == z[0]:
            i.insert(4, z[1])

# Sorting by Brand
MainList.sort(key=lambda x: x[1])

with open('FullInventory.csv', 'w') as f:
    for row in MainList:
        MainList = csv.writer(f)
        MainList.writerow(row)

# 1.B)Item Type List CSVs
PartList = Full_List
LaptopList = []
PhoneList = []
TowerList = []

# Laptop Inventory CSV write
for i in PartList:
    if i[2] == 'laptop':
        LaptopList.append(i)
LaptopList.sort(key=lambda x: x[0])
with open('LaptopInventory.csv', "w") as f:
    for row in LaptopList:
        LaptopList = csv.writer(f)
        LaptopList.writerow(row)

# Phone Inventory CSV write
for i in PartList:
    if i[2] == 'phone':
        PhoneList.append(i)
PhoneList.sort(key=lambda x: x[0])
with open('PhoneInventory.csv', "w") as f:
    for row in PhoneList:
        PhoneList = csv.writer(f)
        PhoneList.writerow(row)

# Tower Inventory CSV write
for i in PartList:
    if i[2] == 'tower':
        TowerList.append(i)
TowerList.sort(key=lambda x: x[0])
with open('TowerInventory.csv', "w") as f:
    for row in TowerList:
        TowerList = csv.writer(f)
        TowerList.writerow(row)

# 1.C) Past Service Date CSV


# datetime today's date
today = datetime.today()

# Items dictionary created using ID as the main key
# Takes rows from input csv files and assigns rows as values in sub keys

items = {}
files = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']
for file in files:
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            item_id = line[0]
            if file == files[0]:
                items[item_id] = {}
                brand = line[1]
                type = line[2]
                status = line[3]
                items[item_id]['Brand'] = brand
                items[item_id]['Type'] = type
                items[item_id]['Status'] = status
            elif file == files[1]:
                price = line[1]
                items[item_id]['Price'] = price
            elif file == files[2]:
                service_date = line[1]
                items[item_id]['Service Date'] = service_date


# Class method will be used to create the Past Service Date CSV
# Will also create a CSV with items that are not past their service date to create a query dictionary
class CSVOutput:
    # Creates list of items needed to write the files
    def __init__(self, item_list):
        self.item_list = item_list

    # Creates Past Service Date CSV, keeps only items past their Service Date
    # Sorts CSV in descending order of date after converting Service Date into datetime
    def past_service(self):
        list = self.item_list
        x = sorted(list.keys(), key=lambda x: datetime.strptime(list[x]['Service Date'], "%m/%d/%Y").date(),
                   reverse=True)
        with open('PastServiceDateInventory.csv', 'w') as file:
            for item in x:
                ID = item
                # Values of subkeys assigned to a list and writen by column
                brand = list[item]['Brand']
                type = list[item]['Type']
                price = list[item]['Price']
                service_date = list[item]['Service Date']
                status = list[item]['Status']
                today = datetime.now().date()
                service_date = datetime.strptime(service_date, "%m/%d/%Y").date()
                past_service_date = service_date < today
                if past_service_date:
                    file.write('{},{},{},{},{},{}\n'.format(ID, brand, type, price, service_date, status))

    def qeury_part(self):
        list = self.item_list
        # Creates Query part CSV, keeps only items before their Service Date
        # Converts Service Date into datetime
        y = sorted(list.keys(), key=lambda x: datetime.strptime(list[x]['Service Date'], "%m/%d/%Y").date(),
                   reverse=True)
        with open('QueryPart.csv', "w") as part:
            for item in y:
                ID = item
                # Values of subkeys assigned to a list and writen by column
                brand = list[item]['Brand']
                type = list[item]['Type']
                price = list[item]['Price']
                service_date = list[item]['Service Date']
                status = list[item]['Status']
                today = datetime.now().date()
                service_date = datetime.strptime(service_date, "%m/%d/%Y").date()
                before_service_date = service_date > today
                if before_service_date:
                    part.write('{},{},{},{},{},{}\n'.format(ID, brand, type, price, service_date, status))


if __name__ == '__main__':
    PastService = CSVOutput(items)
    PastService.past_service()
    PastService.qeury_part()

# 1.D) Damaged Inventory CSV
dmglist = []

for i in Full_List:
    if i[5] == 'damaged':
        dmglist.append(i)
dmglist.sort(key=lambda x: x[3])
with open('DamagedInventory.csv', "w") as f:
    for row in dmglist:
        dmglist = csv.writer(f)
        dmglist.writerow(row)

# 2.A) Query
# Create a query dictionary

# Creates a list where items are not past service date
with open('QueryPart.csv') as a:
    reader = csv.reader(a)
    querypart_list = list(reader)



# Remove items that are damaged from Query List
for i in querypart_list:
    if i[5] == 'damaged':
        querypart_list.remove(i)

# Header is added to act as key for Query Dictionary, will be placed in top row by csv
header = ['ID', 'Brand', 'Type', "Price", "Service Date", "Status"]
with open('FullQuery.csv', "w") as g:
    writer = csv.writer(g)
    writer.writerow(i for i in header)
    for row in querypart_list:
        writer.writerow(row)

columns = []
with open('FullQuery.csv') as q:
    reader = csv.reader(q)
    for row in reader:
        if columns:
            for i, value in enumerate(row):
                columns[i].append(value)
        else:
            columns = [[value] for value in row]
QueryDict = {c[0]: c[1:] for c in columns}

os.remove("QueryPart.csv")
os.remove("FullQuery.csv")

while True:
    q = input("Type to search for item or press q to quit")
    # input of q exits program
    if (q == "q"):
        break
    # creates 2 values to store Brand and Type
    brand = ""
    type = ""
    # If Brand or Type is in the query, assign to brand and type
    for x in QueryDict["Brand"]:
        if x in q:
            brand = x
    for x in QueryDict["Type"]:
        if x in q:
            type = x
    # If either value is not in query inform user of so
    if (brand == "" or type == ""):
        print("No such item in inventory")
    else:
        # List created to store values
        ItemList = ["", "", "", ""]
        # Loop in Query Dictionary
        for x in range(len(QueryDict["ID"])):
            # Check Brand and Type in Query Dictionary
            if (QueryDict["Brand"][x] == brand and QueryDict['Type'][x] == type):
                # Check if Item is the most expensive in Query Dictionary
                if (ItemList[3] < QueryDict["Price"][x]):
                    # Store Item Details into the Item List
                    ItemList[0] = QueryDict["ID"][x]
                    ItemList[1] = QueryDict["Brand"][x]
                    ItemList[2] = QueryDict["Type"][x]
                    ItemList[3] = QueryDict["Price"][x]
        # Print the item(s)
        print("Your item is: " + str(ItemList[0]) + " " + str(ItemList[1]) + " " + str(ItemList[2]) + " " + str(
            ItemList[3]))
        # List created to store other items to consider
        Consider = []
        # Loop in Query Dictionary
        for y in range(len(QueryDict['ID'])):
            # Check for items of the same Type and different Brand
            if (QueryDict["Type"] == type and QueryDict["Brand"] != type):
                Consider.append(QueryDict["ID"][i], QueryDict["Brand"][i], QueryDict["Type"][i], QueryDict["Price"][i])
        # Check if there are any items added to the Consider List
        if len(Consider) != 0:
            print("You may, also, consider ")
            # Loop in Consider list
            for z in range(len(Consider)):
                # Print all items to consider
                print(str(Consider[i][0]) + " " + Consider[i][1] + " " + Consider[i][2] + " " + str(Consider[i][3]))
