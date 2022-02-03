#Running The Simulation

while True:
    # step the physics
    gym.simulate(sim)
    gym.fetch_results(sim, True)

#create viewer

cam_props = gymapi.CameraProperties()
viewer = gym.create_viewer(sim, cam_props)

#update viewer for each iteration
gym.step_graphics(sim)
gym.draw_viewer(viewer, sim, True)
"""
step_graphics() - synchronizes visual and physics state
draw_viewer() - render latest view
notes: this will refresh window very fast
"""

#refersh window by real time
gym.sync_frame_time(sim)

#stop sim after close window
while not gym.query_viewer_has_closed(viewer):

    # step the physics
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    # update the viewer
    gym.step_graphics(sim);
    gym.draw_viewer(viewer, sim, True)

    # Wait for dt to elapse in real time.
    # This synchronizes the physics simulation with the rendering rate.
    gym.sync_frame_time(sim)

#some custom input
gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_SPACE, "space_shoot")
gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_R, "reset")
gym.subscribe_viewer_mouse_event(viewer, gymapi.MOUSE_LEFT_BUTTON, "mouse_shoot")
...
while not gym.query_viewer_has_closed(viewer):
    ...
    for evt in gym.query_viewer_action_events(viewer):
        ...
"""
more in projectiles.py
"""

#cleanup
gym.destroy_viewer(viewer)
gym.destroy_sim(sim)