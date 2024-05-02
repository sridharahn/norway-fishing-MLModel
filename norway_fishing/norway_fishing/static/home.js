$(document).ready(function(){
    $('.modal').modal();
    $('.dropdown-trigger').dropdown();
 });

 document.addEventListener('DOMContentLoaded', function() {
    // Initialize the slider
    var slider = document.getElementById('slider');
    var sliderValue = document.getElementById('slider-value');
    var sl_slider = document.getElementById('sl_slider');
    var shipLength = document.getElementById('ship-length');
    var ep_slider = document.getElementById('ep_slider');
    var enginePower = document.getElementById('engine-pwoer');

    slider.addEventListener('input', function() {
        sliderValue.textContent = slider.value;
    });
    sl_slider.addEventListener('input', function() {
        shipLength.textContent = sl_slider.value;
    });
    ep_slider.addEventListener('input', function() {
        enginePower.textContent = ep_slider.value;
    });
});