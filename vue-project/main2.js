import { createApp } from 'vue';
import './style.css'
import 'leaflet/dist/leaflet.css'
import App from './App.vue';
import { createVueFire, VueFireAuth } from 'vuefire';
import { initializeApp } from 'firebase/app';

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCetbmiUpRv9f1bJUB0EdYj-kiJ9tytXVI",
    authDomain: "ontime-e0281.firebaseapp.com",
    databaseURL: "https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "ontime-e0281",
    storageBucket: "ontime-e0281.firebasestorage.app",
    messagingSenderId: "276717446742",
    appId: "1:276717446742:web:89786f17d2665a1f787df7",
    measurementId: "G-YWZEDZXH81"
  };

const firebaseApp = initializeApp(firebaseConfig);

const vueFire = createVueFire({
  firebaseApp,
  modules: [VueFireAuth()],
});

const app = createApp(App);

app.use(vueFire);
app.mount('#app');
