# -*- coding: utf-8 -*-
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
rect.size = (200, 300)
rect.position = (150-(screen_size[0]/2), 0)

# Add a button to set the throttle to maximum
button_launch = panel.add_button("Launch")
button_launch.rect_transform.position = (0, 120)

button_landing = panel.add_button("Landing")
button_landing.rect_transform.position = (0, 80)

# Add some text displaying the total engine thrust
text = panel.add_text("[...]")
text.rect_transform.position = (0, 0)
text.color = (1, 1, 1)
text.size = 18

# Set up a stream to monitor the throttle button
button_launch_clicked = conn.add_stream(getattr, button_launch, 'clicked')
button_landing_clicked = conn.add_stream(getattr, button_landing, 'clicked')

vessel = conn.space_center.active_vessel
while True:
    if button_launch_clicked():
    	text.content = 'Launch'
    	from falkinho3 import * 
        button_launch.clicked = False
        break   	

    if button_landing_clicked():
    	text.content = 'Landing'
    	from landing import *
        button_landing.clicked = False    	
        break

    time.sleep(0.1)