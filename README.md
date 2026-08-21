# adapter-ros2

**Live (graph):** [https://ali-adapter-ros2.vercel.app](https://ali-adapter-ros2.vercel.app)

Decision OS / AuthGate **execution adapter** for ROS 2 / robotics actuation. It
exposes robot actions as **governed tools**: each tool is the effect *behind* a
Policy Enforcement Point and runs only when the `decision-os-min` kernel
authorizes the action. The adapter holds **no authority** of its own and never
bypasses the kernel — every call is authorized and audited.

> Part of the Decision OS — governed by the Legitimacy ⊥ Authority pipeline
> (FDK legitimacy → AuthGate authority). Adapters adapt tools into governed
> effects and hold **no authority** of their own.

## What it adapts

| Tool | Capability | Effect |
|------|------------|--------|
| `move_arm` | `tool:move_arm` | Move an arm to (x, y, z) at a speed |
| `actuate_gripper` | `tool:actuate_gripper` | Open/close the gripper |

## Install

```bash
pip install -e .          # brings in decision-os-min
# for development:
pip install -e ".[dev]"   # + pytest, ruff, mypy
```

## Usage

```python
from decision_os_min import Governor, set_actor
from dos_adapter_ros2 import governed_tools

policy = {"grants": {"agent:ops": ["tool:move_arm"]}, "default": "deny"}
gov = Governor(policy, audit_path="audit.jsonl")
tools = governed_tools(gov)

set_actor("agent:ops")
tools["move_arm"](0.1, 0.2, 0.3, speed=0.05)   # runs only if the kernel ALLOWs
```

An actor without the matching grant raises `GovernanceRefused` before the effect
runs.

## Status & limitations

**Experimental / interface-only.** The tool bodies are honest stubs that return a
string describing the intended effect — they do **not** publish to real ROS 2
topics/actions (`rclpy`) yet. Wire the real ROS 2 client at the `# TODO` markers
in `dos_adapter_ros2/__init__.py`. What is real today is the governance wiring:
the capability→tool mapping and the fail-closed authorization boundary.

**Safety note:** this adapter is a policy gate for command dispatch, not a safety
controller. It does not provide collision checking, e-stop, joint-limit
enforcement, or real-time guarantees. Do not place it in a control loop where a
missed or delayed authorization could cause unsafe motion. Reference software —
review and test before any real hardware use.

## License

PolyForm Noncommercial 1.0.0 (see `LICENSE`).
