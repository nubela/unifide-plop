$(document).ready(function () {
    $(".rsvp-modal").on("click", function () {
        var campaignId = $(this).parent().parent().find("[data-campaign-id]").attr("data-campaign-id");
        $("#rsvp-form").attr("action", "/campaign/rsvp/" + campaignId + "/");
    });
});