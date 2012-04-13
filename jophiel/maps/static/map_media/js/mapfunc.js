
function resetMarker(){
    if (clickMarker != null) {
        clickMarker.setMap(null);
        clickMarker = null;
    }
    for (var i = 0; i < poiMarker.length; i++) {
    }
    for (var i = 0; i < infoWindows.length; i++) {
        infoWindows[i].close();
    }
}

function listenClickMessage(map) {
	google.maps.event.addListener(map, 'click', function(event) {
		placeMarker(event.latLng);
	});
}

function placeMarker(location) {
	var clickedLocation = new google.maps.LatLng(location);
	var marker = new google.maps.Marker({
		position : location,
		map : map
	});

	map.setCenter(location);
}


function showDefaultLocatin(map){
    var initialLocation;
    var siberia = new google.maps.LatLng(60, 105);
    var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
    var browserSupportFlag = new Boolean();
    
    var infowindow = new google.maps.InfoWindow();
    infoWindows.push(infowindow);
    // Try W3C Geolocation method (Preferred)
    if (navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position){
            initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            contentString = buidlClickMessageInfo(position.coords.latitude,position.coords.longitude);
            map.setCenter(initialLocation);
            map.setZoom(12);
            infowindow.setContent(contentString);
            infowindow.setPosition(initialLocation);
            infowindow.open(map);
        }, function(){
            handleNoGeolocation(browserSupportFlag);
        });
    }
    
};

function handleNoGeolocation(errorFlag){
    if (errorFlag == true) {
        initialLocation = newyork;
        contentString = "Error: The Geolocation service failed.";
    }
    else {
        initialLocation = siberia;
        contentString = "Error: Your browser doesn't support geolocation. Are you in Siberia?";
    }
    map.setCenter(initialLocation);
    infowindow.setContent(contentString);
    infowindow.setPosition(initialLocation);
}


function onClickCallback(event){
    var clickMessage = "";
    resetMarker();
    if (event.latLng) {
        clickMarker = new google.maps.Marker({
            'position': event.latLng,
            'map': map,
            'title': event.latLng.toString(),
        });
        
        var infowindow = new google.maps.InfoWindow({
            content: buidlClickMessageInfo(event.latLng.lat(), event.latLng.lng()),
            size: new google.maps.Size(50, 50)
        });
        google.maps.event.addListener(clickMarker, 'click', function(){
            infowindow.open(map, clickMarker);
        });
        map.panTo(clickMarker.getPosition());
        google.maps.event.trigger(clickMarker, 'click');
    }
    
    
}

function attachSecretMessage(marker, number){
    var infowindow = new google.maps.InfoWindow({
        content: messages[number].showinfo,
        size: new google.maps.Size(50, 50)
    });
    infoWindows.push(infowindow);
    google.maps.event.addListener(marker, 'click', function(){
        resetMarker();
        infowindow.open(map, marker);
    });
}

function showRegion(map){
    var max = {
        x: -180,
        y: -90
    };
    var min = {
        x: 180,
        y: 90
    };
    
    if (messages.length <= 0) {
    
        showDefaultLocatin(map)
    }
    else {
    
        for (var i = 0; i < messages.length; i++) {
            var x = messages[i].x;
            var y = messages[i].y;
            if (x > max.x) {
                max.x = x;
            };
            if (x < min.x) {
                min.x = x;
            };
            
            if (y > max.y) {
                max.y = y;
            };
            if (y < min.y) {
                min.y = y;
            };
                    };
        var southWest = new google.maps.LatLng(min.y, min.x);
        var northEast = new google.maps.LatLng(max.y, max.x);
        if (min.y == max.y) {
            map.setCenter(southWest);
            map.setZoom(14);
        }
        else {
            var bounds = new google.maps.LatLngBounds(southWest, northEast);
            map.fitBounds(bounds);
        }
        
    }
}