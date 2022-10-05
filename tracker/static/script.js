$(".fa-trash-alt").on("click", function(e){
    e.preventDefault();
    var $this = $(this);
    $("#deleteModalBody").attr("action", $this.attr('href'))
    $("#deleteData").modal("show");
    return false;
});


$("#deleteModalBody").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);

    $.ajax({
        url : $this.attr("action"),
        type : "POST",
        data: {csrfmiddlewaretoken:$("#deleteModalBody input[name='csrfmiddlewaretoken']").val()},
        dataType : "json",
        success : function(resp){
            if (resp.message == "success"){
                $("#deleteData").modal("hide");
                window.location.reload();
            }else{
                console.log(resp.message);
            }
        }
    })

});