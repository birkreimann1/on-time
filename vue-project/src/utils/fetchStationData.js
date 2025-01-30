import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";

// Fetch collected data for all stations from the Firebase realtime database
export const fetchStationData = async (stationData) => {
  const db = getDatabase();

  // Define the database entries to be fetched
  const stationsRef = dbRef(db, "stations_new_score");

  try {
    const snapshot = await dbGet(stationsRef);
    if (snapshot.exists()) {
      const stationsData = snapshot.val();
      stationData.value = {};

      // White the fetched data into the variable stationsData
      for (const id in stationsData) {
        if (stationsData.hasOwnProperty(id)) {
          const station = stationsData[id];
          stationData.value[id] = station;
        }
      }

    } else {
      console.log("No data available");
    }
  } catch (error) {
    console.error("Error fetching data from Firebase:", error);
  }
};