# adapter-ros2 — EXPERIMENTAL execution adapter (ROS 2 / robotics)

A **separate, experimental** consumer of `decision-os-min`. It exposes ROS 2 / robotics
actions as **governed tools**: each tool is the effect *behind* the Policy
Enforcement Point, reached only when the kernel permits the action.

```python
from decision_os_min import Governor, set_actor
from dos_adapter_ros2 import governed_tools

gov = Governor(policy, audit_path="audit.jsonl")
tools = governed_tools(gov)          # every ROS 2 / robotics call now authorized + audited
set_actor("agent:ops")
tools["move_arm"](...)                # runs only if the kernel says ALLOW
```

**Status: EXPERIMENTAL / INTERFACE-ONLY.** The tool bodies are honest stubs — wire
the real ROS 2 / robotics SDK where marked. This adapter holds **no authority** and never
bypasses the kernel. It is a separate repo so the core stays small and frozen.
