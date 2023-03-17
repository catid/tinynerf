import torch
from src.core import OccupancyGrid, NerfRenderer, mip360_contract
from src.models import VanillaFeatureMLP, VanillaOpacityDecoder, VanillaColorDecoder

def test_occupancy_grid():
    grid = OccupancyGrid(128)
    grid.grid[:,:,64:] = 0.

    # about 1/2 of the occupancies should be set
    assert grid.grid.sum().item() >= grid.grid.numel() / 3.
    assert grid.grid.sum().item() <= 2. * grid.grid.numel() / 3.
    assert grid.grid.size() == (128, 128, 128)

    coords = [ 
        [32,32,32],
        [32,32,96],
        [32,96,32],
        [32,96,96],
        [96,32,32],
        [96,32,96],
        [96,96,32],
        [96,96,96],
    ]
    unit_coords = 2. * (torch.tensor(coords) / grid.size) - 1.
    occs = [
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
    ]


    print(grid(unit_coords))
    assert torch.all(grid(unit_coords) == torch.tensor(occs))
 
def test_occupancy_grid_update():
    # setup vanilla nerf
    feature_mlp = VanillaFeatureMLP(10, [256 for k in range(8)])
    opacity_decoder = VanillaOpacityDecoder(256)

    def sigma_fn(t: torch.Tensor):
        features = feature_mlp(t)
        opacity = opacity_decoder(features)
        return opacity

    occupancy_grid = OccupancyGrid(32)
    occupancy_grid.update(sigma_fn)
    assert occupancy_grid.grid.sum().item() <= occupancy_grid.grid.numel()

def test_renderer_vanilla_nerf():
    # setup vanilla nerf
    feature_mlp = VanillaFeatureMLP(10, [256 for k in range(8)])
    opacity_decoder = VanillaOpacityDecoder(256)
    color_decoder = VanillaColorDecoder(4, 256, [128])
    
    def occupancy_fn(t: torch.Tensor):
        features = feature_mlp(t)
        opacity = opacity_decoder(features)
        return opacity

    occupancy_grid = OccupancyGrid(64)
    occupancy_grid.update(occupancy_fn)

    renderer  = NerfRenderer(
        occupancy_grid,
        feature_mlp,
        opacity_decoder,
        color_decoder,
        mip360_contract
    )

    rays_o = torch.rand(100, 3)
    rays_d = torch.rand(100, 3)

    rendered_rgb, _ = renderer(rays_o, rays_d)

    assert rendered_rgb.size() == (100, 3)