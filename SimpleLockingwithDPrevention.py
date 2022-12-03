class SimpleLocking:
    def __init__(self):
        self.LockTable = []
        self.Queue = []
        self.TransactionOrder = []
        self.AbortedQueue = []
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
                
    def TryQueue(self,Transaction):
        for Queueitem in self.Queue:
            if Transaction in Queueitem[2]:
                ItemName = Transaction[1]
                # print(f"UL{Transaction}({ItemName})",end="; ")
                # self.Queue.append(Locks)
                # self.LockTable.remove(Locks) 
        pass
    
    def ReadLock(self,Transaction,ItemName):
        if(Transaction not in self.TransactionOrder):
            self.TransactionOrder.append(Transaction)
        
        
        if(self.isTransanctionQueued(Transaction)):
            self.Queue.append([Transaction,ItemName,Transaction])
        
        isLocked, TLocker = self.isItemLocked(ItemName)
        if(isLocked):
            if self.TransactionOrder.index(TLocker) == self.TransactionOrder.index(Transaction):
                print(f"R{Transaction}({ItemName})",end="; ")
            elif self.TransactionOrder.index(TLocker) > self.TransactionOrder.index(Transaction):
                self.Abort(TLocker)
                
            else:
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

    def Abort(self,Transaction):
        print(f"A{Transaction}",end="; ")
        for Locks in self.LockTable:
            if Transaction in Locks[0]:
                ItemName = Locks[1]
                print(f"UL{Transaction}({ItemName})",end="; ")
                self.Queue.append(Locks)
                self.LockTable.remove(Locks) 
                
                #add to queue
        self.TryQueue(Transaction)
    
