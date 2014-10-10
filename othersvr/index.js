
function out(msg) {
    $('#out').html( $('#out').html() + "<li>" + msg + "</li>" );
}
function str(msg) {
    return JSON.stringify(msg);
}

////////////////////////

var _offset = 0;

function dd() {
    var d = new Date();
    return '' + d + '::' + (d.getTime()*1000) + (++offset);
}

var _hasOutstandingRequests = false;

function login() {
    out("Start login..." + dd());
    if (_hasOutstandingRequests) {
	out("Quit login (overlap)");
	return;
    }
    _hasOutstandingRequests = true;
    var data = {username:$('#u1').val(),password:$('#p1').val()};
    var r = $.getJSON('http://localhost:8080/auth/login',data)
	.done(function(a) {
		out("Start login3..." + dd());
		out( "second success" + str(a));
		if (a.success===false) {
		    out("FAIL");
		} else {
		    out("SUCCEED");
		}
	    })
	.fail(function(a) {
		out("Start login4..." + dd());
		out( "error"+str(a) );
	    })
	.always(function(a,b,c) {
		_hasOutstandingRequests = false;
	    })
	;
    out("Ajax request sent..." + str(r));
    out("Start login2..." + dd());
}

function register() {
    out("Start register...");
    if (_hasOutstandingRequests) {
	out("Quit login (overlap)");
	return;
    }
    _hasOutstandingRequests = true;
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
		_hasOutstandingRequests = false;
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
