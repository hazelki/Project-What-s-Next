function initMap() {

    var sanFran = {
        lat: 37.773972,
        lng: -122.431297
    };

    var map = new google.maps.Map(document.getElementById('map'), {
        center: sanFran,
        scrollwheel: true,
        zoom: 10,
        zoomControl: true,
        panControl: true,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    // Define global infoWindow
    // If you do this inside the loop where you retrieve the json,
    // the windows do not automatically close when a new marker is clicked
    // and you end up with a bunch of windows opened at the same time.
    // What this does is create one infowindow and we replace the content
    // inside for each marker.
    var infoWindow = new google.maps.InfoWindow({
        width: 150
    });

  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }
}

function renderEvents(eventIds) {

  // console.log(eventIds);
  // console.log('got here');
     var sanFran = {
        lat: 37.773972,
        lng: -122.431297
    };

    var map = new google.maps.Map(document.getElementById('map'), {
        center: sanFran,
        scrollwheel: true,
        zoom: 10,
        zoomControl: true,
        panControl: true,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    // Define global infoWindow
    // If you do this inside the loop where you retrieve the json,
    // the windows do not automatically close when a new marker is clicked
    // and you end up with a bunch of windows opened at the same time.
    // What this does is create one infowindow and we replace the content
    // inside for each marker.
    var infoWindow = new google.maps.InfoWindow({
        width: 150
    });
    
  var commaList = eventIds.join();
  console.log(commaList);
  console.log('got comma list');
  // Retrieving the information with AJAX
  $.get('/marker_result?id=' + commaList, function (events) {
      // Attach markers to each bear location in returned JSON
      // JSON looks like:
      // {events:[
      // {
      //   "address": "addres", 
      //   "date": "2016-01-01", 
      //   "event_id": 1, 
      //   "lat": "37.77", 
      //   "longi": "-122.41", 
      //   "picture": "picture", 
      //   "title": "title"
      // }]
      // }
      var event, marker, html;

      var i = 0
      var arrayLength = events.events.length;
      for (var i = 0; i < arrayLength; i++) {
        var event = events.events[i];
        console.log(i++ + " " + event.title);

        // Define the marker
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(event.lat, event.longi),
          map: map,
          title: event.title
        });

        // Define the content of the infoWindow
        html = (
          '<div class="window-content">' +
              '<img src=\"'+ event.picture +'\" alt="polarbear" style="width:150px;" class="thumbnail">' +
              '<p><b>Event Date: </b>' + event.date + '</p>' +
              '<p><b>Address: </b>' + event.address + '</p>' +
          '</div>');

        // Inside the loop we call bindInfoWindow passing it the marker,
        // map, infoWindow and contentString
        bindInfoWindow(marker, map, infoWindow, html);
      }

  });

  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }
}

//google.maps.event.addDomListener(window, 'load', initMap);