var b1 = document.getElementById("B1");
var b2 = document.getElementById("B2");

b1.onclick = b1_ajax;
b2.onclick = b2_ajax;

var httpRequest_b1;
var httpRequest_b2;

var b1_on = true;
var b2_on = true;

function b1_ajax(e)
{
    if(b1_on)
    {
        b1_on = false;
        b1.className = "button open";
    }
    else
    {
        b1_on = true;
        b1.className = "button close";
    }
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
    if(b2_on)
    {
        b2_on = false;
        b2.className = "button open";
    }
    else
    {
        b2_on = true;
        b2.className = "button close";
    }
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