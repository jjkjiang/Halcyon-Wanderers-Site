$(document).ready(function () {
    const uploadField = document.getElementById("id_image");

    uploadField.onchange = function () {
        if (this.files[0].size > 1000000) {
            alert("File too big!" +
                "" +
                "Uploads are currently limited to 1MB");
        }

        console.log(this.files[0].size)
    };
});