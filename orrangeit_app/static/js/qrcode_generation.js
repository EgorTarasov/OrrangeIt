text = document.currentScript.getAttribute('text');
tg_link = document.currentScript.getAttribute('tg_link');

new QRCode("output", {
            text: text,
            width: 177,
            height: 177,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
        });

new QRCode("tg_link_qr", {
            text: tg_link,
            width: 177,
            height: 177,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
        });