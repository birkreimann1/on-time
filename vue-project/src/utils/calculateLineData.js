
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
    addScoreFromData(line_data.weather, 'weather');
  }

  if (criteria.traffic && line_data.traffic) {
    addScoreFromData(line_data.traffic, 'traffic');
  }

  if (criteria.light && line_data.light) {
    addScoreFromData(line_data.light, 'light');
  }

  if (criteria.temp && line_data.temp) {
    addScoreFromData(line_data.temp, 'temp');
  }

  if (scores.length === 0) {
    return 0;
  }

  const calculateMedian = (scores) => {
    scores.sort((a, b) => a - b);

    const middle = Math.floor(scores.length / 2);
    
    let median;
    if (scores.length % 2 === 0) {
      median = (scores[middle - 1] + scores[middle]) / 2;
    } else {
      median = scores[middle];
    }

    console.log(scores)
    return Math.round(median);
  };

  return calculateMedian(scores);
}


  
export function calculateAverageScore(lightData) {

  const score_day = parseFloat(lightData.day.score);
  const size_day = parseFloat(lightData.day.data_size);
  const score_night = parseFloat(lightData.night.score);
  const size_night = parseFloat(lightData.night.data_size);

  if (isNaN(score_day) || isNaN(size_day) || isNaN(score_night) || isNaN(size_night)) {
    console.error("Invalid values in light data");
    return 0;
  }

  const average_score = Math.round((score_day * size_day + score_night * size_night) / (size_day + size_night));

  return average_score;
}