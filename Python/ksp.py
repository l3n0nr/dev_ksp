#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                         
# Date: 18/03/02
# Author: Lenon Ricardo(lenonr)
# Version: 0.0.10
#	a = alpha, beta, stable, freeze;
#	b = bugs;
#	c = version;
# 
# Functions:
#   - P1: Launch;
#       	- Development: Start: 18/02/03 - End: 18/02/03.
#   - P2: Control Speed;
#		-P2.1: Orbiter Manuver: 
#       	- Development: Start: 18/02/03 - End: -.
#   - P3: Deploy
#		P3.1: Second Stage 
#			- Orbiter Manuver:
#		P3.2: First Stage  
#			- Suicide Burn:
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 
#

# import libraris
import krpc
import time

# basic information's script
# # # # # # # # # # # # # # # # # # # # #
# script name
conn = krpc.connect(name='SpaceX Style')
canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (250,100) #width/height
rect.position = (210-(screen_size[0]/2),-200)

# Settings for text size in the panel on screen
text = panel.add_text("Countdown")
text.rect_transform.position = (0,-20)
text.color = (1,1,1)
text.size = 18

# Some values for altitudes
gravityturn = 12000

in_atmosfere = 12000
out_atmosfere = 24000

target_apoapsis = 80000 #verificar valores
target_periapsis = 80000 #verificar valores

# Part 01 - Launch
# # # # # # # # # # # # # # # # # # # # #
print "gravity turn at: " + str(gravityturn)
print "target_apoapsis: " + str(target_apoapsis)

# Now we're actually starting
vessel = conn.space_center.active_vessel

vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90,270) # inclination/position
vessel.control.throttle = 1

text.content = 'Three...'
print('3...'); time.sleep(1)
text.content = 'Two...'
print('2...'); time.sleep(1)
text.content = 'One...'
print('1...'); time.sleep(1)
text.content = 'LITOFF'
print('LITOFF!'); time.sleep(1)
text.content = 'Go!!'

# first stage
vessel.control.activate_next_stage()
text.content = 'Burn First Stage'

# while vessel.orbit.apoapsis_altitude < in_atmosfere:
# 	vessel.auto_pilot.target_pitch_and_heading(90,270) # inclination/position

if vessel.orbit.apoapsis_altitude > in_atmosfere and vessel.orbit.apoapsis_altitude < out_atmosfere:
	vessel.auto_pilot.target_pitch_and_heading(80,270) # inclination/position

if vessel.orbit.apoapsis_altitude > out_atmosfere: 
	vessel.auto_pilot.target_pitch_and_heading(45,270) # inclination/position

# Part 02 - Control Speed
# # # # # # # # # # # # # # # # # # # # #
# # while vessel.resources.amount('SolidFuel') > 0.1:
# Burn until the liquid fuel in the boosters is out
while vessel.resources.amount('LiquidFuel') > 0.3:
    time.sleep(1)

vessel.control.throttle = 0
text.content = 'Booster separation'
print('Booster separation')
vessel.control.activate_next_stage()

# Pitch 10 degrees to the west.
text.content = 'Turn to 80 degrees west'
vessel.auto_pilot.target_pitch_and_heading(80,90)


# Burn until we are at the altitude for the gravity turn.
while vessel.flight().mean_altitude < gravityturn:
   time.sleep(1)
   # Display the targeted apoapsis on screen
   text.content = 'Apoapsis: ' + str(vessel.orbit.apoapsis_altitude)
   # Display the altitude and apoapsis in command line.
   print "Mean altitude: " + str(vessel.flight().mean_altitude)
   print "Apoapsis: " + str(vessel.orbit.apoapsis_altitude)
   

text.content = 'Gravity turn'
print('Gravity turn')

# Turn 45 degrees west
vessel.auto_pilot.target_pitch_and_heading(45,90)

# Keep burning until the apoapsis is 100000 meters
while vessel.orbit.apoapsis_altitude < target_apoapsis:
   time.sleep(1)
   # Display the targeted apoapsis on screen
   text.content = 'Apoapsis: ' + str(vessel.orbit.apoapsis_altitude)
   # Display the altitude and apoapsis in command line.
   print "Mean altitude: " + str(vessel.flight().mean_altitude)
   print "Apoapsis: " + str(vessel.orbit.apoapsis_altitude)


text.content = 'Engine off'
vessel.control.throttle = 0
time.sleep(1)


text.content = 'First stage separation'
print('First stage separation')
vessel.control.activate_next_stage()
time.sleep(1)
time.sleep(1)

text.content = 'Short burn of second stage'
# This short burn with 25% thrust isn't really necessary.
vessel.control.throttle = 0.25
time.sleep(1)
vessel.control.throttle = 0

# Pitch to 20 degrees above the horizon. And burn the second stage for 10 seconds (just to make the trajectory a bit .. wider?
vessel.auto_pilot.target_pitch_and_heading(20,90)
vessel.control.throttle = 1

time.sleep(10)

vessel.control.throttle = 0

# Wait until we're on 90% of the apoapsis.
while vessel.flight().mean_altitude < target_apoapsis*0.9:
   time.sleep(1)
   text.content = 'Burn after %d meters' % (target_apoapsis*0.9 - vessel.flight().mean_altitude)


text.content = 'Turn to prograde'
print('Turn to prograde')

ap = vessel.auto_pilot
ap.reference_frame = vessel.orbital_reference_frame
ap.engage()

# Point the vessel in the prograde direction
# Not necessarily the most efficient way to get into orbit, but hey.
ap.target_direction = (0,1,0)


# text.content = 'Extend solar panels'
# vessel = conn.space_center.active_vessel
# for solar_panel in vessel.parts.solar_panels:
#     print solar_panel.state
#     solar_panel.deployed=True

# text.content = 'Orbital burn'
# vessel.control.throttle = 1

# # Keep burning until the periapsis is 72000 meters.
# while vessel.orbit.periapsis_altitude < target_periapsis:
#    time.sleep(1)
#    text.content = 'Periapsis: %d ' % vessel.orbit.periapsis_altitude


# vessel.control.throttle = 0

# # And... we're in orbit.. hopefully.
# text.content = 'Welcome to orbit!'
# print('Welcome to orbit!')