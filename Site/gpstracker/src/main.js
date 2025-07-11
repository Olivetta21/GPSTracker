import { createApp } from 'vue'
import App from './App.vue'
import router from './scripts/routes/router'

const app = createApp(App);

app.use(router).mount('#app');
