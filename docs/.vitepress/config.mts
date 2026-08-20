import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  title: 'Temporal Patterns',
  description: 'Common catalog of reusable patterns for Temporal workflows',
  base: process.env.VITEPRESS_BASE ?? '/temporal-design-patterns/',
  head: [
    ['meta', { name: 'robots', content: 'noindex, follow' }],
    // Google tag (gtag.js)
    ['script', { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=G-KCHNTGYY7N' }],
    ['script', {}, `window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-KCHNTGYY7N');`]
  ],
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'GitHub', link: 'https://github.com/taonic/temporal-design-patterns' }
    ],
    sidebar: [
      {
        text: 'Task Orchestration Patterns',
        link: '/task-orchestration-patterns',
        items: [
          { text: 'Child Workflows', link: '/child-workflows' },
          { text: 'Parallel Execution', link: '/parallel-execution' },
          { text: 'Pick First (Race)', link: '/pick-first' }
        ]
      },
      {
        text: 'Workflow Messaging Patterns',
        link: '/workflow-messaging-patterns',
        items: [
          { text: 'Signal with Start', link: '/signal-with-start' },
          { text: 'Request-Response via Updates', link: '/request-response-via-updates' },
          { text: 'Event Accumulator', link: '/event-accumulator' }
        ]
      },
      {
        text: 'Entity & Lifecycle Patterns',
        link: '/entity-lifecycle-patterns',
        items: [
          { text: 'Entity Workflow', link: '/entity-workflow' },
          { text: 'Continue-As-New', link: '/continue-as-new' },
          { text: 'Updatable Timer', link: '/updatable-timer' }
        ]
      },
      {
        text: 'External Interaction Patterns',
        link: '/external-interaction-patterns',
        items: [
          { text: 'Polling External Services', link: '/polling' },
          { text: 'Long Running Activity', link: '/long-running-activity' },
          { text: 'Kafka Consumption', link: '/kafka-consumption' },
          { text: 'Delayed Start', link: '/delayed-start' },
          { text: 'Delayed Callback', link: '/delayed-callback' },
          { text: 'Approval', link: '/approval' }
        ]
      },
      {
        text: 'Distributed Transaction Patterns',
        link: '/distributed-transaction-patterns',
        items: [
          { text: 'Saga Pattern', link: '/saga-pattern' },
          { text: 'Early Return', link: '/early-return' }
        ]
      },
      {
        text: 'Error Handling & Retry Patterns',
        link: '/error-handling-patterns',
        items: [
          { text: 'Fixed Count of Retries', link: '/fixed-count-retries' },
          { text: 'Fixed Wall-Time Retries', link: '/fixed-wall-time-retries' },
          { text: 'Non-Retryable Errors', link: '/non-retryable-errors' },
          { text: 'Delayed Retry', link: '/delayed-retry' },
          { text: 'Fast/Slow Retries', link: '/fast-slow-retries' },
          { text: 'Retry Alerting via Metrics', link: '/retry-metrics' },
          { text: 'Resumable Activity', link: '/resumable-activity' }
        ]
      },
      {
        text: 'Batch Processing Patterns',
        link: '/batch-processing-patterns',
        items: [
          { text: 'Fan-Out with Child Workflows', link: '/fanout-child-workflows' },
          { text: 'Batch Iterator', link: '/batch-iterator' },
          { text: 'Sliding Window', link: '/sliding-window' },
          { text: 'MapReduce Tree', link: '/mapreduce-tree' }
        ]
      },
      {
        text: 'QoS & Throughput Patterns',
        link: '/qos-throughput-patterns',
        items: [
          { text: 'Downstream Rate Limiting', link: '/downstream-rate-limiting' },
          { text: 'Priority Task Queues', link: '/priority-task-queues' },
          { text: 'Fairness', link: '/fairness' }
        ]
      },
      {
        text: 'Performance & Latency Patterns',
        link: '/performance-latency-patterns',
        items: [
          { text: 'Local Activities', link: '/local-activities' },
          { text: 'Early Return + Local Activities', link: '/early-return-local-activities' },
          { text: 'Eager Workflow Start', link: '/eager-workflow-start' }
        ]
      },
      {
        text: 'Worker Configuration Patterns',
        link: '/worker-configuration-patterns',
        items: [
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
