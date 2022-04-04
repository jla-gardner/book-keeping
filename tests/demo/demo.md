_2022-04-04 11:59 - demo_

# Summary

```python
dict(
   complete=True,
)
```

# Config

```python
dict(
   N=7,
)
```

# Artefacts

## Plots

![img.svg](img.svg)

## Other

- [log](log)

# Code

```python
from book_keeping import Experiment

experiment = Experiment(root="tests", _id="demo")


@experiment.record
def main(N=10):
    for i in range(N):
        print(f"i = {i}")

    svg = """<?xml version="1.0" standalone="no"?>
<svg width="200" height="200" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="180" height="180"/>
</svg>"""

    with open(experiment.file("img.svg"), "w") as f:
        f.write(svg)

    return dict(complete=True)


def test_demo():
    main(N=7)

```
