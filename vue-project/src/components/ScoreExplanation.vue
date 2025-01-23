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
    <p>Score = 100 * (1 - (0,2 • V_kurz_n + 0,4 • V_mittel_n + 0,6 • V_lang_n + 0,8 • V_extrem_n + Ausfall_n)/Gesamtmessungen_n)</p>
    </div>
</template>