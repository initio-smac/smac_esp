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
                      var connected_ssid = jd["connected_ssid"]
                      var strength = jd["connected_ssid_strength"]
                      if( connected_ssid == jd.wifi_config_1["ssid"]) {
                        var conn = document.getElementById("id_conn1");
                        conn.style.color = "green";
                        conn.innerHTML = conn.innerHTML + " ("+ strength + "%) ";
                      }
                      document.getElementById('id_ap_ssid').value = jd.ap_config["ssid"];
                      document.getElementById('id_ap_password').value = jd.ap_config["password"];
                      document.getElementById('id_wifi_ssid_1').value = jd.wifi_config_1["ssid"];
                      document.getElementById('id_wifi_password_1').value = jd.wifi_config_1["password"];
                      if( connected_ssid == jd.wifi_config_2["ssid"]) {
                        var conn = document.getElementById("id_conn2");
                        conn.style.color = "green";
                        conn.innerHTML = conn.innerHTML + " ("+ strength + "%) ";
                      }
                      document.getElementById('id_wifi_ssid_2').value = jd.wifi_config_2["ssid"];
                      document.getElementById('id_wifi_password_2').value = jd.wifi_config_2["password"];
                      document.getElementById('id_text_name_device').value = jd.name_device;
                      document.getElementById('id_text_pin_device').value = jd.pin_device;

                      
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



  document.getElementById("id_wifi_submit_1").onclick = function(){
      var ssid = document.getElementById("id_wifi_ssid_1").value;
      var password = document.getElementById("id_wifi_password_1").value;
      var data = {}
      data["ssid"] = ssid
      data["password"] = password
      data["connection"] = 1
      rest_call(url="/update_wifi", method="GET", data=data, refresh_on_success=true)
  };

  document.getElementById("id_wifi_submit_2").onclick = function(){
      var ssid = document.getElementById("id_wifi_ssid_2").value;
      var password = document.getElementById("id_wifi_password_2").value;
      var data = {}
      data["ssid"] = ssid
      data["password"] = password
      data["connection"] = 2
      rest_call(url="/update_wifi", method="GET", data=data, refresh_on_success=true)
  };

  document.getElementById("id_ap_submit").onclick = function(){
      var ssid = document.getElementById("id_ap_ssid").value;
      var password = document.getElementById("id_ap_password").value;
      var data = {}
      data["ssid"] = ssid
      data["password"] = password
      rest_call(url="/update_wifi_ap", method="GET", data=data, refresh_on_success=true)
  };