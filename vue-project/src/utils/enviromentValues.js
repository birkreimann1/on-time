// Internal and display values for every available enviromental data
export const envValues = {
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
    storm: "Sturm",
    thunderstorm: "Gewitter",
  },
};

// Returns all available items of a category
export function getAvailableItems(label) {
  return Object.keys(envValues[label] || {}).map(
    (key) => envValues[label][key]
  );
}

// Returns the display value of an enviroment item
export function getDisplayValue(rawValue, label) {
  return envValues[label][rawValue] || rawValue;
}

// Returns the internal value of an enviroment item
export function getRawValue(label, category) {
  const categoryData = envValues[category];
  
  for (const rawValue in categoryData) {
    if (categoryData[rawValue] === label) {
      return rawValue;
    }
  }

  return null;
}
