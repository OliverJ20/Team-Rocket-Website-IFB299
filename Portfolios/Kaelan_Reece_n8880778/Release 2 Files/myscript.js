function validate() { //Function which runs all validation functions
	checkFname();
	checkName();
	checkEmail();
	checkPassword();
}

//rules
function displayRules(admin) {
	console.log("rules being displayed?");
	var rule = $('<p>');
	ruleCounter = 0;
	//get data
    $.getJSON( "/admin/rules", function( data ) {
        //create row for each issue
        for (var entry in data.ruleValues) {
			ruleCounter++;
			buttonId = "btn" + ruleCounter;
			updateBtn = "Ubtn" + data.ruleValues[entry]['Rule_ID'];
			deleteBtn = "Ubtn" + data.ruleValues[entry]['Rule_ID'];
			ruleClass = 'ruleInfo' + ruleCounter;
			ruleId = '.' + ruleClass;

			clickStatement = "hide(" + "'" + ruleId  + "'" + "," + "'"+ buttonId + "'" + ")"
			clickDeleteStatement = "deleteRule(" + data.ruleValues[entry]['Rule_ID'] + ")"

			buttonTag = "<button  class = \"expansionContent\" style = \"margin-left:1em\" id = " + buttonId + " onclick=" + clickStatement + ">";
			divStyle = " style=\"display:none;\"";
			divTag = "<div class = " + ruleClass + divStyle + ">";
            var row = $('<div>').attr("id",data.ruleValues[entry]['Rule_ID']);
			row.append($('<h3 style = "display:inline">').html(data.ruleValues[entry]['Rule_Title']));
			row.append($(buttonTag).html("+"));
			if (admin == "True") {
					var link = "/updateRules/"+data.ruleValues[entry]['Rule_ID']
					var updateButton = $('<a href = "'+link+'" id = "'+updateBtn+'">').html('<button  class = \"updateButton\" style = \"margin-left:1em\">Update</button>')
					var deleteButton = $('<button  class = \"updateButton\" onClick = ' + clickDeleteStatement + ' style=\"margin-left:1em\">Delete</button>')
					row.append(updateButton);
					row.append(deleteButton);
			}
			row.append($('<br />').html(""));
			row.append($('<br />').html(""));
			row.append($(divTag).html(data.ruleValues[entry]['Rule_Description']));
			row.append($('<br />').html(""));
            rule.append(row);
        }
    //Populate and show table
    $("#display").html(rule);
})}

function deleteRule(Rule_ID) {
	console.log("rule being deleted?");
	console.log(Rule_ID);
	var rule = $('<p>');
	ruleCounter = 0;

	//get data
    if (confirm("Are you sure you would like to delete this rule?") == true) {
    	$.getJSON( "/admin/rules/delete/" + Rule_ID, function( data ) {
		hideDeletedRule(Rule_ID)
	})}}

function youSure() {
	console.log("Visitor applying");
	$.getJSON("/visitorNotification/", function( data ) {
		if (data.status = "TRUE") {
			alert("A email notification has been sent")
		} else {
			alert("An Error occurred")
		}
		});
		//}
}
function emailOverDue() {
    //Trigger email
    uri = "/overduePayment/"
    $.getJSON(uri, function( data ) {
        if (data.status = "TRUE") {
            alert("A email notification has been sent")
        } else {
            alert("An Error occurred")
        }
    });
}

var showSign;
showSign = "+";
var infoClass;

function hide(infoClass, buttonNum) {
	if ($(infoClass).is(":visible")) {
		$(infoClass).hide();
		showSign = "+";
		document.getElementById(buttonNum).innerHTML = showSign;
	} else {
		$(infoClass).show();
		showSign = "-";
		document.getElementById(buttonNum).innerHTML = showSign;
	}
}

//checks first name
function checkFname() {
    var x = document.forms["register"]["fname"].value; //assign variable x as the value of first name

    if (x == null || x == "") { //checks first name is not left blank
		var errorText = document.getElementById("fname1");
		errorText.innerHTML = "First Name is Required"; //informs user of the error in line
        return false;
	} else if ( x != null || x != "") {	 //if the user corrects the error, the in-line message disappears
		var errorText = document.getElementById("fname1");
		errorText.innerHTML = "";
        return false;
	}
}

//checks username is not left blank
function checkName() {
    var x = document.forms["register"]["user_name"].value; //assigns variable x as the value of username

	if (x == null || x == "") {
		var errorText = document.getElementById("usernameMissing");
		errorText.innerHTML = " username is Required"; //informs user of the error in line
        return false;
    }
	else if ( x != null || x != "") {	 //if the user corrects the error, the in-line message disappears
		var errorText = document.getElementById("usernameMissing");
		errorText.innerHTML = "";
        return false;
	} else {
		return false;
	}
}

//checks email is not left blank
function checkEmail () {
	var y = document.forms["register"]["email"].value;

	if (y == null || y == "") {
		var errorText = document.getElementById("email1");
		errorText.innerHTML = " Email Address is Required"; //informs user of the error in line
        return false;
	} else if ( y != null || y != "") {	 //if the user corrects the error, the in-line error message disappears
		var errorText = document.getElementById("email1");
		errorText.innerHTML = "";
        return false;
	}
}

//checks the password
function checkPassword1() {
	var y = document.forms["register"]["password1"].value; //assigns variable y to the value of password

	if (y == null || y == "") {  //checks password is not left blank
		var errorText = document.getElementById("passWord1");
		errorText.innerHTML = " Password is Required"; //informs user of the error in line
        return false;
	} else if ( y != null || y != "") {	//if the user corrects the error, the in-line message disappears
		var errorText = document.getElementById("passWord1");
		errorText.innerHTML = "";
        return false;
	}
}

//checks confirm password matches password
function checkPassword2() {
	var y = document.forms["register"]["password1"].value; //assigns variable y to the value of password
	var z = document.forms["register"]["password2"].value; //assigns variable z to the value of confirm password

	if ( z == null || z == "") {	//checks confirm password is not left blank
		var errorText = document.getElementById("passWord2");
		errorText.innerHTML = " Confirm Password is Required"; //if the user corrects the error, the in-line message disappears
        return false;
	} else if (y != z) { //checks whether password and confirm password match
		var errorText = document.getElementById("passWord2");
		errorText.innerHTML = " Passwords do not match";  //informs user of the error in line
		return false;
	} else if (y == z) {
		var errorText = document.getElementById("passWord2");
		errorText.innerHTML = ""; //if the user corrects the error, the in-line message disappears
		return false;
	}
}

var showSign;
showSign = "+";
var infoClass;

function hide(infoClass, buttonNum) {
	if ($(infoClass).is(":visible")) {
		$(infoClass).hide();
		showSign = "+";
		document.getElementById(buttonNum).innerHTML = showSign;
	} else {
		$(infoClass).show();
		showSign = "-";
		document.getElementById(buttonNum).innerHTML = showSign;
	}
}

function hideDeletedRule(id) {
	$("#"+ id).hide();
	console.log(id + "deleted");
}

//shows all the form information for parking
function parkingHide(){
	$(".parking").hide(1000);
}

//hides all the form informatino for parking
function parkingShow(){
	$(".parking").show(1000);
}

//shows the entire form
function formShow(){
	$("#hideForm").show(1000);
}

//hides the entire form
function formHide(){
	$("#hideForm").hide(1000);
}

//hides the push to remove empty page space
function pushHide(){
	$(".push").hide(1000);
}

//activates the push so that the footer and page content is not misplaced
function pushShow(){
	$(".push").show(1000);
}