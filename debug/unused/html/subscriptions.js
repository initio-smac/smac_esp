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

  document.getElementById("id_restart").onclick = function(){
      console.log("restarting...");
      showInfo("Restarting Device...")
      data = {}
      //data["mode"] = document.getElementById("id_set_mode").value;
      data["mode"] = 0
      rest_call(url="/restart", method="GET", data=data, refresh_on_success=true)
  };