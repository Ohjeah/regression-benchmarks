import os
import subprocess
from pathlib import Path

import pytest


examples = Path(__file__).parent.glob("../example/*.py")


@pytest.mark.parametrize("pypath", examples)
def test_examples(pypath):
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    p = subprocess.Popen(["python", pypath], env=env)
    assert p.wait() == 0  # SUCCESS==0
