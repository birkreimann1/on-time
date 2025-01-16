import { createApp } from 'vue';
import { VueFire } from "vuefire";
import { initializeApp } from "firebase/app";
import App from "./App.vue";
import './style.css'
import 'leaflet/dist/leaflet.css'

export const firebaseApp = initializeApp({
    apiKey: "AIzaSyCetbmiUpRv9f1bJUB0EdYj-kiJ9tytXVI",
    authDomain: "ontime-e0281.firebaseapp.com",
    databaseURL: "https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "ontime-e0281",
    storageBucket: "ontime-e0281.firebasestorage.app",
    messagingSenderId: "276717446742",
    appId: "1:276717446742:web:89786f17d2665a1f787df7",
    measurementId: "G-YWZEDZXH81"
  });

const app = createApp(App);

// install the VueFire plugin
app.use(VueFire, { firebaseApp });

app.mount("#app");
