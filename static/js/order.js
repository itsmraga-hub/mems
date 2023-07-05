$(document).ready(() => {
  $('.product_inputs').on('input', () => {
    $.ajax({
      url: '/memsprise/order',
      method: 'PUT',
      data: { 'query': query },
      success: function (data) {
        // $('#search-results').html(data);
        console.log('success')
      }
    })
  });
});