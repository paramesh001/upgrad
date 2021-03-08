#!/usr/bin/env python
# coding: utf-8

# In[2]:


print("Enter the input measure-['celsius','fahrenheit','kelvin',rankine]")
input_standard=input()
print("enter the measure value-")
input1=float(input())

print("Enter the output measure-['celsius','fahrenheit','kelvin','rankine']")
output_standard=input()
print("enter the measure value-")
output_given=float(input())


# In[3]:


# function for conversion
def convert_measure(input_standard,input1,output_standard):
   
    #convert input to celsius
    if input_standard=="fahrenheit":
        input2=(input1-32)*5/9
    elif( input_standard=="celsius"):
        input2=input1
    elif input_standard=="kelvin":
        input2=input1-273.15
    elif input_standard=="rankine":
        input2=(input1-491.67)*5/9
        #convert celsius to output standard
    if output_standard=="fahrenheit":
        output_1=(input2*9/5)+32
    elif( output_standard=="celsius"):
        output_1=input2
    elif output_standard=="kelvin":
        output_1=input2+273.15
    elif output_standard=="rankine":
        output_1=(input2*9/5)+491.67

        return output_1


# In[ ]:


# function to check wether the answer is corect or not

def check(output_given,output1):
    if(output_given==output1):
        print("correct conversion")
    else:
        print("wrong conversion")


# In[ ]:


#testing  
print("Enter the input measure-['celsius','fahrenheit','kelvin',rankine]")
in_standard=input()
print("enter the measure value-")
input1=float(input())
print("Enter the output measure-['celsius','fahrenheit','kelvin','rankine']")
output_standard=input()
print("enter the measure value-")
output_given=float(input())
checker=convert_measure(input_standard,input1,output_standard)
check(checker,output_given)


# In[ ]:




