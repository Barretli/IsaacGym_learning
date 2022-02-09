
import numpy as np
from math import sqrt
from isaacgym import gymapi
from isaacgym import gymutil 

gym = gymapi.acquire_gym()

# parse arguments
args = gymutil.parse_arguments(
    description="Collision Filtering: Demonstrates filtering of collisions within and between environments",
    custom_parameters=[
        {"name": "--num_envs", "type": int, "default": 12, "help": "Number of environments to create"},
        {"name": "--all_collisions", "action": "store_true", "help": "Simulate all collisions"},
        {"name": "--no_collisions", "action": "store_true", "help": "Ignore all collisions"}])

# configure sim
sim_params = gymapi.SimParams()
if args.physics_engine == gymapi.SIM_FLEX:
    sim_params.flex.shape_collision_margin = 0.25
    sim_params.flex.num_outer_iterations = 4
    sim_params.flex.num_inner_iterations = 10
elif args.physics_engine == gymapi.SIM_PHYSX:
    sim_params.substeps = 1
    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 4
    sim_params.physx.num_velocity_iterations = 1
    sim_params.physx.num_threads = args.num_threads
    sim_params.physx.use_gpu = args.use_gpu

sim_params.gravity = gymapi.Vec3(0.0, -9.8, 0.0)
sim = gym.create_sim(args.compute_device_id, args.graphics_device_id, args.physics_engine, sim_params)
plane_params = gymapi.PlaneParams()
plane_params.distance = 0
plane_params.static_friction = 1
plane_params.dynamic_friction = 1
plane_params.restitution = 2
gym.add_ground(sim, plane_params)

viewer = gym.create_viewer(sim, gymapi.CameraProperties())

asset_root = "../../assets"
asset_file = "urdf/ball.urdf"
asset = gym.load_asset(sim, asset_root, asset_file, gymapi.AssetOptions())

num_envs = args.num_envs
num_per_row = int(sqrt(num_envs))
env_spacing = 1.25
env_lower = gymapi.Vec3(-env_spacing, 0.0, -env_spacing)
env_upper = gymapi.Vec3(env_spacing, env_spacing, env_spacing)

envs = []

gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_R, "reset")

np.random.seed(17)

for i in range(num_envs):
    env = gym.create_env(sim, env_lower, env_upper, num_per_row)
    envs.append(env)
    
    c = 0.1 + 2 * np.random.random(10)
    color = gymapi.Vec3(c[0], c[1], c[2])


    pose = gymapi.Transform()
    pose.r = gymapi.Quat(0, 0, 0, 1)
    
    pose.p = gymapi.Vec3(0, i, 0)

    ahandle = gym.create_actor(env, asset, pose, "ball", i, 1)
    gym.set_rigid_body_color(env, ahandle, 0, gymapi.MESH_VISUAL_AND_COLLISION, color)
    

gym.viewer_camera_look_at(viewer, None, gymapi.Vec3(20, 5, 20), gymapi.Vec3(0, 1, 0))

initial_state = np.copy(gym.get_sim_rigid_body_states(sim, gymapi.STATE_ALL))

while not gym.query_viewer_has_closed(viewer):

    # Get input actions from the viewer and handle them appropriately
    for evt in gym.query_viewer_action_events(viewer):
        if evt.action == "reset" and evt.value > 0:
            gym.set_sim_rigid_body_states(sim, initial_state, gymapi.STATE_ALL)

    # step the physics
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    # update the viewer
    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)

    # Wait for dt to elapse in real time.
    # This synchronizes the physics simulation with the rendering rate.
    gym.sync_frame_time(sim)

gym.destroy_viewer(viewer)
gym.destroy_sim(sim)
