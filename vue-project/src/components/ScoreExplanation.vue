<template>
  <div>
    <p class="font-bold text-xl pt-4">Beschreibung</p>
    <ul>
      <p>Diese Scores ergeben sich aus einer gewichteten Inzidenz, wobei geringere Verspätungen das Ergebnis weniger stark beeinflussen als längere.</p>
      <p>Der Main Score wird darüber hinaus über die jeweiligen Werte aller derzeit erfassten Umweltfaktoren gemittelt.</p>
    </ul>
    <p class="font-bold text-xl pt-4">Berücksichtigte Umweltfaktoren</p>
    <ul>
      <li>Lichtverhältnisse</li>
      <li>Temperatur</li>
      <li>Verkehrsaufkommen</li>
      <li>Wetter</li>
    </ul>
    <p class="font-bold text-xl pt-4">Berechnung</p>
    <div class="bg-gray-100 p-4 rounded-lg shadow-md border border-gray-300">
      <p class="font-mono text-lg text-center text-black">
        Score = 100 * (1 - (0.2 • V<sub>kurz_n</sub> + 0.4 • V<sub>mittel_n</sub> + 0.6 • V<sub>lang_n</sub> + 0.8 • V<sub>extrem_n</sub> + Ausfall<sub>n</sub>) / Gesamtmessungen<sub>n</sub>)
      </p>
    </div>
  </div>
</template>