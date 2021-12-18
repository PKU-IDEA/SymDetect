message_types = {'i' : "INFO", 'w' : "WARN", 'e' : "ERROR", 'd' : "DEBUG"}

def info(mtype, mstring, mverbose=False, maux=None):
    mname = message_types[mtype]
    print("["+mname+"]", mstring)
    if mverbose:
        print("-"*15+"Additional Output"+"-"*15)
        print(maux)
        print("-"*47)
    pass
