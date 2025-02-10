
// Calculates average score for a station based on the night and day values
export function calculateAverageScore(lightData) {

  // Setup
  const { day, night } = lightData;
  const score_day = parseFloat(day.score);
  const size_day = parseFloat(day.data_size);
  const score_night = parseFloat(night.score);
  const size_night = parseFloat(night.data_size);

  // Check that all included values exist
  if ([score_day, size_day, score_night, size_night].some(isNaN)) {
    console.error("Invalid values in light data");
    return 0;
  }

  // Calculates mean value
  const totalScore = score_day * size_day + score_night * size_night;
  const totalSize = size_day + size_night;
  
  return Math.round(totalScore / totalSize);
}


// Calculates median of all values in the given array
const calculateMedian = (values) => {

  // Check if values contains data
  if (values.length === 0) return 0;
  
  // Sort the array in ascending order
  values.sort((a, b) => a - b);
  
  // Return the mean value
  const middle = Math.floor(values.length / 2);
  return values.length % 2 === 0
    ? (values[middle - 1] + values[middle]) / 2
    : values[middle];
};


// Returns line_data entry based on the the given keys
const extractDataValues = (line_data, criteria, key, callback) => {
  if (criteria[key] && line_data[key]) {
    criteria[key].forEach((criterionValue) => {
      const dataItem = line_data[key][criterionValue];
      if (dataItem) {
        callback(dataItem);
      }
    });
  }
};


// Calculates score based on the given enviromental values
export function calculateScore(line_data, criteria = {}) {
  const scores = [];

  // Pushes score to array
  const addScore = (data) => {
    if (data && data.score) {
      scores.push(parseFloat(data.score));
    }
  };

  // Extract scores for the given enviroment
  ['weather', 'traffic', 'light', 'temp'].forEach((condition) => {
    extractDataValues(line_data, criteria, condition, addScore);
  });

  // Returns mean value of all extracted scores
  return scores.length ? Math.round(calculateMedian(scores)) : 0;
}


// Gets the delay data for the given enviroment criteria
function getDelayDataForCriteria(line_data, criteria) {
  // Setup
  let dataSize = 0;
  let delayTotal = 0;
  let delays = [];

  // Stores number of delays and data entries aswell as delay data
  const addData = (data) => {
    if (data.data_size) {
      dataSize += parseInt(data.data_size);
    }
    if (data.delay_total) {
      delayTotal += parseInt(data.delay_total);
    }
    if (data.average_delay) {
      delays.push(parseFloat(data.average_delay) / 60.0);
    }
  };

  // Extract delays for the given enviroment
  ['weather', 'traffic', 'light', 'temp'].forEach((condition) => {
    extractDataValues(line_data, criteria, condition, addData);
  });

  // Return the data as an object
  return { dataSize, delayTotal, delays };
}


// Calculates delay data based on the given enviroment criteria
export function calculateDelayData(line_data, criteria = {}) {

  // Gets the delay data for the given enviroment criteria 
  const { dataSize, delayTotal, delays } = getDelayDataForCriteria(line_data, criteria);

  // Calculates abstracted values for delay data
  const incidence = dataSize ? delayTotal / dataSize : 0;
  const incidence_return = isNaN(incidence) ? "N/A" : `${Math.round(100 * incidence)} %`;
  const average_delay = calculateMedian(delays);
  const expected_delay = incidence * average_delay;

  return {
    size: dataSize,
    delays: delayTotal,
    incidence: incidence_return,
    average_delay: formatTime(average_delay),
    expected_delay: formatTime(expected_delay),
  };
}


// Outputs the summed delay size based on the given delay type and the set enviroment
function getDelayByEnv(lineData, env, delayType) {
  let delaySize = 0;

  // Adds number of delay occurrences to delaySize
  const addData = (data) => {
    const delayValue = data.delay_info[delayType];
    if (delayValue) {
      delaySize += parseInt(delayValue);
    }
  };

  // Extract delay information of given delay type based on the environment conditions
  ['weather', 'traffic', 'light', 'temp'].forEach((condition) => {
    if (env[condition]) {
      env[condition].forEach((criterionValue) => {
        if (lineData[condition][criterionValue]) {
          addData(lineData[condition][criterionValue]);
        }
      });
    }
  });

  return delaySize;
}


// Returns delay array for bar graph 
export function fillChartArr(line_data_value, data_sizes_value, env) {

  // Setup
  let chartArr = [];
  const size = data_sizes_value.size;
  const delays = data_sizes_value.delays
  const delayTypes = ["short", "medium", "long", "extreme", "cancelled"];

  // Push empty array when no data is available
  if (size === 0) {
    chartArr.push(0, 0, 0, 0, 0, 0);
    return chartArr
  } 

  // Push number of punctual departures into the array
  chartArr.push(Math.round((100 * (size - delays)) / size));

  // Push number of delays & cancelled departures into the array
  delayTypes.forEach((delayType, index) => {
    const data = getDelayByEnv(line_data_value, env, delayType)
    chartArr.push(Math.round((100 * data) / size));
  });

  return chartArr;
}


// Returns time in format (min:sec)
function formatTime(minutesFloat) {
  if (isNaN(minutesFloat)) {
    return "N/A";
  }

  const minutes = Math.floor(minutesFloat);
  const seconds = Math.round((minutesFloat - minutes) * 60);
  return `${minutes}:${seconds.toString().padStart(2, "0")} min`;
}
