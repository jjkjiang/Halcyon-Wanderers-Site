$(document).ready(function () {
    $(document).on("click", ".attend", function () {
        const card = $(this).closest('[id]');
        const eventid = card.attr('id');

        $.ajax({
            type: 'POST',
            url: '/attendance/going/',
            data: {
                'event': eventid,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: UpdateAttendance,
            error: failure,
            dataType: 'html'
        });

        function UpdateAttendance(data, textStatus, jqXHR) {
            const button = card.find('.btn').eq(0);
            button.text("Success!");
            button.removeClass('attend');
            button.addClass('cancel-attend');
            button.removeClass('btn-warning');
            button.addClass('btn-success');

            const attendance_count = card.find('.attendance-count').eq(0);
            const number = parseInt(attendance_count.text()) + 1;
            attendance_count.text(number);
        }
    });

    $(document).on("click", ".cancel-attend", function () {
        const card = $(this).closest('[id]');
        const eventid = card.attr('id');

        $.ajax({
            type: 'POST',
            url: '/attendance/cancel/',
            data: {
                'event': eventid,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: UpdateAttendance,
            error: failure,
            dataType: 'html'
        });

        function UpdateAttendance(data, textStatus, jqXHR) {
            const button = card.find('.btn').eq(0);
            button.text("Cancelled!");
            button.removeClass('cancel-attend');
            button.addClass('attend');
            button.removeClass('btn-success');
            button.addClass('btn-warning');

            const attendance_count = card.find('.attendance-count').eq(0);
            const number = parseInt(attendance_count.text()) - 1;
            attendance_count.text(number);
        }
    });

    function failure(data, textStatus, jqXHR) {
        alert("failure!" + data)
    }
});