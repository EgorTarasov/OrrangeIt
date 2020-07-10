let event_address = document.querySelectorAll('p.event_address');
let event_follow_statuses = document.querySelectorAll('p.followStatus');
let radiusZone;
const maxRadius = 40000;
let myMap;
let radius;
let user_geo;
let pinsCollection;

function createPlacemark(coords) {
    return new ymaps.Placemark(coords, {
        iconCaption: 'Searching...'
    }, {
        preset: 'islands#violetDotIconWithCaption',
        iconLayout: "default#image",
        iconImageHref: "../static/assets/img/orange_pin.png",
        iconImageSize: [50, 50],
        iconImageOffset: [-25, -25]
    });
}

function createPinsInRadius(radius) {
    pinsCollection.removeAll();
    myMap.geoObjects.remove(pinsCollection);
    for (let i = 0; i < event_address.length; i++) {
        let myPlacemark, coords, address = event_address[i].innerHTML;
        if (address !== '') {
            ymaps.geocode(address).then(function (res) {
                    coords = res.geoObjects.get(0).geometry.getCoordinates();
                    if (radius < maxRadius) {
                        if (ymaps.coordSystem.geo.getDistance(coords, user_geo) <= radius) {
                            if ($('#event_type_picker').html() === 'my') {
                                if (event_follow_statuses[i].innerHTML !== 'Following') {
                                    event_address[i].parentElement.style.display = "none";
                                }
                            } else {
                                event_address[i].parentElement.style.display = "inline-block";
                            }
                            myPlacemark = createPlacemark(coords);
                            pinsCollection.add(myPlacemark);

                        } else {
                            event_address[i].parentElement.style.display = "none";
                        }
                    } else {
                        if ($('#event_type_picker').html() === 'my') {
                            if (event_follow_statuses[i].innerHTML !== 'Following') {
                                event_address[i].parentElement.style.display = "none";
                            }
                        } else {
                            event_address[i].parentElement.style.display = "inline-block";
                        }
                        myPlacemark = createPlacemark(coords);
                        pinsCollection.add(myPlacemark);
                    }
                }
            );
        }
    }
    myMap.geoObjects.add(pinsCollection);
}

$(document).ready(function () {
    ymaps.ready(init);
});

function init() {
    myMap = new ymaps.Map('map', {
        center: [55, 55],
        zoom: 9
    });
    pinsCollection = new ymaps.GeoObjectCollection();
    let default_radius = 20000;
    ymaps.geolocation.get({
        provider: 'yandex',
        mapStateAutoApply: true
    }).then(function (result) {
        user_geo = result.geoObjects.get(0).geometry.getCoordinates();
        myMap.setCenter(user_geo);
        radiusZone = new ymaps.Circle([
            user_geo,
            default_radius
        ], {}, {
            fillColor: "#ffffff",
            strokeColor: "#ffb631",
            fillOpacity: 0,
            strokeOpacity: 1,
            strokeWidth: 5
        });
        createPinsInRadius(default_radius);
        myMap.geoObjects.add(radiusZone);
    });

    ymaps.geolocation.get({
        provider: 'auto',
        mapStateAutoApply: true,
        autoReverseGeocode: true
    }).then(function (result) {
        user_geo = result.geoObjects.get(0).geometry.getCoordinates();
    });
}


const $radiusSpan = $('.radiusValue');
const $radiusSlider = $('#radius_slider');
let res;
$radiusSpan.html(Math.floor($radiusSlider.val() / 1000) + " km");
$radiusSlider.on('change', () => {
    res = Math.floor($radiusSlider.val() / 1000);
    $radiusSpan.html(res + " km");
    if (res >= maxRadius / 1000) {
        $radiusSpan.html(res + "+ km");
        radiusZone.geometry.setRadius(100000000);
    } else {
        radiusZone.geometry.setRadius(res * 1000);
    }
});

$('.find_events').click(function () {
    createPinsInRadius(res * 1000);
});

$('#event_type_picker').click(function () {
    if ($(this).html() === 'all') {
        $(this).html('my');
    } else if ($(this).html() === 'my') {
        $(this).html('all');
    }
});