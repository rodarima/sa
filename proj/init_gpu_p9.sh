#!/bin/bash

module purge; module load gcc/6.4.0 java/ibm_8.0.5.15 openmpi/3.0.0 cuda/9.2 atlas/3.10.3

# CUDNNv7.1.4
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/cuda/targets/ppc64le-linux/lib
export LIBRARY_PATH=$LIBRARY_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/cuda/targets/ppc64le-linux/lib
export C_INCLUDE_PATH=$C_INCLUDE_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/cuda/targets/ppc64le-linux/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/cuda/targets/ppc64le-linux/include

# NCCLv2.2.12
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/nccl/lib
export LIBRARY_PATH=$LIBRARY_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/nccl/lib
export C_INCLUDE_PATH=$C_INCLUDE_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/nccl/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/gpfs/projects/sam14/mt_p9/nv_pkgs/nccl/include

source /gpfs/projects/sam14/mt_p9/virtualenv/tf_gpu_p9/bin/activate
