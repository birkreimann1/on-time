<template>
  <div>
    <ul>
      <p>Diese Scores ergeben sich aus der gewichteten Verspätungsrate, wobei geringere Verspätungen das Ergebnis weniger stark beeinflussen als längere.</p>
      <p>Der Main Score wird darüber hinaus über die jeweiligen Werte aller derzeit eingestellten Umweltfaktoren gemittelt.</p>
    </ul>
    <p class="font-bold text-xl pt-4 pb-2">Berechnung</p>
    <div class="bg-gray-100 p-4 rounded-lg shadow-md border border-gray-300">
      <p class="font-mono text-lg text-center text-black">
        score = 100 • (1 - (0.5 • n<sub>kurz</sub> + 0.6 • n<sub>mittel</sub> + 0.7 • n<sub>lang</sub> + 0.8 • n<sub>extrem</sub> + n<sub>ausfall</sub>) / n<sub>gesamt</sub>)
      </p>
    </div>
  </div>
</template>