import functools
import inspect
import os
from datetime import datetime
from pathlib import Path

import __main__

from book_keeping.ids import random_id
from book_keeping.tee import stdout_to_
from book_keeping.util import apply, dual_filter, is_img, markdown_expand, markdown_link, markdown_list


__ME = Path(__file__)


def all_files(p):
    for path, _, files in os.walk(p):
        rel_path = Path(path).relative_to(p)
        for name in files:
            yield rel_path / name


def pretty_dict(_dict):
    max_k = max(len(k) for k in _dict.keys())
    pretty = "dict(\n"
    for k, v in _dict.items():
        pretty += f"   {k: >{max_k}}={str(v).strip()},\n"
    return pretty + ")"


def generate_report(_id, summary, config, artefacts, _file):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(_file, "r") as f:
        code = f.read()

    plots, artefacts = dual_filter(is_img, artefacts)

    plots = "\n".join(apply(markdown_expand, plots))
    artefacts = markdown_list(apply(markdown_link, artefacts))

    with open(__ME.parent / "template.md", "r") as f:
        template = f.read()

    return template.format(
        now=now, title=_id, summary=pretty_dict(summary),
        config=pretty_dict(config), plots=plots, artefacts=artefacts, code=code
    )


class Experiment:
    def __init__(self, root="experiments", project=None):
        _dir = Path(root) / (project if project else "")
        self._id = random_id()
        while (_dir / self._id).exists():
            self._id = random_id()
        self._dir = _dir / self._id
        self._dir.mkdir(exist_ok=False, parents=True)
        self._file = inspect.stack()[1].filename

    def file(self, name: str):
        return self._dir / name

    def record(self, func):
        @functools.wraps(func)
        def wrapper(*args, **config):
            with stdout_to_(self.file("log")):
                print(f"Starting Experiment: {self._id}")
                summary = func(*args, **config)
                artefacts = [*all_files(self._dir)]
                report = generate_report(
                    self._id, summary, config, artefacts, self._file)
            with open(self.file(f"{self._id}.md"), "w") as f:
                f.write(report)
        return wrapper
