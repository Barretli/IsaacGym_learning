#Assets options
asset_options = gym.AssetOptions()
asset_options.density = 10.0

box_asset = gym.create_box(sim, width, height, depth, asset_options)
sphere_asset = gym.create_sphere(sim, radius, asset_options)
capsule_asset = gym.create_capsule(sim, radius, length, asset_options)
"""
This alows use to create box, and there's more options see
class isaacgym.gymapi.AssetOptions()

For collections of components in each asset see
examples/asset_info.py for sample use
"""

#Creating Actors
"""
see deatils in Environments and actors notes
"""



