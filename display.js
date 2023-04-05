/* javascript to accompany jquery.html */

$(document).ready(
    /* this defines a function that gets called after the document is in memory */
    function()
    {

      /* add a click handler for our button */
      $("#displaybutton").click(
        function(e)
        {
          e.preventDefault();
      /* ajax post */
      // $.post("/display.html",
      //   /* pass a JavaScript dictionary */
      //   {
      //     molsel: $("#mol_select").val(),
      //     axis: $("#options").val(),
      //     degreesc: $("#degrees").val()
      //
      //   //   name: $("#name").val(),	/* retreive value of name field */
      //   //   extra_info: "some stuff here"
      //   },
      //   function( data, status )
      //   {
      //     $("#output").html(data)
      //
      //   }
      // );
      $.ajax({url: "/display.html",
      type:"POST",
      data: {molsel: $("#mol_select").val(), axis: $("#options").val(), degreesc: $("#degrees").val()}, success: function(data, status){$("#output").html(data)}});
        }
      );
    }
  );
