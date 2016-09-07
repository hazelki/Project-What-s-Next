function submitButton(event_id) {

  var data = {};
  data["event_id"] = event_id;
  $.post("/add",
        data, 
        function() {
  $("#" + event_id).css( "background", "light blue" );
  $( "#" + event_id).html("Saved");
        });
}