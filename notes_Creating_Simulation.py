from isaacgym import gymapi #<- importing the core API

"""
So we can pull all the Gym API function by calling gymapi
gym = gymapi.acquire_gym()
"""

gym = gymapi.acquire_gym()

"""
Creating Simulation
"""

#create_sim

"""
sim_params = gymapi.SimParams()
sim = gym.create_sim(compute_device_id, graphics_device_id, gymapi.SIM_PHYSX, sim_params)

the sim called create_sim function to load assets, 
create environments and interact with the simulation

In create_sim()
#1 -> selects GPU for physic simulation
#2 -> selects GPU for rendering
^^ so this alowing us to use multi-gpu to for simulation
#3 -> choose physics backend
    we have:
    SIM_PHYSX -> for rigid body, run either CPU or GPU, fully supports new tensor API
    SIM_FLEX -> for soft body and rigid body, only GPU, not fully supports tensor API(yet)
#4 -> addition simulation parameters
"""

#Simulation Parameters


# get default set of parameters
sim_params = gymapi.SimParams()

# set common parameters
sim_params.dt = 1 / 60 
sim_params.substeps = 2
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
"""
dt - simulation timestep, default is 1/60s
substeps - Number of simulation substeps, default is 2. 
           The effective simulation timestep is dt/substeps
note: if the timestep under 1/50s will lead to instabilities
"""

# set PhysX-specific parameters
sim_params.physx.use_gpu = True
sim_params.physx.solver_type = 1
sim_params.physx.num_position_iterations = 6
sim_params.physx.num_velocity_iterations = 1
sim_params.physx.contact_offset = 0.01
sim_params.physx.rest_offset = 0.0
"""
solver_type - type of solver (TGS - is an non-linear iterative solver)
contact_offset - if distance is less than the sum contact_offset will generate contacts
                 default is 0.02m
reset_offset - two shapes will come to reset if distance equal to sum of their rest_offset
               default is 0.01m
num_position_iterations - Position iteration count Default 4
num_velocity_iterations - Velocity iterations count Default 1
"""

# set Flex-specific parameters
sim_params.flex.solver_type = 5
sim_params.flex.num_outer_iterations = 4
sim_params.flex.num_inner_iterations = 20
sim_params.flex.relaxation = 0.8
sim_params.flex.warm_start = 0.5
"""
for reference solver type:
    1 - Newton Jacobi (GPU) - Jacobi solver on GPU (CUDA)
    2 - Newton LDLT (CPU) - Cholesky backend on CPU (Eigen-based)
    3 - Newton PCG1 (CPU) - Preconditioned conjugate gradient on CPU (Eigen-based)
    4 - Newton PCG2 (GPU) - Preconditioned conjugate gradient on GPU (CUDA)
    5 - Newton PCR (GPU) - Preconditioned conjugate residual method on GPU (CUDA)

num_outer_iterations - number of iterations by solver/(simulation substep)
number_inner_iterations - number of linear solver iterations for each outer iterations 
                          only use by Newton solvers
relaxation - convergence rate. greater than 1 may lead to instability
             damping = 1 - (1-relaxation)^num_outer_iterations
warm_start - use for next simulation step. default is 0.4. 
             Larger value could lead to more bouncy behavior or instabilities.
             For simulate slow-moving system with lot of contacts can try up to 1.0
"""

# create sim with these parameters
sim = gym.create_sim(compute_device_id, graphics_device_id, physics_engine, sim_params)

#Up Axis
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)
"""
UP_AXIS_Y - Y axis points up
UP_AXIS_Z - Z axis points up
"""

#Creating a Ground Plane

# configure the ground plane
plane_params = gymapi.PlaneParams()
plane_params.normal = gymapi.Vec3(0, 0, 1) # z-up!
plane_params.distance = 0
plane_params.static_friction = 1
plane_params.dynamic_friction = 1
plane_params.restitution = 0
"""
normal - define plane orientation
         (0, 0, 1) z-up
         (0, 1, 0) y-up
distance - distance of the plane from the orgin
static_friction/ dynamic_friction - coefficients of static/dynamic friction
restitution - to control the elasticity of collisions with the ground plane(bounce on ground)
"""

# create the ground plane
gym.add_ground(sim, plane_params)