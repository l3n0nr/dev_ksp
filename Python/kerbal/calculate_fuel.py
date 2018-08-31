# -*- coding: utf-8 -*-
#!/usr/bin/env python

plus_less=0.50  # percent
mass=14948      # 14.948 kg, final stage
taxa=0.145      # 0.145% fuel, first stage
mass_30plus=mass+(mass*plus_less)
mass_30less=mass-(mass*plus_less)

value=14948
    # Test values:
    # x = ((24948*0,145)/14948) - 0,145 = 0,097002944                                
    # x = ((5135*0,145)/14948) + 0,145  = 0,194811012
    #   x = ((1948*0,145)/14948)- 0,145 = −0,126103827
    # x = ((14948*0,145)/14948)         = 0,145

def calc(mass, taxa, value):    
    x = ((value * taxa)/mass)

    # print x

    if value > mass:
        if x <= 0.99:
            print ('Check you probe, this is very heavy!!')            
            # print x
        else:
            x = x - taxa
            print 'Fuel first stage:',x,'%'
            # print ('value:',value, '>', 'mass:',mass)      
    elif value < mass:          
        x = ((value * taxa)/mass)
        if x <= 0.02:
            print ('Check you probe, this is very light!!')            
            # print x
        else:
            x = x + taxa
            print 'Fuel first stage:',x,'%'
            # print ('mass:',mass, '>','value:',value)      
    else:
        x = ((value * taxa)/mass)
        print 'Fuel first stage:',x,'%'
        # print ('value = mass')          

if mass_30less >= value or mass_30plus <= value or value == mass:
    calc(mass, taxa, value)
else:
    print '+',mass_30plus
    print '-',mass_30less
    print 'V',value
    print ('Very heavy or very light. Check you vessel!')