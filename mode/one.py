mode=0
result=0
second=0

def stop():
    global mode
    # global result
    global second
    print('mode={}'.format(mode))
    mode+=1
    if mode>1000000:
        print('stop')
        result=(0,0)
        second=3
    else:
        result=(50,50)
        second=0
    return result,second