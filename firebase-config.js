// Import the functions you need from the Firebase SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAnalytics } from "firebase/analytics";

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

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Analytics (optional)
const analytics = getAnalytics(app);

// Initialize Firestore (you can use it later for querying)
const db = getFirestore(app);

export { db };  // Export db to use in the main logic
