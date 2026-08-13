import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  title: 'Temporal Agentic Patterns',
  description: 'Catalog of reusable design patterns for Temporal-native AI agents',
  base: process.env.VITEPRESS_BASE ?? '/temporal-agentic-patterns/',
  head: [
    ['meta', { name: 'robots', content: 'noindex, follow' }],
  ],
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'GitHub', link: 'https://github.com/temporal-sa/temporal-agentic-patterns' }
    ],
    sidebar: [
      {
        text: 'Concepts',
        link: '/concepts',
        items: [
          { text: 'Identity', link: '/identity' },
          { text: 'Session, Turn, and Step', link: '/session-turn-step' },
          { text: 'Event Stream', link: '/event-stream' },
          { text: 'Tools and Operations', link: '/tools-and-operations' },
          { text: 'Approvals', link: '/approvals' },
          { text: 'Sandbox and Code Mode', link: '/sandbox-and-code-mode' },
          { text: 'HTTP and Client', link: '/http-and-client' },
          { text: 'Filesystem Authoring', link: '/filesystem-authoring' },
        ]
      },
      {
        text: 'Agent & Session Patterns',
        link: '/agent-session-patterns',
        items: [
          { text: 'Session Workflow', link: '/session-workflow' },
          { text: 'Turn Workflow', link: '/turn-workflow' },
          { text: 'Cancel In-Flight Turn', link: '/cancel-in-flight-turn' },
          { text: 'Session with Signal-and-Start', link: '/session-signal-and-start' },
          { text: 'Eager Interactive Session Start', link: '/eager-interactive-session-start' },
          { text: 'Entity Agent', link: '/entity-agent' },
          { text: 'Session Idle Eviction', link: '/session-idle-eviction' },
          { text: 'Continue-As-New Session', link: '/continue-as-new-session' },
          { text: 'Scheduled Agent Turns', link: '/scheduled-agent-turns' },
          { text: 'Agent Definition Versioning', link: '/agent-definition-versioning' },
          { text: 'Catalog Snapshot Pinning', link: '/catalog-snapshot-pinning' },
          { text: 'Binding Readiness Gate', link: '/binding-readiness-gate' },
          { text: 'Agent Worker Versioning', link: '/agent-worker-versioning' },
          { text: 'Patched Agent Workflow Evolution', link: '/patched-agent-workflow-evolution' },
          { text: 'Operator Session Reset', link: '/operator-session-reset' },
        ]
      },
      {
        text: 'Tool & Model Call Patterns',
        link: '/tool-model-call-patterns',
        items: [
          { text: 'Activity Tool', link: '/activity-tool' },
          { text: 'Workflow Tool', link: '/workflow-tool' },
          { text: 'Callback Tool', link: '/callback-tool' },
          { text: 'Nexus Tool', link: '/nexus-tool' },
          { text: 'Typed Agent Operations', link: '/typed-agent-operations' },
          { text: 'Durable Model Call', link: '/durable-model-call' },
          { text: 'Cached Model Call', link: '/cached-model-call' },
          { text: 'Agent Tool Loop', link: '/agent-tool-loop' },
          { text: 'Structured Model Output', link: '/structured-model-output' },
          { text: 'Provider Retry Delegation', link: '/provider-retry-delegation' },
          { text: 'Model Error Classification', link: '/model-error-classification' },
          { text: 'Rate-Limit Aware Model Calls', link: '/rate-limit-aware-model-calls' },
          { text: 'Model Timeout Profiles', link: '/model-timeout-profiles' },
          { text: 'Tool Retry Profiles', link: '/tool-retry-profiles' },
          { text: 'Poison Tool Quarantine', link: '/poison-tool-quarantine' },
          { text: 'Heartbeat Long Steps', link: '/heartbeat-long-steps' },
          { text: 'Local Activity Tools', link: '/local-activity-tools' },
          { text: 'Fast/Slow Tool Retries', link: '/fast-slow-tool-retries' },
          { text: 'External Tool Polling', link: '/external-tool-polling' },
          { text: 'Tool Compensation', link: '/tool-compensation' },
          { text: 'Prompt Versioning', link: '/prompt-versioning' },
          { text: 'Prompt Experiment Pins', link: '/prompt-experiment-pins' },
        ]
      },
      {
        text: 'Human-in-the-loop Patterns',
        link: '/human-in-the-loop-patterns',
        items: [
          { text: 'Approval-Gated Tools', link: '/approval-gated-tools' },
          { text: 'Ask-User Wait', link: '/ask-user-wait' },
          { text: 'Connection Auth Wait', link: '/connection-auth-wait' },
          { text: 'Session-Scoped Approvals', link: '/session-scoped-approvals' },
          { text: 'Updatable Approval Timer', link: '/updatable-approval-timer' },
          { text: 'Resumable Correction', link: '/resumable-correction' },
          { text: 'Operator Slash Commands', link: '/operator-slash-commands' },
        ]
      },
      {
        text: 'Subagent & Multi-agent Patterns',
        link: '/subagent-patterns',
        items: [
          { text: 'Subagent Toolset', link: '/subagent-toolset' },
          { text: 'Persistent Subagent Threads', link: '/persistent-subagent-threads' },
          { text: 'Fan-Out Subagents', link: '/fanout-subagents' },
          { text: 'Best-Effort Parallel Tools', link: '/best-effort-parallel-tools' },
          { text: 'Remote Subagent', link: '/remote-subagent' },
        ]
      },
      {
        text: 'Code Mode & Sandbox Patterns',
        link: '/code-mode-patterns',
        items: [
          { text: 'Code Mode Orchestrator', link: '/code-mode-orchestrator' },
          { text: 'Tools-Only Sandbox', link: '/tools-only-sandbox' },
          { text: 'Type-Checked Scripts', link: '/type-checked-scripts' },
          { text: 'Script Fan-Out', link: '/script-fan-out' },
          { text: 'Sticky Sandbox Task Queues', link: '/sticky-sandbox-task-queues' },
        ]
      },
      {
        text: 'Safety & Security Patterns',
        link: '/safety-security-patterns',
        items: [
          { text: 'Safety-Profiled Tools', link: '/safety-profiled-tools' },
          { text: 'Guardrail Steps', link: '/guardrail-steps' },
          { text: 'Security Profiles per Agent', link: '/security-profiles-per-agent' },
          { text: 'Network & Resource Sandboxing', link: '/network-resource-sandboxing' },
          { text: 'Split Resume and Observe Handles', link: '/split-resume-observe-handles' },
          { text: 'Delivery Authorization Timing', link: '/delivery-authorization-timing' },
        ]
      },
      {
        text: 'Memory & State Patterns',
        link: '/memory-state-patterns',
        items: [
          { text: 'Session Memory', link: '/session-memory' },
          { text: 'Context Compaction', link: '/context-compaction' },
          { text: 'Cross-Session Memory', link: '/cross-session-memory' },
          { text: 'Externalized Memory', link: '/externalized-memory' },
          { text: 'Claim-Check Payloads', link: '/claim-check-payloads' },
        ]
      },
      {
        text: 'Observability & Operations Patterns',
        link: '/observability-patterns',
        items: [
          { text: 'Standardized Event Stream', link: '/standardized-event-stream' },
          { text: 'Progress Streaming', link: '/progress-streaming' },
          { text: 'Agent Tracing', link: '/agent-tracing' },
          { text: 'Session Visibility Attributes', link: '/session-visibility-attributes' },
          { text: 'Cost & Token Accounting', link: '/cost-token-accounting' },
          { text: 'Session Spend Caps', link: '/session-spend-caps' },
          { text: 'Agent Step Retry Alerting', link: '/agent-step-retry-alerting' },
          { text: 'Eval-Backed Behavior Checks', link: '/eval-backed-behavior-checks' },
        ]
      },
      {
        text: 'QoS & Throughput Patterns',
        link: '/qos-throughput-patterns',
        items: [
          { text: 'Fairness', link: '/fairness' },
          { text: 'Priority Task Queues', link: '/priority-task-queues' },
          { text: 'Downstream Tool Rate Limiting', link: '/downstream-tool-rate-limiting' },
        ]
      },
      {
        text: 'Channel & Integration Patterns',
        link: '/channel-integration-patterns',
        items: [
          { text: 'HTTP Channel Agent', link: '/http-channel-agent' },
          { text: 'Messaging Channel Agent', link: '/messaging-channel-agent' },
          { text: 'Idempotent Delivery', link: '/idempotent-delivery' },
          { text: 'Validated Session Ingress', link: '/validated-session-ingress' },
          { text: 'Split Resume and Observe Handles', link: '/split-resume-observe-handles' },
          { text: 'Delivery Authorization Timing', link: '/delivery-authorization-timing' },
          { text: 'Connection Auth Wait', link: '/connection-auth-wait' },
          { text: 'MCP / OpenAPI Tooling', link: '/mcp-openapi-tooling' },
        ]
      },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/temporal-sa/temporal-agentic-patterns' }
    ],
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Temporal Agentic Patterns Catalog'
    }
  },
  mermaid: {},
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8787',
          changeOrigin: true,
        },
      },
    },
  },
}))
