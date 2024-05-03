$(document).ready(function(){
    $('#speciesForm').submit(function(event) {
        event.preventDefault(); 

if (
    locMarker &&
    locMarker.getLatLng() &&
    locMarker.getLatLng().lat !== null &&
    locMarker.getLatLng().lng !== null
) {
    document.getElementById("locationError").style.display = "none";
    const formData = new FormData(this);
    const data = {};
    const latitude = locMarker.getLatLng().lat;
    const longitude = locMarker.getLatLng().lng;

    console.log("formData", formData);
    formData.forEach((value, key) => (data[key] = value));
    data["Lon (location)"] = longitude;
    data["Lat (location)"] = latitude;
    // Get the CSRF token from the cookie
    const csrftoken = getCookie("csrftoken");

    // Send data to backend for prediction
    fetch("/models/randomforest", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            $("#predictContainer").show();
            $('#predictionCards').empty();
            $.each(data.prediction, function(index, value) {
                createCard(value.code, value.tool, value.name);
            });
        })
        .catch((error) => console.error("Error:", error));
} else {
    console.log("I am error");
    document.getElementById("locationError").style.display = "block";
}

    });

    $('#toolsForm').submit(function(event) {
        event.preventDefault(); 

if (
    locMarker2 &&
    locMarker2.getLatLng() &&
    locMarker2.getLatLng().lat !== null &&
    locMarker2.getLatLng().lng !== null
) {
    document.getElementById("locationError2").style.display = "none";
    const formData = new FormData(this);
    const data = {};
    const latitude = locMarker2.getLatLng().lat;
    const longitude = locMarker2.getLatLng().lng;

    console.log("formData", formData);
    formData.forEach((value, key) => (data[key] = value));
    data["Lon (location)"] = longitude;
    data["Lat (location)"] = latitude;
    // Get the CSRF token from the cookie
    const csrftoken = getCookie("csrftoken");

    // Send data to backend for prediction
    fetch("/models/predictknn", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            $("#suggestionContainer").show();
            $('#suggestionCards').empty();
            $('#predictionCards2').empty();
            $.each(data.prediction, function(index, value) {
                createPrediction(value.code, value.tool, value.name);
            });
            $.each(data.suggestion, function(index, value) {
                createSuggestionCards(value.code, value.tool, value.name);
            });
        })
        .catch((error) => console.error("Error:", error));
} else {
    document.getElementById("locationError2").style.display = "block";
}

    });

    function createSuggestionCards(prediction, tool, name) {
        var imageUrl = "/static/fish/"+prediction+".jpg"
        var cardHtml = '<div class="col-sm-2 p-2 m-2">' +
                            '<div class="card h-80">' +
                            '<img src="'+imageUrl+'" class="card-img-top" alt="Fish Image">' +
                                '<div class="card-body">' +
                                    '<h5 class="card-title">' + name + '</h5>' +
                                    '<p class="card-text"><i>Suggested Tool:</i><strong> '+tool+'</strong></p>' +
                                '</div>' +
                            '</div>' +
                        '</div>';
        $('#suggestionCards').append(cardHtml);
    }


    function createPrediction(prediction, tool, name) {
        var imageUrl = "/static/fish/"+prediction+".jpg"
        var cardHtml = '<div class="card bg-info mb-3 p-3" style="max-width: 540px;">'+
                        '<div class="row g-0">'+
                        '<div class="col-md-4">'+
                            '<img src="'+imageUrl+'" class="img-fluid rounded-start" alt="...">'+
                        '</div>'+
                        '<div class="col-md-8">'+
                            '<div class="card-body">'+
                            '<h5 class="card-title">Suggested Tool:<strong>'+tool+'</strong></h5>'+
                            '<p class="card-text"><small class="text-body-secondary">'+name+'</small></p>'+
                            '</div>'+
                        '</div>'+
                        '</div>'
        $('#predictionCards2').append(cardHtml);
    }

 });

 function createCard(prediction, tool, name) {
    var imageUrl = "/static/fish/"+prediction+".jpg"
    var cardHtml = '<div class="col-sm-3 p-2">' +
                        '<div class="card h-100">' +
                        '<img src="'+imageUrl+'" class="card-img-top" alt="Fish Image">' +
                            '<div class="card-body">' +
                                '<h5 class="card-title">' + name + '</h5>' +
                                '<p class="card-text"><i>Suggested Tool: '+tool+'</i></p>' +
                            '</div>' +
                        '</div>' +
                    '</div>';
    $('#predictionCards').append(cardHtml);
}

 document.addEventListener('DOMContentLoaded', function() {
    // Initialize the slider
    var Crew = document.getElementById('Crew');
    var CrewValue = document.getElementById('Crew-value');
    var sl_slider = document.getElementById('sl_slider');
    var shipLength = document.getElementById('ship-length');
    var ep_slider = document.getElementById('ep_slider');
    var enginePower = document.getElementById('engine-power');
    var pw_slider = document.getElementById('pw_slider');
    var productWeight = document.getElementById('product-weight');
    var Crew2 = document.getElementById('Crew2');
    var CrewValue2 = document.getElementById('Crew-value2');
    var sl_slider2 = document.getElementById('sl_slider2');
    var shipLength2 = document.getElementById('ship-length2');
    var ep_slider2 = document.getElementById('ep_slider2');
    var enginePower2 = document.getElementById('engine-power2');

    Crew.addEventListener('input', function() {
        CrewValue.textContent = Crew.value;
    });
    sl_slider.addEventListener('input', function() {
        shipLength.textContent = sl_slider.value;
    });
    ep_slider.addEventListener('input', function() {
        enginePower.textContent = ep_slider.value;
    });
    pw_slider.addEventListener('input', function() {
        productWeight.textContent = pw_slider.value;
    });

    Crew2.addEventListener('input', function() {
        CrewValue2.textContent = Crew2.value;
    });
    sl_slider2.addEventListener('input', function() {
        shipLength2.textContent = sl_slider2.value;
    });
    ep_slider2.addEventListener('input', function() {
        enginePower2.textContent = ep_slider2.value;
    });
});
