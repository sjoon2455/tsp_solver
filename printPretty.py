# coding : utf-8

### print prettily inserting "-" before and after a given string returning the same length
### input: string
### output: string(pretty)
def printPretty(s):
    leng = len(s)
    resLen = 50
    dashLen = (resLen - leng)/2
    #dashLen = int(dashLen)
    
    #print(dashLen)
    if dashLen % 1 == 0:
        #print(dashLen)    
        dashLen = int(dashLen)   
        res = "-" * dashLen + s + "-" * dashLen
    else:
        #print(dashLen, "9.5")
        dashLen = int(dashLen)
        res = "-" * dashLen + s + "-" * (dashLen+1)
    print(res)

#printPretty("Checking whether it's login GUI")
#printPretty("Getting xml hierarchy and parsing...")
