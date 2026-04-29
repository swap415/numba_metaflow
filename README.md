# numba-metaflow

Reproduce numba [issue #9931](https://github.com/numba/numba/issues/9931)
across a `(python, numba)` matrix using Metaflow's `@conda` decorator.

## Setup

```bash
conda create -n metaflow -c conda-forge python=3.11 metaflow -y
conda activate metaflow
```

## Run

```bash
CONDA_CHANNELS=conda-forge python flow.py --environment=conda run
```

First run bootstraps 7 conda envs (~45s). Cached after that.

## Output

```
python    numba     llvmlite    jit(x**2)             diff
------------------------------------------------------------
3.10.0    0.61.0    0.44.0      9007199515875289      0
3.11.0    0.61.0    0.44.0      9007199515875288      -1
3.11.0    0.63.0    0.46.0      9007199515875288      -1
3.11.0    0.64.0    0.46.0      9007199515875289      0
3.12.0    0.61.0    0.44.0      9007199515875289      0
3.12.0    0.63.0    0.46.0      9007199515875289      0
3.12.0    0.64.0    0.46.0      9007199515875289      0
```
