const $ = window.$;
$(document).ready(function () {
  const amenitiesList = [];
  $('input').css('margin-left', '10px');
  $('input[type=checkbox]').click(function () {
    if ($(this).prop('checked')) {
      amenitiesList.push($(this).attr('data-name'));
    } else {
      const index = amenitiesList.indexOf($(this).attr('data-name'));
      amenitiesList.splice(index, 1);
    }
    $('.amenities h4').text(amenitiesList.join(', ')).css({ width: '220px', height: '16px', overflow: 'hidden', 'text-overflow': 'ellipsis', 'white-space': 'nowrap' });
  });
  $.get('http://0.0.0.0:5001/api/v1/status/', function (data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
});
