// $(".change-profile-info").click(function () {
//     let fields = $(".changable");
//     if (fields[0].hasAttribute("readonly")) {
//         fields.removeAttr("readonly");
//         $(this).text("Confirm changes");
//     } else {
//         fields.attr("readonly", "readonly");
//         $(this).text("Edit profile");
//     }
// });

$( document ).ready(function() {
    $(".changeable").toggle();
});

$(".change-profile-info").click(function(){
    $(".changeable").toggle();
    $(".non-changeable").toggle();
});
