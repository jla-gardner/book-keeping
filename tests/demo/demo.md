_2022-04-04 11:35 - demo_

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
        print(f"{i} = 1")

    svg = """<svg height="100" width="100">
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
</svg>"""

    with open(experiment.file("img.svg"), "w") as f:
        f.write(svg)

    return dict(complete=True)


def test_demo():
    main(N=7)

```
