import krpc
conn = krpc.connect()
vessel = conn.space_center.active_vessel

root = vessel.parts.root
stack = [(root, 0)]
while stack:
    part, depth = stack.pop()
    if part.axially_attached:
        attach_mode = 'axial'
    else:  # radially_attached
        attach_mode = 'radial'
    print(' '*depth, part.title, '-', attach_mode)
    for child in part.children:
        stack.append((child, depth+1))