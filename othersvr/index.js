
function out(msg) {
    $('#out').html( $('#out').html() + "<li>" + msg + "</li>" );
}
function str(msg) {
    return JSON.stringify(msg);
}

////////////////////////

function login() {
    out("Start login...");
    var data = {username:$('#u1').val(),password:$('#p1').val()};
    var r = $.getJSON('http://localhost:8080/auth/login',data)
	.done(function(a) {
		out( "second success" + str(a));
		if (a.success===false) {
		    out("FAIL");
		} else {
		    out("SUCCEED");
		}
	    })
	.fail(function(a) {
		out( "error"+str(a) );
	    })
	.always(function(a,b,c) {
		out( "finished"+str(a) );
		out( "finished"+str(b) );
		out( "finished"+str(c) );
	    })
	;
    out("Ajax request sent..." + str(r));
}

function register() {
    out("Start register...");

    var data = {username:$('#u2').val(),password:$('#p2').val(),email_address:$('#e2').val()};
    var r = $.getJSON('http://localhost:8080/auth/register',data)
	.done(function(a) {
		out( "second success" + str(a));
		if (a.success===false) {
		    out("FAIL");
		} else {
		    out("SUCCEED");
		}
	    })
	.fail(function(a) {
		out( "error"+str(a) );
	    })
	.always(function(a,b,c) {
		out( "finished"+str(a) );
		out( "finished"+str(b) );
		out( "finished"+str(c) );
	    })
	;
    out("Ajax request sent..." + str(r));
}

function forgot() {
    out("Start forgot...");

    var data = {username:$('#u3').val(),email_address:$('#e3').val()};
    var r = $.getJSON('http://localhost:8080/auth/reset_password',data)
	.done(function(a) {
		out( "second success" + str(a));
		if (a.success===false) {
		    out("FAIL");
		} else {
		    out("SUCCEED");
		}
	    })
	.fail(function(a) {
		out( "error"+str(a) );
	    })
	.always(function(a,b,c) {
		out( "finished"+str(a) );
		out( "finished"+str(b) );
		out( "finished"+str(c) );
	    })
	;
    out("Ajax request sent..." + str(r));
}

////////////////////////

function main() {
    out("OK, Ready!");
}

$(main);
