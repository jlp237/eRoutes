function myMap() {
    var mapCanvas = document.getElementById("map");
    var mapOptions = {
        center: new google.maps.LatLng(53.5, 9.9),
        zoom: 10
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);
}



function test(){
    var location = 'Bangkok';
    var lat = 10.5;
    var lng = 15.5;

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