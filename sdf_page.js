// /* javascript to accompany jquery.html */
//
// $(document).ready(
//     /* this defines a function that gets called after the document is in memory */
//     function()
//     {
//
//       /* add a click handler for our button */
//       $("#uploadsdfn").click(
//         function(e)
//         {
//           e.preventDefault();
//       /* ajax post */
//       var formData = new FormData();
//
//       /* add the file input and molecule name input to the FormData object */
//       formData.append('filename', $('#sdf_file')[0].files[0]);
//       formData.append('entmolname', $('#emolname').val());
//
//       /* send an AJAX POST request */
//       $.ajax({
//         url: '/sdf_page.html',
//         type: 'POST',
//         data: formData,
//         contentType: false,
//         processData: false,
//         success: function(data, status) {
//           alert('Data: ' + data + '\nStatus: ' + status);
//         }
//       );
//         }
//       );
//     }
//   );
