import stationIds from "../../../datascraping/stationData/station_ids.json";

export function getNameByID(stationID) {
    return stationIds[stationID].name;
}

export function getValueByName(stationName) {
    const stationValues = Object.values(stationIds);
    for (let element of stationValues) {
        if (element.name === stationName) {
            return element;
        }
    }
    return null;
}

export function getIDByName(stationName) {
    for (let key of Object.keys(stationIds)) {
        if (stationIds[key].name === stationName) {
            return key;
        }
    }
    return null;
}
