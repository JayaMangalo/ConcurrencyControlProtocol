class SimpleLocking:
    def __init__(self):
        self.LockTable = []
        self.Queue = []
        self.TransactionOrder = []
        self.AbortedTransaction = []
        pass
    
        
    def isItemLocked(self,ItemName):
        for Locks in self.LockTable:
            if ItemName in Locks[1]:
                return True, Locks[0]
        return False,False
                
    def isTransanctionAborted(self,Transaction):
        for Queueitem in self.AbortedTransaction:
            if Transaction in Queueitem[0] and Queueitem[2] in ("R","W"):
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
                        try:
                            self.Queue.remove(Queueitem)
                            Queues.remove(Queueitem)
                        except:
                            break
                    else:
                        break
                elif(Queueitem[2] == "W"):
                    if self.WriteLock(Transaction,ItemName,True):
                        try:
                            self.Queue.remove(Queueitem)
                            Queues.remove(Queueitem)
                        except:
                            break
                    else:
                        
                        break
                elif(Queueitem[2] == "C"):  
                    self.Queue.remove(Queueitem)
                    self.Commit(Transaction)
                    break
                        
    def TryRestart(self):
        TransactionOrder = []
        SeperateQueue = []
        
        for item in self.AbortedTransaction:
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
                        self.AbortedTransaction.remove(Queueitem)
                        Queues.remove(Queueitem)
                    else:
                        break
                elif(Queueitem[2] == "W"):
                    if self.WriteLock(Transaction,ItemName,True):
                        self.AbortedTransaction.remove(Queueitem)
                        Queues.remove(Queueitem)
                    else:
                        break
                elif(Queueitem[2] == "C"):  
                    self.AbortedTransaction.remove(Queueitem)
                    self.Commit(Transaction)
                    break
    
    
    def ReadLock(self,Transaction,ItemName,bypass):
        if(Transaction not in self.TransactionOrder):
            self.TransactionOrder.append(Transaction)
        
        if(self.isTransanctionAborted(Transaction) and not bypass):
            self.AbortedTransaction.append([Transaction,ItemName,"R"])
            return False
        
        if(self.isTransanctionQueued(Transaction) and not bypass):
            self.Queue.append([Transaction,ItemName,"R"])
            return False
        
        isLocked, TLocker = self.isItemLocked(ItemName)
        if(isLocked):
            if self.TransactionOrder.index(TLocker) == self.TransactionOrder.index(Transaction):
                print(f"R{Transaction}({ItemName})",end="; ")
                return True
            elif self.TransactionOrder.index(TLocker) > self.TransactionOrder.index(Transaction):
                self.Abort(TLocker)
                print(f"XL{Transaction}({ItemName})",end="; ")
                self.LockTable.append([Transaction,ItemName,"R"])
                print(f"R{Transaction}({ItemName})",end="; ")
                return True
            else:
                if not bypass:
                    self.Queue.append([Transaction,ItemName,"R"])
                
                return False
                
        else:
            print(f"XL{Transaction}({ItemName})",end="; ")
            self.LockTable.append([Transaction,ItemName,"R"])
            print(f"R{Transaction}({ItemName})",end="; ")
            return True
    
    def WriteLock(self,Transaction,ItemName,bypass):
        if(Transaction not in self.TransactionOrder):
            self.TransactionOrder.append(Transaction)
        
        if(self.isTransanctionAborted(Transaction) and not bypass):
            self.AbortedTransaction.append([Transaction,ItemName,"W"])
            return False
        
        if(self.isTransanctionQueued(Transaction) and not bypass):
            self.Queue.append([Transaction,ItemName,"W"])
            return False
        
        isLocked, TLocker = self.isItemLocked(ItemName)
        if(isLocked):
            if self.TransactionOrder.index(TLocker) == self.TransactionOrder.index(Transaction):
                print(f"W{Transaction}({ItemName})",end="; ")
                return True
            elif self.TransactionOrder.index(TLocker) > self.TransactionOrder.index(Transaction):
                self.Abort(TLocker)
                print(f"XL{Transaction}({ItemName})",end="; ")
                self.LockTable.append([Transaction,ItemName,"W"])
                print(f"W{Transaction}({ItemName})",end="; ")
                return True
            else:
                if not bypass:
                    self.Queue.append([Transaction,ItemName,"W"])
                
                return False
                
        else:
            print(f"XL{Transaction}({ItemName})",end="; ")
            self.LockTable.append([Transaction,ItemName,"W"])
            print(f"W{Transaction}({ItemName})",end="; ")
            return True
    
    def Commit(self,Transaction):
        if(self.isTransanctionAborted(Transaction)):
            self.AbortedTransaction.append([Transaction,None,"C"]) 
            return False
        
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
        
    def Abort(self,Transaction):
        print(f"A{Transaction}",end="; ")
        Locklist = []    
        for Locks in self.LockTable:
            if Transaction in Locks[0]:
                ItemName = Locks[1]
                Locklist.append(Locks)
                print(f"UL{Transaction}({ItemName})",end="; ")
                self.AbortedTransaction.append(Locks)
        for lockrelease in Locklist:
            self.LockTable.remove(lockrelease) 
        
        queuelist = []    
        for Queue in self.Queue:
            if Transaction in Queue[0]:
                ItemName = Queue[1]
                queuelist.append(Queue)
                print(f"UL{Transaction}({ItemName})",end="; ")
                self.AbortedTransaction.append(Queue)
        for queuerelease in queuelist:
            self.Queue.remove(queuerelease) 

    def End(self):
        i = 0
        while self.AbortedTransaction:
            self.TryRestart()
            i+=1
            if i == 15:
                print("MANUALBREAK")
                break # failsave #means that gigantic 5000+ transactions will fail