// window.setTimeout(function () {
//   location.href = "http://127.0.0.1:8000/memsprise/dashboard";
// }, 5000);

$(document).ready(function () {
  $('#dropdown-profile-icon').click(() => {
    // console.log('first')
    $('#dropdown-content').toggleClass('block none')
  });

  $('#sidebar-dashboards').click(() => {
    $('#sidebar-container__div-dropdown-dashboards').toggleClass('block none');
  })
  $('#sidebar-products').click(() => {
    $('#sidebar-container__div-dropdown-products').toggleClass('block none');
  })

  $('#sidebar-orders').click(() => {
    $('#sidebar-container__div-dropdown-orders').toggleClass('block none');
  })
  $('#sidebar-users').click(() => {
    $('#sidebar-container__div-dropdown-users').toggleClass('block none');
  })
});

