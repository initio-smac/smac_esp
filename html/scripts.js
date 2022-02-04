    var DATA = {};
    var id_info = document.getElementById("id_info")

    function showInfo(text) {
        document.getElementById("id_info_wrapper").style.display = "block";
        document.getElementById("id_info").innerHTML = text;
    }

    function hideInfo() {
        document.getElementById("id_info_wrapper").style.display = "none";
        document.getElementById("id_info").innerHTML = "";
    }


   function rest_call(url, method="GET", data={}, refresh_on_success=true) {
        document.getElementById("id_loader").style.display = "block";
        if(method == "POST"){
            data = JSON.stringify( data );
        }
        var params = [];
        for(var k in data) {
            params.push(k + "=" + data[k]);
        }
        params = params.join("&")
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
             if (this.readyState == 4) {
                document.getElementById("id_loader").style.display = "none";
                if(this.status == 200) {
                    var result = this.responseText;
                    alert(this.responseText);
                    if(url == "/check_for_update") {
                        //document.getElementById("id_download_update").style.display = "block";
                        //id_info.innerHTML = "New Update is available.";
                        var resp = JSON.parse(result);
                        if(resp["resp_code"] == 1) {
                            var download = confirm("New Update Available. Download Now?");
                            if(download) {
                                document.getElementById("id_download_update").style.display = "block";
                            }
                        } else if(resp["resp_code"] == 0) {
                            alert(resp["text"])
                        } else {
                            alert(resp["text"])
                        }

                    } else if( refresh_on_success ) {
                        location.reload();
                    } else {
                        console.log(result);
                        //id_info.innerHTML = result;
                        alert(result);
                    }
                } else {
                  alert(this.statusText)

                }
             }
        };
        if(method == "GET") {
            var params = (params != "")? "?"+params : "";
            xhttp.open(method, url+params, true);
            xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
            xhttp.send(  );
        } else if(method == "POST"){
            xhttp.open(method, url, true);
            xhttp.setRequestHeader("Content-type", "application/json; charset=utf-8");
            xhttp.send( data  );
        }
   }

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
                      document.getElementById('id_version').innerHTML = jd.version;
                      document.getElementById('id_device').innerHTML = jd.id_device;
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

                      var blocked_topics = jd.blocked_topic;
                      if(blocked_topics.length > 0) {
                          var text = "";
                          //document.getElementsByClassName("C_topic_wrapper")[0].style.display = "block";
                          for (i = 0; i < blocked_topics.length; i++) {
                               id_topic = blocked_topics[i]
                               //if( (id_topic != "") && (id_topic != jd.id_device) && (id_topic != "#") && (id_topic != null) ) {
                               if( (id_topic != "") && (id_topic != "#") &&  (id_topic != null) ) {
                                    text += "<input type='checkbox' name='sel_blocked_topic' value='"+ id_topic +"'>" + id_topic + "<br>";
                               }
                        }
                          document.getElementById("id_blocked_topic_container").innerHTML +=  text;
                      } else {
                        document.getElementById("id_blocked_topic_container").innerHTML = "No Topics";
                        document.getElementById("id_remove_blocked_topic").style.display = "none";
                      }

                      var topics = jd.sub_topic;
                      if(topics.length > 0) {
                          var text = "";
                          document.getElementsByClassName("C_topic_wrapper")[0].style.display = "block";
                          for (i = 0; i < topics.length; i++) {
                               id_topic = topics[i][0]
                               if( (id_topic != "") && (id_topic != jd.id_device) && (id_topic != "#") && (id_topic != null) ) {
                                    text += "<input type='checkbox' name='sel_topic' value='"+ id_topic +"'>" + topics[i][1] + "/" + topics[i][2] + "<br>";
                               }
                        }
                          document.getElementById("id_topics").innerHTML +=  text;
                      } else {
                        document.getElementById("id_topics").innerHTML = "No homes";
                        document.getElementById("id_remove_topic").style.display = "none";
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
      data["mode"] = document.getElementById("id_set_mode").value;
      rest_call(url="/restart", method="GET", data=data, refresh_on_success=true)
  };

  /*document.getElementById("id_restart_webrepl").onclick = function(){
      console.log("restarting in WebREPL mode...");
      showInfo("Restarting Device in WebREPL mode...")
      data = {}
      data["mode"] = 3;
      rest_call(url="/restart_webrepl", method="GET", data=data, refresh_on_success=true)
  };*/

  document.getElementById("id_reset_device").onclick = function(){
      console.log("Resetting Device");
      showInfo("Resetting Device...")
      //document.getElementById("id_info_wrapper").style.display = "block";
      data = {}
      //data["mode"] = document.getElementById("id_set_mode").value;
      rest_call(url="/reset_device", method="GET", data=data)
  };

  document.getElementById("id_remove_blocked_topic").onclick = function(){
      var topics = [];
      var t = document.getElementsByName("sel_blocked_topic");
      for(i in t) {
          if(t[i].checked) {
            topics.push(t[i].value);
          }
      };
      //console.log(topics)
      if(topics.length == 0) {
            //id_info.innerHTML = "Select a Home to Remove"
            alert("Select a Topic to Remove")
      } else{
        //console.log(topics);
        //console.log(topics.values());
        var data = {}
        data["blocked_topic"] = JSON.stringify(topics) //stringify for converting js-array to python-list
        console.log(data)
        rest_call(url="/remove_blocked_topic", method="GET", data=data)
      }
  };

    document.getElementById("id_remove_topic").onclick = function(){
      var topics = [];
      var t = document.getElementsByName("sel_topic");
      for(i in t) {
          if(t[i].checked) {
            topics.push(t[i].value);
          }
      };
      //console.log(topics)
      if(topics.length == 0) {
            //id_info.innerHTML = "Select a Home to Remove"
            alert("Select a Home to Remove")
      } else{
        //console.log(topics);
        //console.log(topics.values());
        var data = {}
        data["sub_topic"] = JSON.stringify(topics) //stringify for converting js-array to python-list
        console.log(data)
        rest_call(url="/remove_topic", method="GET", data=data)
      }
  };

  document.getElementById("id_check_for_update").onclick = function(){
      //console.log("checking for updates");
      showInfo("Checking For Updates...")
      var data = {}
      //data["version"] = DATA.version
      rest_call(url="/check_and_download_update", method="GET", data=data, refresh_on_success=true)
  };

