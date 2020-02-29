#!/usr/bin/env python3

print("\nCustomer key decoding\n=====================\n\n")
myfile=open("CUSTOMERKEY", "rb")
key=myfile.readline()
myfile.close()

print ("Raw key is:\n")
print (key)

sum=key[0:8].decode("utf-8")
print("Checksum: ",sum)

v=0
decoded=b''
for c in key[8:]:
   c -= 77
   c %= 256
   v += c
   decoded += bytes([c])

print("Checksum from reading bytes: %08x"%v)

exp=decoded[0:8].decode("utf-8")
print("Expiration date: ",exp)

id=decoded[8:].decode("utf-8")
print("Customer name or id: ", id)

