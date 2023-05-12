# tinynerf

Concise (<1000 locs) and fast implementation of several NeRF techniques. Currently it contains an implementation of vanilla [NeRF](https://arxiv.org/abs/2003.08934), [K-Planes](https://arxiv.org/abs/2301.10241) and [Cobafa](https://arxiv.org/abs/2302.01226), accelerated with a single CUDA kernel to compute the weights from 'NeRF equation'.

[](https://user-images.githubusercontent.com/53355258/227556618-2e01b870-4191-4323-b254-c13c01c428db.mp4)

## Setup

Create a conda environment, install PyTorch, and install requirements.

```bash
conda create -n tinynerf python=3.10
conda activate tinynerf

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r requirements.txt
```

I got the dataset from nerfstudio, running the `ns-download-data blender` command and then copying it to `./data/`.

Run it:

```bash
CUDA_VISIBLE_DEVICES=1 python train.py --data data/blender/chair --method kplanes --datatype synthetic --output k_planes --batch_size 512
```

## Features

- [x] Vanilla NeRF, K-Planes and Cobafa
- [x] Occupancy grid to accelerate training (based on Instant-NGP but with slightly different decaying method)
- [x] Unbounded and AABB scenes
- [x] Dynamic batches, each iteration process a constant number of samples by packing samples from each ray
- [x] CUDA implementation of NeRF weights computation
- [x] Reproduction of KPlanes results on synthetic dataset
- [ ] Reproduction of Cobafa results on synthetic dataset
- [ ] Proposal sampling
- [x] COLMAP data loading
- [ ] Appearance embedding

## References

These repositories were useful learning resources :
- [https://github.com/KAIR-BAIR/nerfacc]()
- [https://github.com/apchenstu/TensoRF]()
- [https://github.com/sarafridov/K-Planes]()
