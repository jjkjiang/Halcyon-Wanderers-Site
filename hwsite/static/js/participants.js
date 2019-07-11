$(document).ready(function () {
    $(document).on("click", ".participant-detail", function () {
        const card = $(this).parent().closest('[id]');
        const eventid = card.attr('id');

        $.ajax({
            type: 'POST',
            url: '/events/participants/',
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

            modal = $('#modalBody')
                .eq(0).empty()
                .addClass('list-group')
                .addClass('list-group-flush');

            card.find('.attendance-count').eq(0).text(data.length);

            if (data.length === 0) {
                modal.append(
                    $('<p>').text("Nobody here :(")
                );
                return;
            }

            for (let i = 0; i < data.length; i++) {
                let li = $('<li>')
                    .addClass('list-group-item')
                    .attr('style', 'width:100%;')
                    .appendTo(modal);
                let context = $('<p>');

                let img = $('<img>')
                    .addClass('img-responsive')
                    .attr('src', data[i]["avatar"])
                    .attr('style', 'height:38px;')
                    .appendTo(context);

                context.append(" " + data[i]["username"]);

                if (card.hasClass("hasrole")) {
                    context.append(":   ");

                    let icon = $('<img>')
                        .addClass('img-responsive')
                        .attr('src', data[i]["roleicon"])
                        .attr('style', 'height:30px;')
                        .appendTo(context);

                    context.append(data[i]["role"]);
                }

                context.appendTo(li);
            }
        }
    });

    function failure(data, textStatus, jqXHR) {
        alert("failure!" + data);
    }
});