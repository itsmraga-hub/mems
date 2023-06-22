$(document).ready(() => {
  $('#sidebar-open').click(() => {
    // console.log('first')
    $('#sidebar-container').toggleClass('sidebar-container sidebar-closed')
    $('#main-content-container').toggleClass('width-large')
  });

});