"use strict";

const serverUrl = "http://35.182.117.67:8000";

async function uploadImage() {
    // encode input file as base64 string for upload
    let file = document.getElementById("file").files[0];
    let converter = new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result
            .toString().replace(/^data:(.*,)?/, ''));
        reader.onerror = (error) => reject(error);
    });
    let encodedString = await converter;

    // clear file upload input field
    document.getElementById("file").value = "";

    // make server call to upload image
    // and return the server upload promise
    return fetch(serverUrl + "/images", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({filename: file.name, filebytes: encodedString})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function updateImage(image) {
    document.getElementById("view").style.display = "block";

    let imageElem = document.getElementById("image");
    imageElem.src = image["fileUrl"];
    imageElem.alt = image["fileId"];

    return image;
}

function translateImage(image) {
    // make server call to translate image
    // and return the server upload promise
    return fetch(serverUrl + "/images/" + image["fileId"] + "/translate-text", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({fromLang: "auto", toLang: "en"})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function annotateImage(translations) {
    let translationsElem = document.getElementById("translations");
    // Emander Changes: Define a variable array to store each line of the translated text
    let combined_translated_text = [];
    while (translationsElem.firstChild) {
        translationsElem.removeChild(translationsElem.firstChild);
    }
    translationsElem.clear
    for (let i = 0; i < translations.length; i++) {
        let translationElem = document.createElement("h6");
        translationElem.appendChild(document.createTextNode(
            translations[i]["text"] + " -> " + translations[i]["translation"]["translatedText"]
        ));
        translationsElem.appendChild(document.createElement("hr"));
        translationsElem.appendChild(translationElem);
        // Emander Changes: Push each line of the translated text to the array
        combined_translated_text.push(translations[i]['translation']['translatedText'])
    }
    // Emander Changes: return the array of translated text to be used in the createSpeech function
    return combined_translated_text
}

// Emander Changes: Create a function to create the speech from the translated text
function createSpeech(combined_translated_text) {
    // Emander Changes: make server call to text-to-speech endpoint in app.py
    return fetch(serverUrl + "/text-to-speech/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        // Emander Changes: Send the array of translated text to the server
        body: JSON.stringify({combined_translated_text: combined_translated_text})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    }).then(data => {
        document.getElementById("audio_source").src = "../Capabilities/" + data.outputFile;
        // Emander Changes: Display the audio result
        document.getElementById("audio_result").style.display = "block";
        document.getElementById("audio_player").load();
        document.getElementById("audio_player").play();
    })
}

function uploadAndTranslate() {
    uploadImage()
        .then(image => updateImage(image))
        .then(image => translateImage(image))
        .then(translations => annotateImage(translations))
        // Emander Changes: Pass the array of translated text to the createSpeech function
        .then(combined_translated_text => createSpeech(combined_translated_text))
        .catch(error => {
            alert("Error: " + error);
        })
}

class HttpError extends Error {
    constructor(response) {
        super(`${response.status} for ${response.url}`);
        this.name = "HttpError";
        this.response = response;
    }
}