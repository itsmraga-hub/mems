$(document).ready(() => {
  var cartItems = [];

  $('.add-to-cart').click(function() {
    var productId = $(this).data('product-code');
    var quantity = $(this).siblings('.quantity').val();

    var cartItem = {
      product_id: productId,
      quantity: quantity
    };

    cartItems.push(cartItem);
    $(this).text('Added to Cart').prop('disabled', true);
  });

  $('#order').click(function(e) {
    e.preventDefault();
    var productsJSON = JSON.stringify(cartItems);

    // Pass the selected products to the cart page
    var url = 'order/?products=' + encodeURIComponent(productsJSON);
    window.location.href = url;
  });

  // $('#order').click(() => {
  //   print('Order clicked')
  //   $.ajax({
  //     url: '/add_to_order/',
  //     method: 'POST',
  //     data: {
  //       cart_items: JSON.stringify(cartItems)
  //     },
  //     success: (response) => {
  //       // Update the cart content on success
  //       $('#cart').html(response.cart_content);
  //     },
  //     error: function(xhr, status, error) {
  //       // Handle error if needed
  //       console.log(error);
  //     }
  //   });

    // Clear cart items after adding to cart
  //   cartItems = [];
  // });
});
