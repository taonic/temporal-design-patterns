import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  title: 'Temporal Patterns',
  description: 'Common catalog of reusable patterns for Temporal workflows',
  base: '/temporal-design-patterns/',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'GitHub', link: 'https://github.com/taonic/temporal-design-patterns' }
    ],
    sidebar: [
      {
        text: 'Distributed Transaction Patterns',
        items: [
          { text: 'Overview', link: '/distributed-transaction-patterns' },
          { text: 'Saga Pattern', link: '/saga-pattern' },
          { text: 'Early Return', link: '/early-return' },
          { text: 'Idempotent Distributed Transactions', link: '/idempotent-distributed-transactions' }
        ]
      },
      {
        text: 'Entity & Lifecycle Patterns',
        items: [
          { text: 'Overview', link: '/entity-lifecycle-patterns' },
          { text: 'Entity Workflow', link: '/entity-workflow' },
          { text: 'Continue-As-New', link: '/continue-as-new' },
          { text: 'Updatable Timer', link: '/updatable-timer' }
        ]
      },
      {
        text: 'Workflow Messaging Patterns',
        items: [
          { text: 'Overview', link: '/workflow-messaging-patterns' },
          { text: 'Signal with Start', link: '/signal-with-start' },
          { text: 'Request-Response via Updates', link: '/request-response-via-updates' }
        ]
      },
      {
        text: 'Task Orchestration Patterns',
        items: [
          { text: 'Overview', link: '/task-orchestration-patterns' },
          { text: 'Child Workflows', link: '/child-workflows' },
          { text: 'Parallel Execution', link: '/parallel-execution' },
          { text: 'Pick First (Race)', link: '/pick-first' }
        ]
      },
      {
        text: 'External Interaction Patterns',
        items: [
          { text: 'Overview', link: '/external-interaction-patterns' },
          { text: 'Polling External Services', link: '/polling' },
          { text: 'Long Running Activity', link: '/long-running-activity' },
          { text: 'Approval', link: '/approval' },
          { text: 'Delayed Start', link: '/delayed-start' }
        ]
      },
      {
        text: 'Worker Configuration Patterns',
        items: [
          { text: 'Overview', link: '/worker-configuration-patterns' },
          { text: 'Worker-Specific Task Queues', link: '/worker-specific-taskqueue' },
          { text: 'Activity Dependency Injection', link: '/activity-dependency-injection' }
        ]
      },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/taonic/temporal-design-patterns' }
    ],
    search: {
      provider: 'local'
    },
    footer: {
      message: 'Temporal Design Patterns Catalog'
    }
  },
  mermaid: {}
}))
