$(document).ready(function () {
    $('#form').submit(function (event) {
        event.preventDefault();
        $('#modalConfirm').modal({
            backdrop: 'static',
            keyboard: false
        });
        $('#confirm').click(function () {
            let tags = $('#inputTags').tagging("getTags");
            $('#tagsField').val(tags.join(' '));

            let inputRegExp = /^[0-9a-zA-Zа-яА-Я-\s]+$/;

            if ($('#event_name').val().match(inputRegExp)) {
                const telegramSocket = new WebSocket(
                    'ws://'
                    + window.location.host
                    + '/ws/tg_group_creator/'
                    + $('#event_name').val().split(' ').join('_')
                    + '/'
                );

                telegramSocket.onmessage = function (e) {
                    const data = JSON.parse(e.data);
                    //alert(data.telegram_group_link);
                    $('#telegramGroupLinkField').val(data.telegram_group_link);
                    $('#form').unbind('submit').submit();
                };

                telegramSocket.onclose = function (e) {
                    console.error('Whoops, telegram group could not be created due to an error');
                    $('#form').unbind('submit').submit();
                };
            } else {
                alert("No special symbols in event name, sorry(")
            }
        });
    });
});