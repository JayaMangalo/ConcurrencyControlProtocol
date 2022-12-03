from SimpleLocking import SimpleLocking


if __name__ == "__main__":
    
    filename = "test/test1.txt"
    f = open(filename, "r")

    lm = SimpleLocking()

    for line in f:
        data = line.split()
        
        Transaction = data[1]
        if data[0] == 'R':
            ItemName = data[2]
            lm.ReadLock(Transaction,ItemName,False)
            
        elif data[0] == 'W':
            ItemName = data[2]
            lm.WriteLock(Transaction,ItemName,False)
            
        elif data[0] == 'C':
            Transaction = data[1]
            lm.Commit(Transaction)
            
        