
// Gives name of the station that matches the id
export function getNameByID(stationID) {
    return window.stationIds[stationID].name;
}


// Gives station data corresponding to the station name
export function getValueByName(stationName) {
    const stationValues = Object.values(window.stationIds);
    for (let element of stationValues) {
        if (element.name === stationName) {
            return element;
        }
    }
    return null;
}


// Gives id of the station with the given name
export function getIDByName(stationName) {
    for (let key of Object.keys(window.stationIds)) {
        if (window.stationIds[key].name === stationName) {
            return key;
        }
    }
    return null;
}
