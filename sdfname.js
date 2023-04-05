/* javascript to accompany jquery.html */

$(document).ready(
    /* this defines a function that gets called after the document is in memory */
    function()
    {

      /* add a click handler for our button */
      $("#sdfnsub").click(
        function()
        {
      /* ajax post */
      $.post("/Loc",
        /* pass a JavaScript dictionary */
        {
          sdfname: $("#sdfname").val()
      );
        }
      );
    }
  );
