function changeHandler(input_value) {
    const username = $(input_value).serialize();
    $.ajax("/show", {
        type: "post",
        data: username,
        dataType: "json",
    }).done(function (data) { 
        const message = JSON.parse(data.values).message
        $("#word").html(message);
    })
}