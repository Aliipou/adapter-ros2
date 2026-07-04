"""Decision OS execution adapter for ROS 2 / robotics. EXPERIMENTAL.

Provides governed tools for ROS 2 / robotics. Each tool is the effect BEHIND the PEP: it
runs only when the kernel permits the action. The bodies are honest stubs — wire
the real ROS 2 / robotics SDK where marked. This adapter holds NO authority and never
bypasses the kernel; `governed_tools(governor)` wraps the tools so every call is
authorized + audited.
"""

from __future__ import annotations

from typing import Any


def move_arm(x, y, z, speed) -> str:
    # TODO: wire the real ROS 2 / robotics SDK here. Until then, an honest stub.
    return f"[ros2] move arm -> ({x},{y},{z}) @ {speed}m/s"


def actuate_gripper(state) -> str:
    # TODO: wire the real ROS 2 / robotics SDK here. Until then, an honest stub.
    return f"[ros2] gripper -> {state}"


# The tool registry + per-tool capability specs (capability = "tool:<name>").
TOOLS = {"move_arm": move_arm, "actuate_gripper": actuate_gripper}
SPECS: dict[str, dict[str, Any]] = {
    "move_arm": {"capability": "tool:move_arm"},
    "actuate_gripper": {"capability": "tool:actuate_gripper"},
}


def governed_tools(governor: Any) -> dict[str, Any]:
    """Wrap this adapter's tools with a decision_os_min.Governor so every call is
    routed through the kernel. Returns the governed tool registry."""
    return governor.wrap(TOOLS, specs=SPECS)
