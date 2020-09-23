function getState() {
  console.log( "document loaded" );
  var url = "/get_state_names"; 
  $.get(url,function(data, status) {
      console.log("got response for get_state_names request");
      if(data) {
          var state = data.states;
          var uiStates = document.getElementById("uiStates");
          $('#uiStates').empty();
          for(var i in state) {
              var opt = new Option(state[i]);
              $('#uiStates').append(opt);
          }
      }
  });
}

function getDistrict() {

    var selectedState = document.getElementById('uiStates');

    console.log( "document loaded" );

    var url = "/load_districts";
    $.post(url, {
        state: selectedState.value
    }, function(data, status) {
        console.log("got response for load_districts request");
        console.log(data)
        if(data) {
            var district = data.district;
            var uiDistricts = document.getElementById("uiDistricts");
            $('#uiDistricts').empty();
            for(var i in district) {
                var opt = new Option(district[i]);
                $('#uiDistricts').append(opt);
            }
        }
    });
}

function sendMail(){
    console.log("Send Mail has been clicked");

    var district=document.getElementById("uiDistricts");
    var mail=document.getElementById("uiEmail");

    var url="/send_mail";
    $.post(url, {
        district:district.value,
        mail:mail.value
    },function(data,status){
        console.log("sending email")
        uiClick.innerHTML="<h2>"+"You will receive an email everyday about COVID-19 stats. \nThank You.";
        console.log(status);
        location.reload()
    });
}


window.onload = () => {
    getState();
    document.getElementById('uiStates').onchange = function() {
        console.log('Selected state');
        getDistrict();
    };
}
