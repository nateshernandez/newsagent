"""Hooks for the News Scout agent."""

from typing import Any

from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry

EXA_TOOL_SUFFIX = "_exa"


def _is_exa_tool(tool_name: str) -> bool:
    return tool_name.endswith(EXA_TOOL_SUFFIX)


class ExaApprovalHook(HookProvider):
    def __init__(self, app_name: str = "newsagent") -> None:
        self.app_name = app_name

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        registry.add_callback(BeforeToolCallEvent, self._approve_exa_tool)

    def _approve_exa_tool(self, event: BeforeToolCallEvent) -> None:
        tool_name = event.tool_use["name"]

        if not _is_exa_tool(tool_name):
            return

        tool_input = event.tool_use.get("input", {})

        approval = event.interrupt(
            f"{self.app_name}-exa-approval",
            reason={"tool": tool_name, "input": tool_input},
        )

        if approval and str(approval).lower() not in ("y", "yes"):
            event.cancel_tool = "User denied permission to run Exa tool"
