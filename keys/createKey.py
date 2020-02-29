#!/usr/bin/env python3

print("\nCustomer key creation\n=====================\n\n")
id=input("Enter customer name or id: ")
exp="0"
while int(exp)<20200101:
   exp=input("Enter expiration date (YYYYMMDD): ")
   if int(exp)<20200101:
      print("\nBad date.\nThe format should be 4 digits for year, 2 digits for month, 2 digits for day\n")


line=str.encode(exp+id)
sum=0
k=b''
for c in line:
	sum+=c
	c+=77
	c%=256
	k+=bytes([c])

key=str.encode("%08x"%sum)
key+=k
myfile=open("CUSTOMERKEY", "wb")
myfile.write(key)
myfile.close()
print("\nCustomer key is in file CUSTOMERKEY")
