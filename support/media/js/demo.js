var SELECTED_COMMENT_FORM;
var MODAL_OPEN = false;

$(document).ready(function () {

    $(".rsvp-modal").on("click", function () {
        var campaignId = $(this).parent().parent().find("[data-campaign-id]").attr("data-campaign-id");
        $("#rsvp-form").attr("action", "/campaign/rsvp/" + campaignId + "/");
    });

    $(".commentForm").on("submit", function (evt) {
        if (MODAL_OPEN) {
            return;
        }
        evt.preventDefault();
        if ($(this).find(".commentInput").val() == "") {
            return;
        }
        SELECTED_COMMENT_FORM = this;
        $("#comment-modal").modal('show');
        MODAL_OPEN = true;
    });

    $("#comment-name-form").on("submit", function (evt) {
        evt.preventDefault();

        var name = $("#name").val();
        $(SELECTED_COMMENT_FORM).find(".commentUserName").val(name);
        $(SELECTED_COMMENT_FORM).submit()
    });

    $("#comment-modal").on('hidden', function () {
        MODAL_OPEN = false;
    })

});