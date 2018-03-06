var b1 = document.getElementById("B1");
var b2 = document.getElementById("B2");

b1.onclick = b1_ajax;
b2.onclick = b2_ajax;

var httpRequest_b1;
var httpRequest_b2;

function b1_ajax(e)
{
    var form = document.getElementById("b1-form");
    
    var form_data = new FormData(form);

    httpRequest_b1 = new XMLHttpRequest();
    httpRequest_b1.onreadystatechange = ajax_handle_response;
    httpRequest_b1.open("POST", '/b1');
    httpRequest_b1.send(form_data);
}

function ajax_handle_response() {
    if(httpRequest_b1.readyState == 4 && httpRequest_b1.status == 200) {
        ;
    }

}

function b2_ajax(e)
{
    var form = document.getElementById("b2-form");
    
    var form_data = new FormData(form);

    httpRequest_b2 = new XMLHttpRequest();
    httpRequest_b2.onreadystatechange = ajax_handle_response2;
    httpRequest_b2.open("POST", '/b2');
    httpRequest_b2.send(form_data);
}

function ajax_handle_response2() {
    if(httpRequest_b2.readyState == 4 && httpRequest_b2.status == 200) {
        ;
    }

}