#Loading Assets
asset_root = "../../assets"
asset_file = "urdf/franka_description/robots/franka_panda.urdf"
asset = gym.load_asset(sim, asset_root, asset_file)

"""
load_asset(sim , asset_root, asset_file):
    asset_root: absolute path to current working directory
    asset_file: asset file format
        .urdf for URDF files
        .xml for MJCF files
        .usd/.usda for USD files
"""

#for pass extra info to the asset importer
"""
Called by AssetOptions()
"""
asset_options = gymapi.AssetOptions()
asset_options.fix_base_link = True
asset_options.armature = 0.01

asset = gym.load_asset(sim, asset_root, asset_file, asset_options)

#Loading Mashes in Assets
"""
We can use meshes to specified in assets, if asset file also specifies for that mesh,
then materials from the asset take priority
To use mesh materials instead, use:
"""
asset_options_mesh_materials = True

"""
To force isaacgym always generate smooth vertex normals/face normals
for mesh has incomplete normals use
"""
asset_options.mesh_normal_mode = gymapi.COMPUTE_PER_VERTEX
asset_options.mesh_normal_mode = gymapi.COMPUTE_PER_FACE

"""
If mesh has submeshes that represent a convex decomposition
to load the submeshes as seperate shapes in the asset use
"""
asset_options.convex_decomposition_from_submeshes = True

#Overriding Inertial Properties
"""
Each rigid body as a center of mass and inertia tensor
To adjust/overrid these for better simulation use
See python/examples/convex_decomposition.py for sample usage.
"""
asset_options.override_com = True
asset_options.override_inertia = True

#Convex Decomposition
#enable convex decomposition
asset_options.vhacd_enabled = True

#perform the convex decomposition
asset_options.vhacd_params.resolution = 300000
asset_options.vhacd_params.max_convex_hulls = 10
asset_options.vhacd_params.max_num_vertices_per_ch = 64
"""
called by isaacgym.gymapi.VHacdParams
See python/examples/convex_decomposition.py for sample usage
"""
