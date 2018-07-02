//Change Car Img Start
$(document).ready(function(){
    $("select").change(function(){
        //$("input").change();
    });
});

function display(value) {
    //alert(value);
    $("#car_img").html("<img id='theImg' src='/static/img/" + value + ".jpg' class='\responsive-img\' style='width:100%;'/>");

    var car_model = value

    $.ajax({
        type: "GET",
        url: '/get_car_data',
        data: {
            'car_model': car_model,
        },
        //dataType: 'json',
        success: function (data) {

            var car_array = [];
            for(var property in data) {
            car_array.push(data[property]);
            }

            //myObj = $.parseJSON(data);
            $( '#range' ).text(car_array[0] + " km");
            $( '#battery' ).text(car_array[1]+ " kWh");
            $( '#acceleration' ).text(car_array[2] + " sec");
            $( '#speed' ).text(car_array[3] + " km/h");
            $( '#power' ).text(car_array[4]);

        }
    });
};

//Change Maps Location IN DEVELOPMENT
$(document).ready(function(){
    $("#start").mouseout(function(){
        //alert("test");
        //update_map(value)
    });
});

function update_map(value){
    var location = value

    $.ajax({
        type: "GET",
        url: '/get_geo_data',
        data: {
            'location': location,
        },
        //dataType: 'json',
        success: function (data) {
            alert("success ajax")
            var geo_array = [];
            for(var property in data) {
            geo_array.push(data[property]);
            }
            //update map

        }
    });
}


function showLoadingImg() {
    //alert("loading");
    //document.getElementById('form-load-img').style.display = 'block';
    $(".loading").css("display", "block");
};


//CSRF_TOKEN UPDATE
$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});