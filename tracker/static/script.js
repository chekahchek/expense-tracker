$(document).ready(function(){
    var pathname = window.location.pathname.split('/');
    var pathLength = pathname.length;
    if (pathLength == 2) { /*Pathname = 2 refers to the main landing page for trip list view*/
        $('#addModal').text("Add trip");
        $('#addDataLabel').text("Add trip");
    }
    else if (pathname.includes('blog')){
        //pass
    }
    else {
        $('#addModal').text("Add expense");
        $('#addDataLabel').text("Add expense");
    }
})


$(".fa-trash-alt").on("click", function(e){
    e.preventDefault();
    var $this = $(this);
    $("#deleteModalBody").attr("action", $this.attr('href'))
    $("#deleteData").modal("show");
    return false;
});


$(".fa-edit").on("click", function(e){
    var pathname = window.location.pathname.split('/');
    var pathLength = pathname.length;
    if (pathname.includes('blog')) {
        //pass
    }
    else {
        e.preventDefault();
        var $this = $(this);
        if (pathLength == 2) {
            var title = $this.parents(".record").find('td').eq(0).text();
            var budget = $this.parents(".record").find('td').eq(1).text();
            var depart_date = $this.parents(".record").find('td').eq(2).text();
            var return_date = $this.parents(".record").find('td').eq(3).text();
            $("#editModalBody input[name='title']").val(title)
            $("#editModalBody input[name='budget']").val(budget)
            $("#editModalBody input[name='depart_date']").val(depart_date)
            $("#editModalBody input[name='return_date']").val(return_date)
            $("#editModalBody").attr("action", $this.attr('href'))
            $("#editData").modal("show");
            return false;
        }
        else {
            let description = $this.parents(".record").find('td').eq(0).text();
            let expense = $this.parents(".record").find('td').eq(1).text();
            let expense_type = $this.parents(".record").find('td').eq(2).text();
            let transaction_date = $this.parents(".record").find('td').eq(3).text();
            $("#editModalBody input[name='description']").val(description)
            $("#editModalBody input[name='expense']").val(expense)
            $("#editModalBody select[name='expense_type']").val(expense_type)
            $("#editModalBody input[name='transaction_date']").val(transaction_date)
            $("#editModalBody").attr("action", $this.attr('href'))
            $("#editData").modal("show");
            return false;
        }
    }
}
);


$("#editModalBody").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation();
    var $this = $(this);
    var pathname = window.location.pathname.split('/');
    var pathLength = pathname.length;

    if (pathLength == 2){
        $.ajax({
            url : $this.attr("action"),
            type : "POST",
            data : {
                title: $("#editModalBody input[name='title']").val(),
                budget : $("#editModalBody input[name='budget']").val(),
                depart_date : $("#editModalBody input[name='depart_date']").val(),
                return_date : $("#editModalBody input[name='return_date']").val(),
                csrfmiddlewaretoken:$("#editModalBody input[name='csrfmiddlewaretoken']").val()
            },
            dataType : "json",
            success : function(resp){
                if (resp.message == "success"){
                    $("#editData").modal("hide");
                    window.location.reload();
                }else{
                    console.log(resp.message);
                }
            }
        })
    }
    else {
        $.ajax({
            url : $this.attr("action"),
            type : "POST",
            data : {
                description: $("#editModalBody input[name='description']").val(),
                expense : $("#editModalBody input[name='expense']").val(),
                expense_type : $("#editModalBody select[name='expense_type']").val(),
                transaction_date : $("#editModalBody input[name='transaction_date']").val(),
                csrfmiddlewaretoken:$("#editModalBody input[name='csrfmiddlewaretoken']").val()
            },
            dataType : "json",
            success : function(resp){
                if (resp.message == "success"){
                    $("#editData").modal("hide");
                    window.location.reload();
                }else{
                    console.log(resp.message);
                }
            }
        })
    }

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