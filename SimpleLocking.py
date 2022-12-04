class SimpleLocking:
    def __init__(self):
        self.LockTable = []
        self.Queue = []
        pass
    
    def isItemLocked(self,ItemName):
        for Locks in self.LockTable:
            if ItemName in Locks[1]:
                return True
        return False
                
    def isTransanctionQueued(self,Transaction):
        for Queueitem in self.Queue:
            if Transaction in Queueitem[0] and Queueitem[2] in ("R","W"):
                return True
        return False
                
    def TryQueue(self):
        TransactionOrder = []
        SeperateQueue = []
        
        for item in self.Queue:
            if item[0] not in TransactionOrder:
                TransactionOrder.append(item[0])
                SeperateQueue.append([item])
            else:
                idx = TransactionOrder.index(item[0])
                SeperateQueue[idx].append(item)
        
        for Queues in SeperateQueue:    
            while Queues:
                Queueitem = Queues[0]
                Transaction = Queueitem[0]
                ItemName = Queueitem[1]
                
                if(Queueitem[2] == "R"):
                    if self.ReadLock(Transaction,ItemName,True):
                        self.Queue.remove(Queueitem)
                        Queues.remove(Queueitem)
                    else:
                        break
                elif(Queueitem[2] == "W"):
                    if self.WriteLock(Transaction,ItemName,True):
                        self.Queue.remove(Queueitem)
                        Queues.remove(Queueitem)
                    else:
                        break
                elif(Queueitem[2] == "C"):  
                    self.Queue.remove(Queueitem)
                    self.Commit(Transaction)
                    break
                        
       
    
    def ReadLock(self,Transaction,ItemName,bypass):
        if(self.isTransanctionQueued(Transaction) and not bypass):
            self.Queue.append([Transaction,ItemName,"R"])
            return False
        
        isLocked = self.isItemLocked(ItemName)
        if(isLocked):
            if not bypass:
                self.Queue.append([Transaction,ItemName,"R"])
            return False
        else:
            print(f"XL{Transaction}({ItemName})",end="; ")
            self.LockTable.append([Transaction,ItemName])
            print(f"R{Transaction}({ItemName})",end="; ")
            return True
    
    def WriteLock(self,Transaction,ItemName,bypass):
        if(self.isTransanctionQueued(Transaction) and not bypass):
            self.Queue.append([Transaction,ItemName,"W"])
            return False
        
        isLocked = self.isItemLocked(ItemName)
        if(isLocked):
            if not bypass:
                self.Queue.append([Transaction,ItemName,"W"])
            return False
        else:
            print(f"XL{Transaction}({ItemName})",end="; ")
            self.LockTable.append([Transaction,ItemName])
            print(f"W{Transaction}({ItemName})",end="; ")
            return True
    
    def Commit(self,Transaction):

        if(self.isTransanctionQueued(Transaction)):
            self.Queue.append([Transaction,None,"C"]) 
            return False
        
        print(f"C{Transaction}",end="; ")
        Locklist = []    
        for Locks in self.LockTable:
            if Transaction in Locks[0]:
                ItemName = Locks[1]
                Locklist.append(Locks)
                print(f"UL{Transaction}({ItemName})",end="; ")
        for lockrelease in Locklist:
            self.LockTable.remove(lockrelease) 
            
        self.TryQueue()

        
    def End(self):
        if self.Queue:
            print("DEADLOCK OCCURRED")

    
