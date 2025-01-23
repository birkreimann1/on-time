const calculateMedian = (values) => {
  values.sort((a, b) => a - b);

  const middle = Math.floor(values.length / 2);

  let median;
  if (values.length % 2 === 0) {
    median = (values[middle - 1] + values[middle]) / 2;
  } else {
    median = values[middle];
  }

  return median;
};

export function calculateScore(line_data, criteria = {}) {
  let scores = [];

  const addScoreFromData = (data, criterionKey) => {
    criteria[criterionKey].forEach((criterionValue) => {
      if (data && data[criterionValue] && data[criterionValue].score) {
        scores.push(parseFloat(data[criterionValue].score));
      }
    });
  };

  if (criteria.weather && line_data.weather) {
    addScoreFromData(line_data.weather, "weather");
  }

  if (criteria.traffic && line_data.traffic) {
    addScoreFromData(line_data.traffic, "traffic");
  }

  if (criteria.light && line_data.light) {
    addScoreFromData(line_data.light, "light");
  }

  if (criteria.temp && line_data.temp) {
    addScoreFromData(line_data.temp, "temp");
  }

  if (scores.length === 0) {
    return 0;
  }


  return Math.round(calculateMedian(scores));
}

export function calculateAverageScore(lightData) {
  const score_day = parseFloat(lightData.day.score);
  const size_day = parseFloat(lightData.day.data_size);
  const score_night = parseFloat(lightData.night.score);
  const size_night = parseFloat(lightData.night.data_size);

  if (
    isNaN(score_day) ||
    isNaN(size_day) ||
    isNaN(score_night) ||
    isNaN(size_night)
  ) {
    console.error("Invalid values in light data");
    return 0;
  }

  const average_score = Math.round(
    (score_day * size_day + score_night * size_night) / (size_day + size_night)
  );

  return average_score;
}

export function calculateDelays(line_data, criteria = {}) {
  let dataSize = 0;
  let delayTotal = 0;
  let delays = [];

  const addDataSizeFromData = (data, criterionKey) => {
    criteria[criterionKey].forEach((criterionValue) => {
      if (data && data[criterionValue] && data[criterionValue].data_size) {
        if (!data[criterionValue].data_size == "") {
          dataSize += parseInt(data[criterionValue].data_size); 
        }
      }
      if (data && data[criterionValue] && data[criterionValue].delay_total) {
        if (!data[criterionValue].delay_total == "") {
          delayTotal += parseInt(data[criterionValue].delay_total); 
        }
      }
      if (data && data[criterionValue] && data[criterionValue].average_delay) {
        delays.push(parseFloat(data[criterionValue].average_delay) / 60.0);
      }
    });
  };

  if (criteria.weather && line_data.weather) {
    addDataSizeFromData(line_data.weather, "weather");
  }

  if (criteria.traffic && line_data.traffic) {
    addDataSizeFromData(line_data.traffic, "traffic");
  }

  if (criteria.light && line_data.light) {
    addDataSizeFromData(line_data.light, "light");
  }

  if (criteria.temp && line_data.temp) {
    addDataSizeFromData(line_data.temp, "temp");
  }

  const incidence = parseFloat(delayTotal) / parseFloat(dataSize);
  const average_delay = calculateMedian(delays)
  const expected_delay = incidence * average_delay

  return {
    "size": dataSize, 
    "delays": delayTotal, 
    "incidence": Math.round(100.0 * incidence),
    "average_delay": formatMinutesToMinutesAndSeconds(average_delay),
    "expected_delay": formatMinutesToMinutesAndSeconds(expected_delay)
  };
}

function formatMinutesToMinutesAndSeconds(minutesFloat) {
  const minutes = Math.floor(minutesFloat);
  const seconds = Math.round((minutesFloat - minutes) * 60);
  return `${minutes}:${seconds.toString().padStart(2, '0')} min`;
}