$(document).ready(function () {
    const notificationSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/notifications/'
    );

    notificationSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(window.location.host + '/' + 'event/' + data.event_id);
        // Capitalizing the first letter of event name
        data.event_name = "«" + data.event_name.charAt(0).toUpperCase() + data.event_name.slice(1) + "»"
        Push.Permission.request();
        Push.create(data.event_name + ' starts ' + data.when, {
            icon: "../static/assets/img/orange_pin.png",
            body: "Event " + data.event_name + ' begins at ' + data.event_time_begin + ". Don`t miss it!",
            link: window.location.host + '/' + 'event/' + data.event_id,
            timeout: 5000,               // Timeout before notification closes automatically.
            vibrate: [100, 100, 100],    // An array of vibration pulses for mobile devices.
            onClick: function () {
                //window.open(window.location.host + '/' + 'event/' + data.event_id, '_blank');
            }
        });
    };

    notificationSocket.onclose = function (e) {
        console.error('Whoops, notifications socket closed unexpectedly');
    };
});