const colorPicker = document.getElementById('color_picker');
const colorRgb = document.getElementById('color_rgb');
const statuses = document.getElementById('statuses');
const pickButton = document.getElementById('pick_color');
const toggleSwitch = document.getElementById('toggle_switch');
const brightness = document.getElementById('brightness');
const brightnessValue = document.getElementById('brightness_value');
const device_preview = document.getElementById('device_preview');
const deviceSelect = document.getElementById('device'); // Device select element
const checkOn = document.getElementById('check_on');
const modeSwitch = document.getElementById('mode_switch');
const modeColor = document.getElementById('mode_color');
const modeWhite = document.getElementById('mode_white');
const hue = document.getElementById('hue');
const hueValue = document.getElementById('hue_value');
const form = document.getElementById('main_form');
const deleteButton = document.getElementById('delete_device');

colorPicker.addEventListener('input', () => {
    const hexColor = colorPicker.value;

    // Convert HEX to RGB
    const rgb = hexToRgb(hexColor);
    colorRgb.value = `"r": ${rgb.r}, "g": ${rgb.g}, "b": ${rgb.b}`;
});

// Helper function to convert HEX to RGB
function hexToRgb(hex) {
    const bigint = parseInt(hex.slice(1), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return { r, g, b };
}

// Aktualizacja wartości wyświetlanej obok suwaka
brightness.addEventListener('input', () => {
    brightnessValue.textContent = brightness.value;
});

hue.addEventListener('input', () => {
    hueValue.textContent = hue.value;
});

deleteButton.addEventListener('click', () => {
    let currentStatuses = {};
    try {
        currentStatuses = JSON.parse('{' + statuses.value + '}');
    } catch (e) {
        console.warn('Invalid JSON in statuses:', statuses.value);
    }

    if (currentStatuses.hasOwnProperty(device_preview.value)) {
        delete currentStatuses[device_preview.value];
    }
    let jsonString = JSONtoString(currentStatuses);
    jsonString = jsonString.substring(2, jsonString.length - 2);                    // Usuń pierwszy "{" i ostatni znak "}"
    if (jsonString != "{}"){
        statuses.value = jsonString;
    }
    else {
        statuses.value = "";
    }
    updateDeviceSelect();
});

// Dodanie danych do textarea po kliknięciu przycisku "PICK"
pickButton.addEventListener('click', () => {
    let currentStatuses = {};
    let editStatus = false;
    let newStatus = "";
    try {
        currentStatuses = JSON.parse('{' + statuses.value + '}');
    } catch (e) {
        console.warn('Invalid JSON in statuses:', statuses.value);
    }

    // Sprawdź, czy `statuses` ma poprawny JSON
    try {
        currentStatuses = JSON.parse('{' + statuses.value + '}');
    } catch (e) {
        console.warn('Invalid JSON in statuses:', statuses.value);
    }

    // Sprawdź, czy `device_preview` już istnieje
    if (currentStatuses.hasOwnProperty(device_preview.value)) {
        editStatus = true;
    }
    if ((statuses.value != "") && !editStatus) {
        statuses.value += ', \n'
    }
    const toggleSwitchValue = toggleSwitch.checked ? 'on' : 'off';
    if (toggleSwitchValue == 'on'){
        const modeSwitchValue = modeSwitch.checked ? 'color' : 'white';
        if (modeSwitchValue == 'color'){
            newStatus = '{ "switch": "' + (toggleSwitch.checked ? 'on' : 'off') + '", "ltype": "color", "color": { "br": ' + brightness.value + ','+ colorRgb.value + ' } }';
        }
        else{
            newStatus = '{ "switch": "' + (toggleSwitch.checked ? 'on' : 'off') + '", "ltype": "white", "white": { "br": ' + brightness.value + ', "ct": '+ hue.value + ' } }';
        
        }
    }
    else{
        newStatus = '{ "switch": "off" }';
    
    }
    newStatus = JSON.parse(newStatus);
    if (editStatus){
        currentStatuses[device_preview.value] = newStatus;
        let jsonString = JSONtoString(currentStatuses);
        jsonString = jsonString.substring(2, jsonString.length - 2);                    // Usuń pierwszy "{" i ostatni znak "}"
        statuses.value = jsonString;
    }
    else{
        newStatus =JSON.parse('{"' + device_preview.value + '": ' + JSONtoString(newStatus)+'}');
        newStatus = JSONtoString(newStatus);
        newStatus = newStatus.substring(2, newStatus.length - 2); 
        statuses.value += newStatus;
        updateDeviceSelect();
    }
});

function JSONtoString(json){
    let jsonString = JSON.stringify(json, null, 2);                      // Sformatowany JSON
    jsonString = jsonString.replace(/\\"/g, '"');                                   // Usuń ukośniki przed cudzysłowami
    jsonString = jsonString.trim();                            // Usuń nadmiarowe białe znaki (spacje, nowe linie, itp.)
    jsonString = jsonString.replace(/"\s*{\s*/g, '{').replace(/\s*}\s*"/g, '}');    // Usuń znaki " przed { i za }
    return jsonString;
}

function onLoadStatus(status){
    currentStatuses = JSON.parse('{' + status + '}');
    currentStatuses = JSONtoString(currentStatuses);
    currentStatuses = currentStatuses.substring(2, currentStatuses.length - 2); 
    statuses.value = currentStatuses;
}

document.addEventListener("DOMContentLoaded", function() {
    if (statuses.value.length > 0) {
        onLoadStatus(statuses.value);
    }
});

toggleSwitch.addEventListener("click", () => {
    const toggleSwitchValue = toggleSwitch.checked ? 'on' : 'off';
    if(toggleSwitchValue === 'off'){
        checkOn.style.display = "none";
    }
    else{
        checkOn.style.display = "block";
    }
});

modeSwitch.addEventListener("click", () => {
    const modeSwitchValue = modeSwitch.checked ? 'color' : 'white';
    if(modeSwitchValue === 'white'){
        modeColor.style.display = "none";
        modeWhite.style.display = "block";
    }
    else{
        modeColor.style.display = "block";
        modeWhite.style.display = "none";
    }
});

// Funkcja aktualizująca selecta z device
function updateDeviceSelect() {
    const deviceOptions = Array.from(deviceSelect.options); // Get all device options
    
    deviceOptions.forEach(option => {
        const deviceId = option.value; // ID of the device
        // If the device ID exists in statuses, select the option
        if (statuses.value.includes(deviceId)) {
            option.selected = true;
        } else {
            option.selected = false;
        }
    });
};

form.addEventListener('submit', (event) => {
    deviceSelect.disabled= false;
    statuses.disabled= false;
    statuses.value = "{" + statuses.value + "}";
});
