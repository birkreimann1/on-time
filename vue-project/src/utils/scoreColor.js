
// Returns a color based on the score value
export function getScoreColor(score) {
  if (score >= 90) {
    return "#397d3b";
  } else if (score >= 75) {
    return "#d9ad1e";
  } else if (score >= 50) {
    return "#b3721d";
  } else if (score >= 1) {
    return "#8f2c25";
  } else {
    return "##ffffff";
  }
}
