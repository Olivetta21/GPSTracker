import { createApp } from 'vue'
import App from './App.vue'
import router from './scripts/routes/router'

const app = createApp(App);

router.beforeEach((to, from, next) => {
    to.meta?.classe?.beforeOpen();
    from.meta?.classe?.beforeClose();
    next();
    to.meta?.classe?.afterOpen();
    from.meta?.classe?.afterClose();
});

app.use(router).mount('#app');
