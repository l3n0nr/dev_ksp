# -*- coding: utf-8 -*-
#!/usr/bin/env python

mass=14948      # 14.948 kg, final stage
taxa=0.145      # 0.145% fuel, first stage

value=1135
                # x = ((24948*0,145)/14948) - 0,145 = 0,097002944                                
                # x = ((5135*0,145)/14948) + 0,145  = 0,194811012
                #   x = ((1948*0,145)/14948)- 0,145 = −0,126103827
                # x = ((14948*0,145)/14948)         = 0,145

def calc(mass, taxa, value):
    if value > mass:
        x = ((value * taxa)/mass) 
        x = x - taxa

        print ('value:',value, '>', 'mass:',mass)      
    elif value < mass:        
        # x = ((value * taxa)/mass)   
        x = ((value / mass)+taxa)   
        # x = taxa + x

        print ('mass:',mass, '>','value:',value)      
    else:
        x = ((value * taxa)/mass)

        print ('value = mass')      
    
    print x
    
    # if x <= 0.10:
    #     print ('Heavy-heavy!!')
    # elif x > 0.18:
    #     print ('Light-light!!')
    # else:
    #     print ('Lets GO!!')


calc(mass, taxa, value)