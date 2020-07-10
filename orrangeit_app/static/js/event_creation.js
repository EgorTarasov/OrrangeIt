$(document).ready(function () {
    $("#inputTags").tagging();
    $("#gallery_images").on("change", function () {
        if ($("#gallery_images")[0].files.length > 5) {
            alert("You can select only 5 images for gallery");
            $('#gallery_images').val('');
        }
    });

    // let d = new Date($.now());
    //
    // let begin = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate() + ' ' +
    //     (d.getHours() + 2) + ':' + d.getMinutes();
    // let end = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + (d.getDate() + 1) + ' '
    //     + (d.getHours() + 2) + ':' + d.getMinutes();
    //
    // // $('#event_end').val(end);
    // // $('#event_begin').val(begin);
});
