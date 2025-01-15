// Import the Firestore db instance from firebase-config.js
import { db } from './firebase-config.js';

const stationSelect = document.getElementById('stationSelect');
const departureList = document.getElementById('departureTimes');

// Function to load stations
function loadStations() {
  const stationsRef = db.collection('stations');
  stationsRef.get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
      const station = doc.data();
      const option = document.createElement('option');
      option.value = doc.id;
      option.textContent = station.name;
      stationSelect.appendChild(option);
    });
  });
}

// Function to fetch and display departures
function getDepartures() {
  const stationId = stationSelect.value;
  if (!stationId) return;

  departureList.innerHTML = ''; // Clear previous departures

  const departuresRef = db.collection('stations').doc(stationId).collection('departures');
  departuresRef.orderBy('time').limit(5).get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
      const departure = doc.data();
      const listItem = document.createElement('li');
      listItem.textContent = `${departure.time} - Bus ${departure.busNumber} to ${departure.destination}`;
      departureList.appendChild(listItem);
    });
  });
}

// Load stations when the page loads
loadStations();

// Add event listener for station selection
stationSelect.addEventListener('change', getDepartures);
