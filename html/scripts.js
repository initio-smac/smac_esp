    



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
      //data["mode"] = document.getElementById("id_set_mode").value;
      data["mode"] = 0
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

  

  var els = document.getElementsByClassName("C_change_property")
  for(var i = 0, x = els.length; i < x; i++) {
    els[i].onclick = function() {
      console.log("cc")
      var id_property = ele.getAttribute("data-id-property");
      var type_property = ele.getAttribute("data-type-property");
      console.log(id_property)
      console.log(type_property)
  };
}
  

