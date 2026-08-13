from temporalio import workflow


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._commands: list[str] = []
        self._stop = False
        self._policy = "strict"

    @workflow.signal
    def slash(self, command: str) -> None:
        self._commands.append(command)
        if command.startswith("/approvals "):
            self._policy = command.split(" ", 1)[1]
        elif command == "/stop":
            self._stop = True

    @workflow.query
    def status(self) -> str:
        return f"policy={self._policy};commands={len(self._commands)}"

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        await workflow.wait_condition(lambda: self._stop or len(self._commands) > 0)
        if not self._stop:
            # Auto-stop after first command so the sample completes.
            self._stop = True
        return f"slash_command_invoked:{self._commands[-1]}:{self._policy}"
