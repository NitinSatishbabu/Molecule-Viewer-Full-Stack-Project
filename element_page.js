/* javascript to accompany jquery.html */

$(document).ready(
    /* this defines a function that gets called after the document is in memory */
    function()
    {

      /* add a click handler for our button */
      $("#addbutton").click(
        function(e)
        {
          e.preventDefault();
      /* ajax post */
      $.post("/form_handler.html",
        /* pass a JavaScript dictionary */
        {
          element_number: $("#elementNumber").val(),
          element_code: $("#elementCode").val(),
          element_name: $("#elementName").val(),
          colour_1: $("#colour1").val(),
          colour_2: $("#colour2").val(),
          colour_3: $("#colour3").val(),
          radius: $("#radius").val()

        //   name: $("#name").val(),	/* retreive value of name field */
        //   extra_info: "some stuff here"
        },
        function( data, status )
        {
          alert( "Data: " + data + "\nStatus: " + status );
        }
      );
        }
      );
    }
  );
