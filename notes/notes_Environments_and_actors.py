spacing = 2.0
lower = gymapi.Vec3(-spacing, 0.0, -spacing)
upper = gymapi.Vec3(spacing, spacing, spacing)

env = gym.create_env(sim, lower, upper, 8)
#gym.create_env(simulation, lower, uper, number of environments)

#example of gym.create_actor()
pose = gymapi.Transform()
pose.p = gymapi.Vec3(0.0, 1.0, 0.0)
pose.r = gymapi.Quat(-0.707107, 0.0, 0.0, 0.707107)

actor_handle = gym.create_actor(env, asset, pose, "MyActor", 0, 1)
"""
.p - corrdiantes 
.r - orentation quaternion
.Quat(x,y,z,w)
see math utilities in maths.py

Question: For .create_actor(env, asset, pose, "MyActor", 0, 1) what does 0 and 1 do?
Answer: The last two integers are collision_group and collision_filter

collision_group: id that sign two bodies can collide with each other, 
                 so two bodies can physically interact with each other.
collision_filter: filter that to avoid two bodies collide who has same bit set
"""

# set up the env grid
num_envs = 64
envs_per_row = 8
env_spacing = 2.0
env_lower = gymapi.Vec3(-env_spacing, 0.0, -env_spacing)
env_upper = gymapi.Vec3(env_spacing, env_spacing, env_spacing)

# cache some common handles for later use
envs = []
actor_handles = []

# create and populate the environments
for i in range(num_envs):
    env = gym.create_env(sim, env_lower, env_upper, envs_per_row)
    envs.append(env)

    height = random.uniform(1.0, 2.5)

    pose = gymapi.Transform()
    pose.p = gymapi.Vec3(0.0, height, 0.0)

    actor_handle = gym.create_actor(env, asset, pose, "MyActor", i, 1)
    actor_handles.append(actor_handle)

