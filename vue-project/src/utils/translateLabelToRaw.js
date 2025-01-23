// utils.js
export function getRawValue(translatedLabel, category) {
    const displayValues = {
      light: {
        day: "Tag",
        night: "Nacht",
      },
      temp: {
        freezing: "unter 0 °C",
        cool: "0 - 10 °C",
        mild: "10 - 20 °C",
        warm: "20 - 30 °C",
        hot: "über 30 °C",
      },
      traffic: {
        work: "Berufsverkehr",
        offwork: "mittleres Verkehrsaufkommen",
        free: "geringes Verkehrsaufkommen",
      },
      weather: {
        clouds: "Bedeckt",
        sun: "Sonne",
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
  