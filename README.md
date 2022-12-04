# ConcurrencyControlProtocol
A program to implement CCP: ConcurrencyControlProtocol

1. Part 1: Simple Locking
    There is 2 programs for this section, SimpleLocking.py and SimpleLockingwithDPrevention.py
    - SimpleLocking.py is the version that does not have deadlock prevention (as required in specification) 
    - SimpleLockingwithDPrevention.py has a deadlock prevention method (Wound-Wait). The SimpleLockingwithDPrevention is simply experimental and does not work as expected with large test cases (~50 lines).

    How to Run:
    - python LockManagertest.py
    - You may change the test cases by changing the targeted filename in LockManagertest.py 
    - (Optional) You may change to DBPreventionMode by changing the imports from SimpleLocking to SimpleLockingwithDBPrevention simply by uncommenting 