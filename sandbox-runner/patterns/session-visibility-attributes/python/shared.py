from temporalio.common import SearchAttributeKey

TASK_QUEUE = "agentic-session-visibility"
TURN_STATUS = SearchAttributeKey.for_keyword("AgentTurnStatus")
TENANT_ID = SearchAttributeKey.for_keyword("AgentTenantId")
