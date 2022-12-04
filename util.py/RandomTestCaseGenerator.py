import random

size = int(input("HOW MANY LINES: "))
transactions = int(input("HOW MANY TRANSACTIONS: "))
items = int(input("HOW MANY Items: "))
filename = str(input("Filename: "))


file1 = open("../test/"+filename, "w") 
stringpossible = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V"]
itemsize = min(items,25)
stringlist = stringpossible[0:itemsize]

for i in range(size):
    transaction = random.randint(1,transactions)
    itemname = random.choice(stringlist)
    string = f"R {transaction} {itemname}\n"
    
    file1.write(string)
    
for i in range(transactions):
    string = f"C {i+1}\n"
    file1.write(string)

    