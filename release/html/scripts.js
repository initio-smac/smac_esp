document.getElementById("id_wifi_submit_1").onclick=function(){var e=document.getElementById("id_wifi_ssid_1").value,t=document.getElementById("id_wifi_password_1").value,c={};c.ssid=e,c.password=t,c.connection=1,rest_call(url="/update_wifi",method="GET",c=c,refresh_on_success=!0)},document.getElementById("id_ap_submit").onclick=function(){var e=document.getElementById("id_ap_ssid").value,t=document.getElementById("id_ap_password").value,c={};c.ssid=e,c.password=t,rest_call(url="/update_wifi_ap",method="GET",c=c,refresh_on_success=!0)},document.getElementById("id_select_input_type").onclick=function(){var e="switch";document.getElementById("id_ip_sel_switch").checked?e="switch":document.getElementById("id_ip_sel_pushbtn").checked&&(e="pushbutton");var t={};t.input_type=e,rest_call(url="/update_input_type",method="GET",t=t,refresh_on_success=!0)},document.getElementById("id_update_name_device").onclick=function(){var e={};e.name_device=document.getElementById("id_text_name_device").value,console.log(e),rest_call(url="/update_name_device",method="GET",e=e,refresh_on_success=!0)},document.getElementById("id_update_pin_device").onclick=function(){var e={};e.pin_device=document.getElementById("id_text_pin_device").value,console.log(e),rest_call(url="/update_pin_device",method="GET",e=e)},document.getElementById("id_restart").onclick=function(){console.log("restarting..."),showInfo("Restarting Device..."),data={},data.mode=0,rest_call(url="/restart",method="GET",data=data,refresh_on_success=!0)},document.getElementById("id_reset_device").onclick=function(){console.log("Resetting Device"),showInfo("Resetting Device..."),data={},rest_call(url="/reset_device",method="GET",data=data)},document.getElementById("id_remove_blocked_topic").onclick=function(){var e=[],t=document.getElementsByName("sel_blocked_topic");for(i in t)t[i].checked&&e.push(t[i].value);if(0==e.length)alert("Select a Topic to Remove");else{var c={};c.blocked_topic=JSON.stringify(e),console.log(c),rest_call(url="/remove_blocked_topic",method="GET",c=c)}},document.getElementById("id_remove_topic").onclick=function(){var e=[],t=document.getElementsByName("sel_topic");for(i in t)t[i].checked&&e.push(t[i].value);if(0==e.length)alert("Select a Home to Remove");else{var c={};c.sub_topic=JSON.stringify(e),console.log(c),rest_call(url="/remove_topic",method="GET",c=c)}},document.getElementById("id_check_for_update").onclick=function(){showInfo("Checking For Updates...");var e={};rest_call(url="/check_and_download_update",method="GET",e=e,refresh_on_success=!0)};for(var els=document.getElementsByClassName("C_change_property"),i=0,x=els.length;i<x;i++)els[i].onclick=function(){console.log("cc");var e=ele.getAttribute("data-id-property"),t=ele.getAttribute("data-type-property");console.log(e),console.log(t)};