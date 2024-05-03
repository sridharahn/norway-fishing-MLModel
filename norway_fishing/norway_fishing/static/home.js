$(document).ready(function(){
    $('.modal').modal();
    $('.dropdown-trigger').dropdown();
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
 });

 function createCard(prediction, tool, name) {
    var imageUrl = "/static/fish/"+prediction+".jpeg"
    var cardHtml = '<div class="col-sm-3 p-2">' +
                        '<div class="card h-100">' +
                        '<img src="'+imageUrl+'" class="card-img-top" alt="Fish Image">' +
                            '<div class="card-body">' +
                                '<h5 class="card-title">' + name + '</h5>' +
                                '<p class="card-text">Suggested Tool: '+tool+'</p>' +
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
});
