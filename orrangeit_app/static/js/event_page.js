ymaps.ready(init);
address = document.currentScript.getAttribute('address');

function init() {
    let myPlacemark, coords,
        myMap = new ymaps.Map('map', {
            center: [0, 0],
            zoom: 9
        });

    if (address != '') {
        ymaps.geocode(address).then(function (res) {
            coords = res.geoObjects.get(0).geometry.getCoordinates();
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            myMap.setCenter(coords);
        });
    }

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
}

