 <div id="table">
                    <div align="center">
                        </br>
                        </br>
                        <select id="field"></select>
                        <input type="text" id="value" maxlength="30"> </input>
                        <button id="search" class="btn" onclick="filter()">Search</button>
                        <button id="search" class="btn" onclick="reset()">Clear</button>
                    </div>
                    <h1 align="center" id="title"></h1>
                    <br>
                    <table id="display">
                    </table>
                </div>

function searchComboHealth() {
    var options = {"ID": 0,
      "Date": 1,
      "Time": 2,
      "Location": 3,
      "Violator": 4,
      "Status": 5
    };
    $("#field").empty(); // remove old options
    $.each(options, function(key,value) {
      $("#field").append($("<option></option>")
         .attr("value", value).text(key));
    });
}

function searchComboParking() {
    var options = {"ID": 0,
      "Date": 1,
      "Time": 2,
      "Vehicle License number": 3,
      "Permit": 4,
      "Status": 5
    };

    $("#field").empty(); // remove old options
    $.each(options, function(key,value) {
      $("#field").append($("<option></option>")
         .attr("value", value).text(key));
    });
}

function searchComboOther() {
    var options = {"ID": 0,
      "Type": 1,
      "Date": 2,
      "Time": 3,
      "Location": 4,
      "Status": 5
    };

    $("#field").empty(); // remove old options
    $.each(options, function(key,value) {
      $("#field").append($("<option></option>")
         .attr("value", value).text(key));
    });
}

function searchComboUsers() {
    var options = {"ID": 0,
      "Name": 1,
      "Email": 2,
      "Account Type": 3,
    };

    $("#field").empty(); // remove old options
    $.each(options, function(key,value) {
      $("#field").append($("<option></option>")
         .attr("value", value).text(key));
    });
}

function filter() {
    var field = $("#field").find(":selected").val();
    var value = $("#value").val();

    reset();

    var MyRows = $('#display').find('tbody').find('tr');
    for (var i = 1; i < MyRows.length; i++) {

        if ($(MyRows[i]).find('td:eq('+String(field)+')').text() != String(value)) {
            $(MyRows[i]).hide();
        }
    }
}

function reset(){
    $("#value").val(""); // remove old options
    var MyRows = $('#display').find('tbody').find('tr');
    for (var i = 1; i < MyRows.length; i++) {
        $(MyRows[i]).show();
    }
}
