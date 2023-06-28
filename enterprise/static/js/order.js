$(document).ready(() => {
  $('.product-inputs').on('input', () => {

    var changedInputValue = $(this).val();
    var inputIndex = $('.product-inputs').index(this);
    console.log('Input at index', inputIndex, 'changed:', changedInputValue);
    // $(this).val = changedInputValue
  });
});
