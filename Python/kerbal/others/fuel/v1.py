# -*- coding: utf-8 -*-
#!/usr/bin/env python

mass=14948      # 14.948 kg, final stage
taxa=0.145      # 0.145% fuel, first stage
plus_less=0.50  # percent

mass_plus=mass+(mass*plus_less)
mass_less=mass-(mass*plus_less)

value=5135      # kg
    # Values of the real prove:
    # Very heavy
    # x = ((24948*0,145)/14948) - 0,145 = 0,097002944                                

    # Normal
    # x = ((5135*0,145)/14948) + 0,145  = 0,194811012
        # Very Light
    #   x = ((1948*0,145)/14948)- 0,145 = −0,126103827

    # Equal default
    # x = ((14948*0,145)/14948)         = 0,145

def calc(mass, taxa, value):    
    # x = ((value * taxa)/mass)
    # x = ((mass * taxa)/ value)

    # print x

    if value > mass and value >= mass_less:
        # workins!
        x = ((value * taxa)/mass)
        if x <= 0.99:
            print ('Check you probe, this is very heavy!!')            
            # print x
        else:
            print 'value > mass',x
            x = x - taxa
            print 'Fuel first stage:',x,'%'
            # print ('value:',value, '>', 'mass:',mass)      
    elif value < mass and value <= mass_plus:          
        # x = ((mass * taxa)/ value)
        x = ((value * taxa)/mass)        
        # if x <= 0.06:
        #     print ('Check you probe, this is very light!!')            
        #     # print x
        # else:
        print 'value < mass',x
        x = 1 - (x + taxa)
        print 'Fuel first stage:',x,'%'
        # print ('mass:',mass, '>','value:',value)      
    else:
        # x = ((value * taxa)/mass)
        # print 'Fuel first stage:',x,'%'
        # print ('value = mass')          
        print ('??')

calc(mass, taxa, value)

# if mass_less >= value or mass_plus <= value or value == mass:
#     calc(mass, taxa, value)
# else:
#     print '+',mass_plus
#     print '-',mass_less
#     print 'V',value
#     print ('Very heavy or very light. Check you vessel!')