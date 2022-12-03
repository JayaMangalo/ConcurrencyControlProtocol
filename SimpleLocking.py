class SimpleLocking:
    def __init__(self):
        self.LockTable = []
        self.Queue = []
        pass
    
    def isItemLocked(self,ItemName):
        for Locks in self.LockTable:
            if ItemName in Locks[1]:
                return True, Locks[0]
        return False,False
                
    def isTransanctionQueued(self,Transaction):
        for Queueitem in self.Queue:
            if Transaction in Queueitem[2]:
                return True
        return False
                
    def TryQueue(self,TLocker):
        for Queueitem in self.Queue:
            if TLocker in Queueitem[2]:
                Transaction = Queueitem[0]
                ItemName = Queueitem[1]
                self.ReadLock(Transaction,ItemName,True)
        pass
    
    def ReadLock(self,Transaction,ItemName,bypass):
        if(self.isTransanctionQueued(Transaction and not bypass)):
            self.Queue.append([Transaction,ItemName,Transaction])
        
        isLocked, TLocker = self.isItemLocked(ItemName)
        if(isLocked):
            self.Queue.append([Transaction,ItemName,TLocker])
        else:
            print(f"XL{Transaction}({ItemName})",end="; ")
            self.LockTable.append([Transaction,ItemName])
            print(f"R{Transaction}({ItemName})",end="; ")
            
        return True
    
    def WriteLock(self,Transaction,ItemName):
        return True
    
    def Commit(self,Transaction):
        print(f"C{Transaction}",end="; ")
        for Locks in self.LockTable:
            if Transaction in Locks[0]:
                ItemName = Locks[1]
                print(f"UL{Transaction}({ItemName})",end="; ")
                self.LockTable.remove(Locks) 
        self.TryQueue(Transaction)

    
