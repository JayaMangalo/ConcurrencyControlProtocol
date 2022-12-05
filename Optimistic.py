from OCCTransaction import Transaction
import time

class OCC:
    def __init__(self):
        self.transactions = []


    def validTest(self, TID) -> bool:
        '''
        If for all Ti with TS(Ti) < TS(Tj), either one of the following condition holds:
            - finishTS(Ti) < startTS(Tj)
            - startTS(Tj) < finishTS(Ti) < validationTS(Tj) and the set of data items written by Ti does not intersect with the set of data items read by Tj
        '''

        for i in self.transactions:
            if(i.id == TID.id): continue

            if(i.validationTS == None): continue

            if(i.validationTS < TID.validationTS):
                if(i.finishTS < TID.startTS): pass
                elif((TID.startTS < i.finishTS) and (i.finishTS < TID.validationTS)):
                    for item in i.writeArr:
                        if item in TID.readArr:
                            return False
                else:
                    return False
        return True
    
    def ReadItem(self, TID, Item):
        id = TID - 1
        #Jika transaksi belum dimulai
        if (self.transactions[id].startTS == None):
            time.sleep(0.1) #add delay
            self.transactions[id].startTS = time.time()
        
        print(f"R{TID}({Item})",end="; ")
        self.transactions[id].readArr.append(Item)

    def WriteItem(self, TID, Item):
        id = TID - 1
        #Jika transaksi belum dimulai
        if (self.transactions[id].startTS == None):
            time.sleep(0.1) #add delay
            self.transactions[id].startTS = time.time()
        
        print(f"W{TID}({Item})",end="; ")
        self.transactions[id].writeArr.append(Item)
    
    def Commit(self, TID):
        print(f"C{TID}",end="; ")
        id = TID - 1
        time.sleep(0.1) #add delay
        self.transactions[id].validationTS = time.time()

        # Validation Phase
        success = self.validTest(self.transactions[id])
        # Write Phase
        if (success):
            time.sleep(0.1) #add delay
            self.transactions[id].finishTS = time.time()
            print(f"T{TID} success",end="; ")
        else:
            print("Validation failed; ")
            print(f"T{TID} aborted",end="; ")
    
if __name__ == '__main__':
    total_transaction = int(input("Total Transaction : "))
    filename = str(input("Test file : "))

    file_path = "test/" + filename
    f = open(file_path, "r")

    occ = OCC()
    for i in range(total_transaction):
        Tx = Transaction(i)
        occ.transactions.append(Tx)

    for line in f:
        data = line.split()
        
        TID = int(data[1])
        if data[0] == 'R':
            ItemName = data[2]
            occ.ReadItem(TID,ItemName)
            
        elif data[0] == 'W':
            ItemName = data[2]
            occ.WriteItem(TID,ItemName)
            
        elif data[0] == 'C':
            occ.Commit(TID) 