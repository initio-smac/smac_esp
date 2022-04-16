var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
     if (this.readyState == 4) {
        document.getElementById("id_loader").style.display = "none";
        if(this.status == 200) {
            var result = this.responseText;
            try {
                  console.log("res");
                  console.log(result);
                  var jd = JSON.parse(result);
                  document.getElementById('id_version').innerHTML = jd.version;
                  document.getElementById('id_device').innerHTML = jd.id_device;
                  document.getElementById('id_text_name_device').value = jd.name_device;
                  document.getElementById('id_text_pin_device').value = jd.pin_device;
                  if(jd.hasOwnProperty('input_type')){
                        var ip_type = jd["input_type"]
                        if(ip_type == "switch") {
                            document.getElementById('id_ip_sel_switch').checked = true;
                        } else if(ip_type == "pushbutton") {
                            document.getElementById('id_ip_sel_pushbtn').checked = true;
                        } else {
                            document.getElementById('id_ip_sel_switch').checked = true;
                        }
                  } else {
                    document.getElementById('id_ip_sel_switch').checked = true;
                    //document.getElementById('id_ip_sel_pushbtn').checked = false;
                  }

            } catch(err) {
                console.log(err);
            }
        } else {
          console.log(this.status);
          console.log(this.statusText)
        }
     }
};
xhttp.open("GET", "/load_config", true);
xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
document.getElementById("id_loader").style.display = "block";
xhttp.send();

document.getElementById("id_select_input_type").onclick = function(){
   var ip_type = "switch";
   if(document.getElementById('id_ip_sel_switch').checked) {
       ip_type = "switch";
   }else if(document.getElementById('id_ip_sel_pushbtn').checked) {
       ip_type = "pushbutton";
   }
    var data = {}
    data["input_type"] = ip_type
    rest_call(url="/update_input_type", method="GET", data=data, refresh_on_success=true)
};


document.getElementById("id_update_name_device").onclick = function(){
    var data = {}
    data["name_device"] = document.getElementById("id_text_name_device").value;
    console.log(data)
    rest_call(url="/update_name_device", method="GET", data=data, refresh_on_success=true)
};

document.getElementById("id_update_pin_device").onclick =function(){
    var data = {}
    data["pin_device"] = document.getElementById("id_text_pin_device").value;
    console.log(data)
    rest_call(url="/update_pin_device", method="GET", data=data)
};

document.getElementById("id_restart").onclick = function(){
      console.log("restarting...");
      showInfo("Restarting Device...")
      data = {}
      //data["mode"] = document.getElementById("id_set_mode").value;
      data["mode"] = 0
      rest_call(url="/restart", method="GET", data=data, refresh_on_success=true)
  };