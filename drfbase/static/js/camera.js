window.onload = function (event) {
    setInterval(function () {
        console.log('timeout');
        $.ajax({
            url: '/camspic/1/',
            success: function (data) {
                $('.image_block_view').html(data.result);
                console.log(`success ${data.result}`);
            }
        })
    }, 2000);
}