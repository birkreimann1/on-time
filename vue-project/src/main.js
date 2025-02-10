// External imports
import "./style.css";
import "leaflet/dist/leaflet.css";
import { createApp } from "vue";
import { VueFire } from "vuefire";
import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs } from "firebase/firestore";
import stationIds from '../../station_data/station_ids.json';

// Imports from project
import App from "./App.vue";
import router from "./router";

// Initialisation of the firebase app
export const firebaseApp = initializeApp({
  apiKey: "AIzaSyCetbmiUpRv9f1bJUB0EdYj-kiJ9tytXVI",
  authDomain: "ontime-e0281.firebaseapp.com",
  databaseURL:
    "https://ontime-e0281-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "ontime-e0281",
  storageBucket: "ontime-e0281.firebasestorage.app",
  messagingSenderId: "276717446742",
  appId: "1:276717446742:web:89786f17d2665a1f787df7",
  measurementId: "G-YWZEDZXH81",
});


// // Initialize Firestore
// const db = getFirestore(firebaseApp);

// // Fetch a document from Firestore
// const fetchStationsFromFirestore = async () => {
//   const stationsCollection = collection(db, "stations");
//   try {
//     const stationsSnapshot = await getDocs(stationsCollection);
//     const stationsObject = {};
//     stationsSnapshot.docs.forEach((doc) => {
//       stationsObject[doc.id] = doc.data();
//     });
//     window.stationIds = stationsObject;
//     console.log("Stations:", stationsObject);
//   } catch (error) {
//     console.error("Error fetching stations:", error);
//   }
// };

// // Fetch stationIds from the Firestore
// fetchStationsFromFirestore();

// App setup
const app = createApp(App);
app.use(VueFire, { firebaseApp });
app.use(router);
app.mount("#app");

// Make the stationsIds available for the session
window.stationIds = stationIds

// Exports to use inside the project
export { };
