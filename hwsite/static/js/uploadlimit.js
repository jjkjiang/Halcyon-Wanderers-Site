$(document).ready(function () {
    const uploadField = document.getElementById("id_image");

    uploadField.onchange = function () {
        if (this.files[0].size > 10000000) {
            alert("File too big!" +
                "" +
                "Uploads are currently limited to 10MB");
        }

        console.log(this.files[0].size)
    };
});