  document.getElementById("id_check_for_update").onclick = function(){
      //console.log("checking for updates");
      showInfo("Checking For Updates...")
      var data = {}
      //data["version"] = DATA.version
      rest_call(url="/check_and_download_update", method="GET", data=data, refresh_on_success=true)
  };

  document.getElementById("id_reset_device").onclick = function(){
      console.log("Resetting Device");
      showInfo("Resetting Device...")
      //document.getElementById("id_info_wrapper").style.display = "block";
      data = {}
      //data["mode"] = document.getElementById("id_set_mode").value;
      rest_call(url="/reset_device", method="GET", data=data)
  };

  document.getElementById("id_restart").onclick = function(){
      console.log("restarting...");
      showInfo("Restarting Device...")
      data = {}
      //data["mode"] = document.getElementById("id_set_mode").value;
      data["mode"] = 0
      rest_call(url="/restart", method="GET", data=data, refresh_on_success=true)
  };