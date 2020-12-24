from two import decision
import one

while True:
    result,second=decision()
    #send result to pi
    if result==(0,0):
        one.mode=0