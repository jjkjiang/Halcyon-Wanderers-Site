$(document).ready(function () {
    $(document).on("click", ".participant-detail", function () {
        const card = $(this).parent().closest('[id]');
        const eventid = card.attr('id');

        $.ajax({
            type: 'POST',
            url: '/participants/',
            data: {
                'event': eventid,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: UpdateModal,
            error: failure,
            dataType: 'html'
        });

        function UpdateModal(data, textStatus, jqXHR) {
            data = eval(data);

            console.log(data);

            modal = $('#modalBody').eq(0).empty();

            card.find('.attendance-count').eq(0).text(data.length);

            if (data.length === 0) {
                modal.append(
                    $('<p>').text("Nobody here :(")
                );
                return;
            }

            for (let i = 0; i < data.length; i++) {
                modal.append(
                    $('<li>').append(
                        $('<p>').prepend(
                            $('<img>').attr('src', data[i]["avatar"]).attr('style', 'height:38px')
                        ).append(" " + data[i]["username"])
                    )
                );
            }
        }
    });

    function failure(data, textStatus, jqXHR) {
        alert("failure!" + data)
    }
});