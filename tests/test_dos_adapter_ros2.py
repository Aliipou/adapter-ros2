import pytest
from decision_os_min import Governor, GovernanceRefused, set_actor

from dos_adapter_ros2 import SPECS, TOOLS, governed_tools

_ANY = next(iter(TOOLS))                       # some tool name from this adapter
POLICY = {"grants": {"agent:ops": [f"tool:{_ANY}"]}, "default": "deny"}


def _gov(tmp_path):
    return Governor(POLICY, audit_path=str(tmp_path / "a.jsonl"))


def test_permitted_tool_reaches_the_actuator(tmp_path):
    tools = governed_tools(_gov(tmp_path))
    set_actor("agent:ops")
    out = tools[_ANY](**{k.split("=")[0].strip(): 1 for k in _sample_args(_ANY)})
    assert isinstance(out, str)                # the stub effect ran


def test_unauthorized_actor_never_reaches_the_actuator(tmp_path):
    tools = governed_tools(_gov(tmp_path))
    set_actor("agent:intruder")                # no grants
    with pytest.raises(GovernanceRefused):
        tools[_ANY](**{k.split("=")[0].strip(): 1 for k in _sample_args(_ANY)})


def _sample_args(name):
    # crude arg discovery for the smoke test
    import inspect
    from dos_adapter_ros2 import __dict__ as d
    return [p for p in inspect.signature(d[name]).parameters]
