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
          { text: 'Early Return', link: '/early-return' }
        ]
      },
      {
        text: 'Event-Driven Patterns',
        items: [
          { text: 'Overview', link: '/event-driven-patterns' },
          { text: 'Signal with Start', link: '/signal-with-start' },
          { text: 'Request-Response via Updates', link: '/request-response-via-updates' },
          { text: 'Updatable Timer', link: '/updatable-timer' }
        ]
      },
      {
        text: 'Stateful / Lifecycle Patterns',
        items: [
          { text: 'Overview', link: '/stateful-lifecycle-patterns' },
          { text: 'Continue-As-New', link: '/continue-as-new' },
          { text: 'Child Workflows', link: '/child-workflows' }
        ]
      },
      {
        text: 'Business Process Patterns',
        items: [
          { text: 'Overview', link: '/business-process-patterns' },
          { text: 'Approval', link: '/approval' },
          { text: 'Delayed Start', link: '/delayed-start' }
        ]
      },
      {
        text: 'Long-Running Patterns',
        items: [
          { text: 'Overview', link: '/long-running-patterns' },
          { text: 'Polling External Services', link: '/polling' },
          { text: 'Long Running Activity', link: '/long-running-activity' },
          { text: 'Parallel Execution', link: '/parallel-execution' },
          { text: 'Pick First (Race)', link: '/pick-first' },
          { text: 'Worker-Specific Task Queues', link: '/worker-specific-taskqueue' }
        ]
      },
      {
        text: 'SDK Examples',
        items: [
          { text: 'Java', link: '/java' },
          { text: 'Go', link: '/go' }
        ]
      }
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
