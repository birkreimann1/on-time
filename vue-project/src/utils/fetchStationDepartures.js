import axios from "axios";
import stationIds from "../../../datascraping/stationData/station_ids.json";
import { calculateScore } from "../utils/calculateLineData";


// Fetches the upcoming departures for a station
export const fetchStationDepartures = async (id, stationData) => {

  // API Request using the allorigins api as proxy server
  const url = `https://api.allorigins.win/get?url=https://netzplan.swhl.de/api/v1/stationboards/hafas/${id}?v=0&limit=10`;

  console.log("API Request:", url);
  let stationDeparturesData = [];
  let errorMsg = "";

  try {
    // Send request with axios
    const response = await axios.get(url);
    console.log("API Response:", response);

    // Check if the API response has the expected format
    if (!response.data || !response.data.contents) {
      console.log("No data available from API");
      errorMsg = "Keine Einträge verfügbar!";
      return { stationDeparturesData, errorMsg };
    }

    // Parse the API response string into an json object
    const data = JSON.parse(response.data.contents);
    console.log("Parsed data:", data);

    // Check if the API response was parsed correctly
    if (!data || !data.data) {
      console.log("No data field found in the API response.");
      errorMsg = "Keine Einträge verfügbar!";
      return { stationDeparturesData, errorMsg };
    }
    stationDeparturesData = data.data;
    
    // Get available lines of the station from stationIds.json
    const stationLines = stationIds[id].lines;

    // Map id, score and time left to the station data item
    stationDeparturesData = stationDeparturesData
      .map((item) => {

        // Calculate delay
        const departureTime = item.time * 1000;
        const currentTime = Date.now();
        const timeLeft = Math.max(
          0,
          Math.floor((departureTime - currentTime) / 60000)
        );

        // Check if line is mentioned in stationIds.json
        const line = item.line.name;
        if (!stationLines.includes(line)) {
          return null;
        }
        const line_data = stationData[id].lines[line];

        // Calculate score based on the current enviromental data
        const env_data = stationData[id].env_data;
        const score = calculateScore(line_data, env_data);

        return {
          ...item,
          id,
          score,
          timeLeft,
        };
      })
      // Filter lines not included in stationIds.json
      .filter((item) => item !== null);

    return { stationDeparturesData, errorMsg };

  } catch (error) {
    // When no data could be fetched return an empty departure array
    console.error("Error fetching station data:", error);
    stationDeparturesData = [];
    errorMsg = "Keine Einträge verfügbar!";
    return { stationDeparturesData, errorMsg };
  }
};