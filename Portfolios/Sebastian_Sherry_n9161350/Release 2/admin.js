//Generate User table
function usersTable() {
    //disable add button
    setAddUser();

    //set title
    $("#title").html("Users");

    //new table
    var table = $('<table>');

    //Table heading
    var header = $('<tr>');
    header.append($('<th style="width:20px; text-align: center;">').html("ID"));
    header.append($('<th style="width:20px; text-align: center;">').html("Name"));
    header.append($('<th style="width:20px; text-align: center;">').html("Email"));
    header.append($('<th style="width:20px; text-align: center;">').html("Account Type"));

    table.append(header);

    //get data
    $.getJSON( "/admin/users/", function( data ) {
        //create row for each issue
        for (var entry in data.users) {
            var row = $('<tr style="cursor: pointer;">').attr("id",data.users[entry]['User_ID']);
            row.append($('<td align="center" style="height:30px;">').html(data.users[entry]['User_ID']));
            row.append($('<td align="center">').html(data.users[entry]['Name']));
            row.append($('<td align="center">').html(data.users[entry]['Email']));
            row.append($('<td align="center">').html(data.users[entry]['Account_Type']));
            table.append(row);
        }
    });

    //Populate and show table
    $("#display").html(table);
};

//Send email for pending Fines
function emailPending(id) {
    //Trigger email
    uri = "/remindPayment/"+id;
    $.getJSON(uri, function( data ) {
        if (data.status = "TRUE") {
            alert("A email notification has been sent")
        } else {
            alert("An Error occurred")
        }
    });
}

//Send email for overdue Fines
function emailOverDue(id) {
    //Trigger email
    uri = "/overduePayment/"+id;
    $.getJSON(uri, function( data ) {
        if (data.status = "TRUE") {
            alert("A email notification has been sent")
        } else {
            alert("An Error occurred")
        }
    });
}
