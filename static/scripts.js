/**
 * Created by Stuart on 8/17/2015.
 */


$(document).ready(function() {
    document.getElementById("audio").volume=0.3;

    $("#slider").slider({
        min: 0,
        max: 100,
        value: 30,
        slide: function(event, ui) {
            setVolume(ui.value / 100);
        }
    });

    function setVolume(v) {
        var cabinsound = document.getElementById('audio');
        cabinsound.volume = v;
    }

    setTimeout(function() {
        $("#donate").show();
        $("#blurb").hide();
    }, 6000); // wait 10 mins and hide it
});

