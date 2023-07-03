$(document).ready(function () {
  $('#search-input').on('input', function () {
    var query = $(this).val();
    if (query.length >= 2) {
      $.ajax({
        url: '/memsprise/products',
        method: 'GET',
        data: { 'query': query },
        success: function (data) {
          // $('#search-results').html(data);
          console.log('success')
        }
      });
    } else {
      // $('#search-results').empty();
      console.log('fail')
    }
  });
});