############# Importing modules and stuffs we require  ######################################################

try:
        import sys
        from functools import lru_cache, cmp_to_key
        from heapq import merge, heapify, heappop, heappush
        # from math import *
        from collections import defaultdict as dd, deque, Counter as Cntr
        from itertools import combinations as comb, permutations as perm
        from bisect import bisect_left as bl, bisect_right as br, bisect, insort
        from time import perf_counter
        from fractions import Fraction
        import copy
        from copy import deepcopy
        import time
        starttime = time.time()
        mod = int(pow(10, 9) + 7)
        mod2 = 998244353

        def data(): return sys.stdin.readline().strip()
        def out(*var, end="\n"): sys.stdout.write(' '.join(map(str, var))+end)
        def L(): return list(sp())
        def sl(): return list(ssp())
        def sp(): return map(int, data().split())
        def ssp(): return map(str, data().split())
        def l1d(n, val=0): return [val for i in range(n)]
        def l2d(n, m, val=0): return [l1d(n, val) for j in range(m)]
        def A2(n,m): return [[0]*m for i in range(n)]
        def A(n):return [0]*n
        # sys.setrecursionlimit(int(pow(10,6)))
        # from sys import stdin
        # input = stdin.buffer.readline
        # I = lambda : list(map(int,input().split()))
        # import sys
        # input=sys.stdin.readline

        import random

except:
        pass
############# Importing modules and stuffs we require  ######################################################


























###############################################  Actual Code begin here  ##################################################################


# Define the source station
# We will have 5 stations having 3 messages each which they will try to send to a common destination, different destination path will just be slightly complex to implement
Sources = []
for i in range(5):
        Sources.append(deque())
        for j in range(3):
                Sources[-1].append(chr(ord("A")+i)+str(j))

# Our destination
Dest = []



# T is the time taken to reach from source to destination by a packet
T = 500
# Tf is the packet length
Tf = 100
# Here for example a channel can accomodate 5 different frames/packet




# This is the time when each station wants to send the message
Send_time = [0 for i in range(5)]


# This is the time when each station which sent a frame is expecting a acknowledgement, it is expected after 2*T time of sending a frame, for -1, it means it is not expecting any acknoledgement
Acknowledge = [-1 for i in range(5)]


# Our time counter
cur_t = 0


# A queue to store all the packets which are in the channel
cur_transmitting_message = deque()

# A queue to store all the Acknowledgement which are in the channel
cur_transmitting_Ack = []




# While all the packets haven't arrived in the Destination
while(len(Dest)<15):

        # if cur_t%100==0: print("Time", cur_t, "Send Time", Send_time, "Acknowledge ", Acknowledge,"Sources ",*Sources,"Dest ",Dest)

        # If a packet reaches the destination, we send an acknowledgement from the Destination
        while cur_transmitting_message and cur_transmitting_message[0][0]+T == cur_t:
                heappush(cur_transmitting_Ack,[cur_t+5,cur_transmitting_message[0][1]])
                cur_transmitting_message.popleft()


        # If a acknowledgement reaches the source
        if cur_transmitting_Ack and cur_transmitting_Ack[0][0]==cur_t:
                print("Initial source at t = ", cur_t)


                for i,ele in enumerate(Sources):
                        print("\t Source = ",chr(ord("A")+i),"::  Values = ",*ele)

                print("Initial Dest ", *Dest)

                print("Current arrived Packets")

                # For all the acknowledgments that were intented to be delivered at this time
                while  cur_transmitting_Ack and cur_transmitting_Ack[0][0]==cur_t:
                        x,y = heappop(cur_transmitting_Ack)
                        Dest.append(y)

                        print(y)

                        for i in range(5):
                                if y in Sources[i]:
                                        Sources[i].remove(y)
                                        Acknowledge[i]=-1
                                        Send_time[i] = cur_t+random.randint(0,10**3) if len(Sources[i]) else 0
                                        break

                print("Final source at t = ", cur_t)


                for i,ele in enumerate(Sources):
                        print("\t Source = ",chr(ord("A")+i),"::  Values = ",*ele)

                print("Final Dest ", *Dest)
                print("-"*100)




        # If a station is expecting an ackowledgment at this point of time, that means its packet collided, randomly allot it next sending time
        if cur_t in Acknowledge:
                for i in range(5):
                        if Acknowledge[i]==cur_t:
                                Acknowledge[i]=-1
                                Send_time[i] = cur_t+random.randint(0,10000)



        # Check all the packets which are ready to send at this point of time
        ready_to_send = []
        for i in range(5):
                if Send_time[i]==cur_t:
                        ready_to_send.append(i)


        # If there are packets
        if len(ready_to_send):
                # If there is only 1 packet to send and the last packet which was to be sent was before Tf time, sent the packet
                if ((cur_transmitting_message and cur_t+Tf<cur_transmitting_message[-1][0]) or len(cur_transmitting_message)==0) and len(ready_to_send)==1:
                        ele = ready_to_send[0]
                        Acknowledge[ele] = cur_t + 2*T
                        cur_transmitting_message.append([cur_t,Sources[ele][0]])
                # Else collision will occur and all the packets which were meant to send at this point plus all the packets which were sent within the last Tf second will be discarded
                else:
                        while(cur_transmitting_message and cur_t+Tf>=cur_transmitting_message[-1][0]):
                                cur_transmitting_message.pop()
                        # Give an acknowledgement time so that the packets realise after 2*T time that collision occured
                        for ele in ready_to_send:
                                Acknowledge[ele] = cur_t + 2*T

        cur_t+=1



print("Total time taken = ", cur_t)
print("Total number of frame sent = ", len(Dest))


print("For an highly efficient system total time taken should have been", len(Dest)*Tf)
Teff = len(Dest)*Tf+T-Tf
efficiency = Teff/cur_t
print("Efficiency (in %) = ", efficiency*100)


print("\n\n*Note that the time is in unit where we can define unit to be as second or millisecond whatever we want")
