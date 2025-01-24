// utils.js
export function getRawValue(translatedLabel, category) {
    const displayValues = {
      light: {
        null: "Keine Auswahl",
        day: "Tag",
        night: "Nacht",
      },
      temp: {
        null: "Keine Auswahl",
        freezing: "unter 0 °C",
        cool: "0 - 10 °C",
        mild: "10 - 20 °C",
        warm: "20 - 30 °C",
        hot: "über 30 °C",
      },
      traffic: {
        null: "Keine Auswahl",
        work: "Berufsverkehr",
        free: "Freizeitverkehr",
        offwork: "Ruhiger Verkehr",
      },
      weather: {
        null: "Keine Auswahl",
        clear: "Klar",
        clouds: "Bedeckt",
        rain: "Regen",
        fog: "Nebel",
        snow: "Schnee",
        thunderstorm: "Gewitter",
        storm: "Sturm",
      },
    };
  
    // Get the category data
    const categoryData = displayValues[category];
  
    // Reverse the category data: map translated values to raw values
    for (const rawValue in categoryData) {
      if (categoryData[rawValue] === translatedLabel) {
        return rawValue;
      }
    }
  
    // Return null if no match is found
    return null;
  }
  