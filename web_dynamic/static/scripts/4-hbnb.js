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
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/places_search',
    type: 'POST',
    data: JSON.stringify({}),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      for (let i = 0; i < data.length; i++) {
        $('section.places').append('<article></article>');
        $('.places article:last-child').append('<div class="title_box"></div>');
        $('.title_box:last-child').append(`<h2>${data[i].name}</h2>`);
        $('.title_box:last-child').append(`<div class="price_by_night">$${data[i].price_by_night}</div>`);
        $('article:last-child').append('<div class="information"></div>');
        if (data[i].max_guest === 1) {
          $('.information:last-child').append(`<div class="max_guest">${data[i].max_guest} Guest</div>`);
        } else { $('.information:last-child').append(`<div class="max_guest">${data[i].max_guest} Guests</div>`); }
        if (data[i].number_rooms === 1) {
          $('.information:last-child').append(`<div class="number_rooms">${data[i].number_rooms} Bedroom</div>`);
        } else { $('.information:last-child').append(`<div class="number_rooms">${data[i].number_rooms} Bedrooms</div>`); }
        if (data[i].number_bathrooms === 1) {
          $('.information:last-child').append(`<div class="number_bathrooms">${data[i].number_bathrooms} Bathroom</div>`);
        } else { $('.information:last-child').append(`<div class="number_bathrooms">${data[i].number_bathrooms} Bathrooms</div>`); }
        $('article:last-child').append('<div class="user"><b>Owner:</b> Valentina</div>');
        $('article:last-child').append(`<div class="description">${data[i].description}</div>`);
      }
    }
  });
  $('button').click(function () {
    $('article').remove();
    const data = { amenities: amenities.id };
    getAll(JSON.stringify(data));
  });
});
