$(document).ready(function(){
    //set health as first active
    $("#Health").addClass('active');
    $("#Health").addClass('btn-success');

    //Populate table
    healthTable();

});

//Switch radio Buttons
$(document).on('click.bs.radio', '.btn-radio > .btn', function(e) {
    //Remove active and colour
    $(this).siblings().removeClass('active');
    $(this).siblings().removeClass('btn-success');
    //Add active and colour
    $(this).addClass('active');
    $(this).addClass('btn-success');

    //hide table and switch
    $("#table").fadeOut( function() {
        switch (e.target.id) {
            case "Health":
                healthTable();
                break;
            case "Parking":
                parkingTable();
                break;
            case "Other":
                smokingTable();
                break;
        };
    });

    $("#table").fadeIn(500);
});

//generate Health and Safety table
function healthTable() {
    //set title
    $("#title").html("Health and Safety Violations");

    //new table
    var table = $('<table>');

    //Table heading
    var header = $('<tr>');
    header.append($('<th style="width:20px; text-align: center;">').html("ID"));
    header.append($('<th style="width:40px; text-align: center;">').html("Date"));
    header.append($('<th style="width:40px; text-align: center;">').html("Time"));
    header.append($('<th style="width:50px; text-align: center;">').html("Person Name"));
    header.append($('<th style="width:50px; text-align: center;">').html("Department"));
    header.append($('<th style="width:50px; text-align: center;">').html("Location"));
    header.append($('<th style="width:30px; text-align: center;">').html("Supervisor"));
    header.append($('<th style="width:30px; text-align: center;">').html("Status"));

    table.append(header);

    //get data
    $.getJSON( "/admin/health/", function( data ) {
        //create row for each issue
        for (var entry in data.issues) {
            var row = $('<tr>').attr("id",data.issues[entry]['Issue_Number']);
            //Link to edit entry
            //var link = "/editHealth/"+data.issues[entry]['Issue_Number'];
            //row.append($('<td align="center" style="height:30px;">').html('<a href="'+link+'">'+data.issues[entry]['Issue_Number']+'</a>'));
            row.append($('<td align="center" style="height:30px;">').html(data.issues[entry]['Issue_Number']));
            row.append($('<td align="center">').html(data.issues[entry]['Date']));
            row.append($('<td align="center">').html(data.issues[entry]['Time']));
            row.append($('<td align="center">').html(data.issues[entry]['Person_Name']));
            row.append($('<td align="center">').html(data.issues[entry]['Department']));
            row.append($('<td align="center">').html(data.issues[entry]['Place_in_campus']));
            row.append($('<td align="center">').html(data.issues[entry]['Supervisor']));
            if (data.issues[entry]['Resolution_Date'] == null) {
                row.append($('<td align="center" style="height:20px;">').html('Pending'));
            } else {
                row.append($('<td align="center" style="height:20px;">').html('Complete'));
            };

            table.append(row);
        }
    });

    //Populate and show table
    $("#display").html(table);
};

//generate Parking violation table
function parkingTable() {
    //set title
    $("#title").html("Parking Violations");

    //new table
    var table = $('<table>');

    //Table heading
    var header = $('<tr>');
    header.append($('<th style="width:20px; text-align: center;">').html("ID"));
    header.append($('<th style="width:20px; text-align: center;">').html("Date"));
    header.append($('<th style="width:20px; text-align: center;">').html("Time"));
    header.append($('<th style="width:20px; text-align: center;">').html("Description"));
    header.append($('<th style="width:20px; text-align: center;">').html("Vehicle Type"));
    header.append($('<th style="width:20px; text-align: center;">').html("Vehicle License number"));

    table.append(header);

    //get data
    $.getJSON( "/admin/parking/", function( data ) {
        //create row for each issue
        for (var entry in data.issues) {
            var row = $('<tr style="cursor: pointer;">').attr("id",data.issues[entry]['Citation_Number']);
            //var link = "/editParking/"+data.issues[entry]['Citation_Number'];
            //row.append($('<td align="center" style="height:30px;">').html('<a href="'+link+'">'+data.issues[entry]['Citation_Number']+'</a>'));
            row.append($('<td align="center" style="height:30px;">').html(data.issues[entry]['Citation_Number']));
            row.append($('<td align="center">').html(data.issues[entry]['Date']));
            row.append($('<td align="center">').html(data.issues[entry]['Time']));
            row.append($('<td align="center">').html(data.issues[entry]['Description']));
            row.append($('<td align="center">').html(data.issues[entry]['Vehicle_Type']));
            row.append($('<td align="center">').html(data.issues[entry]['Vehicle_License_number']));

            table.append(row);
        }
    });

    //Populate and show table
    $("#display").html(table);
};

//generate Smoking and other violation table
function smokingTable() {
    //set title
    $("#title").html("Other Violations");

    //new table
    var table = $('<table>');

    //Table heading
    var header = $('<tr>');
    header.append($('<th style="width:20px; text-align: center;">').html("ID"));
    header.append($('<th style="width:20px; text-align: center;">').html("Type"));
    header.append($('<th style="width:20px; text-align: center;">').html("Date"));
    header.append($('<th style="width:20px; text-align: center;">').html("Time"));
    header.append($('<th style="width:20px; text-align: center;">').html("Description"));
    header.append($('<th style="width:20px; text-align: center;">').html("Location"));
    header.append($('<th style="width:20px; text-align: center;">').html("Department"));
    header.append($('<th style="width:20px; text-align: center;">').html("Supervisor"));

    table.append(header);

    //get data
    $.getJSON( "/admin/other/", function( data ) {
        //create row for each issue
        for (var entry in data.issues) {
            var row = $('<tr style="cursor: pointer;">').attr("id",data.issues[entry]['Citation_Number']);
            //var link = "/editOther/"+data.issues[entry]['Citation_Number'];
            //row.append($('<td align="center" style="height:30px;">').html('<a href="'+link+'">'+data.issues[entry]['Citation_Number']+'</a>'));
            row.append($('<td align="center" style="height:30px;">').html(data.issues[entry]['Citation_Number']));
            row.append($('<td align="center">').html(data.issues[entry]['Violation_Type']));
            row.append($('<td align="center">').html(data.issues[entry]['Date']));
            row.append($('<td align="center">').html(data.issues[entry]['Time']));
            row.append($('<td align="center">').html(data.issues[entry]['Description']));
            row.append($('<td align="center">').html(data.issues[entry]['Place_in_campus']));
            row.append($('<td align="center">').html(data.issues[entry]['Department']));
            row.append($('<td align="center">').html(data.issues[entry]['Supervisor']));

            table.append(row);
        }
    });

    //Populate and show table
    $("#display").html(table);
};

function showTable() {
    $("#table").show(800);
}
