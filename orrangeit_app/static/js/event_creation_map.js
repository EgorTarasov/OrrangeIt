ymaps.ready(init);

function init() {
    let suggestView = new ymaps.SuggestView('address_suggest');
    let myPlacemark,
        myMap = new ymaps.Map('map', {
            center: [55.653994, 37.622093],
            zoom: 10
        });
    // Слушаем клик на карте.
    myMap.events.add('click', function (e) {
        let coords = e.get('coords');
        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        } else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        myMap.setCenter(coords);
        getAddress(coords);
    });

    let address_input = document.getElementById('address_suggest');
    address_input.oninput = function () {
        if (address_input.value != '') {
            ymaps.geocode(address_input.value).then(function (res) {
                    coords = res.geoObjects.get(0).geometry.getCoordinates();
                    if (myPlacemark) {
                        myPlacemark.geometry.setCoordinates(coords);
                    } else {
                        myPlacemark = createPlacemark(coords);
                        myMap.geoObjects.add(myPlacemark);
                        myPlacemark.events.add('dragend', function () {
                            getAddress(myPlacemark.geometry.getCoordinates());
                        });
                    }
                    myMap.setCenter(coords);
                    myPlacemark.properties
                        .set({
                            iconLayout: "default#image",
                            iconImageHref: "../static/assets/img/orange_pin.png",
                            iconImageSize: [50, 50],
                        });
                },
            );
        }
    };


    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'Searching...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true,
            iconLayout: "default#image",
            iconImageHref: "../static/assets/img/orange_pin.png",
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        ymaps.geocode(coords).then(function (res) {
            let firstGeoObject = res.geoObjects.get(0);
            myPlacemark.properties
                .set({
                    iconLayout: "default#image",
                    iconImageHref: "../static/assets/img/orange_pin.png",
                    iconImageSize: [50, 50],
                });
            document.getElementById("address_suggest").value = firstGeoObject.getAddressLine();
        });
    }
}

