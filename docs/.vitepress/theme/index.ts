import DefaultTheme from 'vitepress/theme'
import './custom.css'
import DaytonaRunner from './components/DaytonaRunner.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('DaytonaRunner', DaytonaRunner)
  },
}
