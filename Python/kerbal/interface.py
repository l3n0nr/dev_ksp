#!/usr/bin/env python

# Reference: <krpc.github.io/krpc/tutorials/user-interface.html>

import time, krpc

conn = krpc.connect(name='User Interface Example')
canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
rect = panel.rect_transform
rect.size = (200, 400)
rect.position = (150-(screen_size[0]/2), 0)

# # Add a button to set the throttle to maximum
# button_launch = panel.add_button("Launch")
# button_launch.rect_transform.position = (0, 120)

# button_landing = panel.add_button("Landing")
# button_landing.rect_transform.position = (0, 80)

size = 180
size_t = 30

# Add a button to set the throttle to maximum
button_launch = panel.add_button("Sub-orbital")
button_launch.rect_transform.position = (0, size)

button_orbit = panel.add_button("Execute Manuveur")
button_orbit.rect_transform.position = (0, size-size_t)

button_landing = panel.add_button("Landing")
button_landing.rect_transform.position = (0, size-(size_t*2))

# Add some text displaying the total engine thrust
text = panel.add_text("[...]")
text.rect_transform.position = (0, -50)
text.color = (1, 1, 1)
text.size = 18

# Set up a stream to monitor the throttle button
button_launch_clicked = conn.add_stream(getattr, button_launch, 'clicked')
button_orbit_clicked = conn.add_stream(getattr, button_orbit, 'clicked')
button_landing_clicked = conn.add_stream(getattr, button_landing, 'clicked')

vessel = conn.space_center.active_vessel
while True:
    if button_launch_clicked():
        text.content = 'Launch'

        # from base import sub_orbital
        # sub_orbital()
        from falkinho3 import *
        main()
        
        button_launch.clicked = False   

    if button_orbit_clicked():
        text.content = 'Orbital Maneuver'

        from base import orbital_maneuver
        orbital_maneuver()
        
        button_orbit.clicked = False    
    
    if button_landing_clicked():
        text.content = 'Landing'

        from base import landing_test
        landing_test()

        button_landing.clicked = False  

    time.sleep(0.1)