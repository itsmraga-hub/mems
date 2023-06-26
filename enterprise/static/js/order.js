$(document).ready(function() {
  // Select the form by name
  var orderForm = $('div[name="orderForm"]');

  // Intercept the form submission
  orderForm.submit(function(e) {
    e.preventDefault(); // Prevent the form from submitting normally

    // Get the form data
    var formData = orderForm.serialize();
    console.log(formData)

    // Send an AJAX request to the Django view
    $.ajax({
      type: 'POST',
      url: '/confirm-order/',
      data: formData,
      success: function(response) {
        // Handle the success response
        // For example, display a success message or redirect to a success page
      },
      error: function(xhr, status, error) {
        // Handle the error response
        // For example, display an error message or perform error handling
      }
    });
  });
});




// $(document).ready(function() {
//   var selectedProducts = [];

//   function renderSelectedProducts() {
//     var selectedProductsContainer = $('#selected-products');

//     // Clear the container before rendering
//     selectedProductsContainer.empty();

//     // Render selected products
//     selectedProducts.forEach(function(productId) {
//       // Fetch product details from the server and append to the container
//       // ...
//       // Example: selectedProductsContainer.append('<li>' + product.name + '</li>');
//     });
//   }

//   // Retrieve selected products from the URL parameter
//   var urlParams = new URLSearchParams(window.location.search);
//   var productsParam = urlParams.get('products');
//   // console.log(productsParam);

//   if (productsParam) {
//     selectedProducts = productsParam.split(',');
//     renderSelectedProducts();
//   }

//   // $('#confirm-order').click(function() {
//   //   // Perform the order confirmation logic
//   //   // ...

//   //   // Redirect to the order confirmation page
//   //   window.location.href = '/order-confirmation/';
//   // });
// });