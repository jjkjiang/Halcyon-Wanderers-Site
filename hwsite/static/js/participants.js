$(document).ready(function () {
    $(document).on("click", ".participant-detail", function () {
        const card = $(this).parent().closest('[id]');
        const eventid = card.attr('id');

        $.ajax({
            type: 'POST',
            url: 'participants/',
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
            
            users = JSON.parse(data[0]);
            avatars = JSON.parse(data[1]);
            modal = $('#modalBody').eq(0).empty();


            if (users.length === 0) {
                modal.append(
                    $('<p>').text("Nobody here :(")
                );
                return;
            }

            for (let i = 0; i < users.length; i++) {
                modal.append(
                    $('<li>').append(
                        $('<p>').prepend(
                            $('<img>').attr('src', avatars[i]["fields"]["avatar"]).attr('style', 'height:38px')
                        ).append(" " + users[i]["fields"]["username"])
                    )
                );
            }
        }
    });

    function failure(data, textStatus, jqXHR) {
        alert("failure!" + data)
    }
});