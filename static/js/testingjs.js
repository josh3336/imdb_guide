



//puts text in search box that dissapears when clicked on and reappears if left empty

$(function(){ //Document ready shorthand
  var $search = $('#simple_zip');//Cache the element for faster DOM searching since we are using it more than once
  original_val = $search.val(); //Get the original value to test against. We use .val() to grab value="Search"
  $search.focus(function(){ //When the user tabs/clicks the search box.
    if($(this).val()===original_val){ //If the value is still the default, in this case, "Search"
      $(this).val('');//If it is, set it to blank
    }
  })
  .blur(function(){//When the user tabs/clicks out of the input
    if($(this).val()===''){//If the value is blank (such as the user clicking in it and clicking out)...
      $(this).val(original_val); //... set back to the original value
    }
  });
});



$(document).ready(function(){ 
    //attach a jQuery live event to the button
    $('#getdata-button').click(function(){

        console.log("echo ")

        $.getJSON("findproviders.html", function(data) {

        console.log("echo "+ data)
            //alert(data); //uncomment this for debug
            alert(JSON.stringify(data));
            //alert (data.item1+" "+data.item2+" "+data.item3); //further debug

            $('#showdata').html("<p>"+JSON.stringify(data)+"</p>");
        });
    });
});


//when zip form field is changed it checks to make sure it is a valid zip then
//passses zipcode to findproviders view and returns the providers in a select drop down list
$(document).ready(function(){ 
    //attach a jQuery live event to the button
$('#simple_zip').change(function(){

  $('#selectme').html('')
	var x=$('#simple_zip').val()

	var re5digit=/^\d{5}$/;
	if (x.search(re5digit)==-1){
	  	document.getElementById('error_zipform').innerHTML='Invalid Zip';
	 	return false;
	  };
	  $("#error_zipform").html('')


      	var zipcode={zipcode:$('#simple_zip').val()}
        $.getJSON("findproviders.html",zipcode,function(data) {

            //alert(data); //uncomment this for debug
            //alert (data.item1+" "+data.item2+" "+data.item3); //further debug
            $("#selectme").append('<option value="' + "" + '">' + "Select Provider" + '</option>');   
            for ( var k in data ) {
  
    			     var optionId = k;
    			     var optionValue = data[ k ];
   				     $("#selectme").append('<option value="' + optionValue + '">' + optionId + '</option>');    
			         }
        });

    });
});

//checks to see enter key is pressed down within the input field, if so it changes the focus to the provider selectme form
$(document).ready(function(){ 
$("input").bind("keydown", function(event) {
    if (event.which === 13) {
        event.stopPropagation();
        event.preventDefault();
        $('#selectme').focus();
        $('#selectme').click();

    }
});
});


//submits selectme form when changed and puts a loading message in the content part of the page
$(function() {
    $('#selectme').change(function() {
        $('#loading-indicator').show();
        $('#loading_message').html('');
        //var zip_head={zipcode:$('#simple_zip').val(),headend:$('#selectme').val()}
        zipcode=$('#simple_zip').val();
        headend=$('#selectme').val();
        var input = $("<input>").attr("type", "hidden").attr("name", "zipcode").val(zipcode);
        $('#selectmeform').append($(input));
        var input = $("<input>").attr("type", "hidden").attr("name", "headend").val(headend);
        $('#selectmeform').append($(input));
        document.cookie = "time_sec="+Math.round(+new Date()/1000);
        string="Your tv guide is being loaded and processed, your content will be displayed within 30 seconds."
        $('#loading_message').append(string);
        $('#selectmeform').submit()
    });
});





//used with jquery multiselect plugin, submits channelform
$(document).ready(function(prmstr){
  var checkforchange=0
   $("#channels").multiselect({
    noneSelectedText: "remove channels",
    selectedText: "remove channels",
    click: function(event,ui){
          checkforchange=1
    },
    uncheckAll: function(event,ui){
      checkforchange=1
},
    checkAll: function(event,ui){
      checkforchange=1
},

    close: function(event,ui){
          if(checkforchange==1){
          for (var i = 0; i < prmarr.length; i++){
              splitequal=prmarr[i].split('=')
              if (splitequal[0]=="type") {
               var input = $("<input>").attr("type", "hidden").attr("name", splitequal[0]).val(splitequal[1]); 
               $('#channelform').append(input)
              }

          };
            $('#channelform').submit()}
    }
  });
});

//used with jquery multiselect plugin, submits typeform
$(document).ready(function(prmstr){
  var checkforchange=0;
   $("#type").multiselect({
    noneSelectedText: "show all",
    header: "Show Only:",
    multiple: false,
    selectedList:2,
    click: function(event,ui){
          checkforchange=1
    },

      uncheckAll: function(event,ui){
        checkforchange=1
  },
      checkAll: function(event,ui){
        checkforchange=1
  },


    close: function(event,ui){
          if(checkforchange==1){
    
          for (var i = 0; i < prmarr.length; i++){
              splitequal=prmarr[i].split('=')
              if (splitequal[0]=="channels") {
               var input = $("<input>").attr("type", "hidden").attr("name", splitequal[0]).val(splitequal[1]); 
               $('#typeform').append(input)
              }

          };
            $('#typeform').submit()}
    }
  });
});






//checks to see if item is  selected for channels if so it checks it 
$(document).ready(function(){
    for (var i = 0; i < prmarr.length; i++){
      splitequal=prmarr[i].split('=');
      if (splitequal[0]=="channels"){
      $('#channels option[value="'+splitequal[1]+'"]').attr('selected', 'true');
    };
    };
});

//checks to see if item is selected for type if so it checks it 
$(document).ready(function(){
    for (var i = 0; i < prmarr.length; i++){
      splitequal=prmarr[i].split('=');
      if (splitequal[0]="type"){
      $('#type option[value="'+splitequal[1]+'"]').attr('selected', 'true');
    };
  };
});



//refreshes multiselect so checkmarks show up
$(document).ready(function(){
 $("#channels").multiselect("refresh");
 });

$(document).ready(function(){
 $("#type").multiselect("refresh");
 });



//grabs headers so they can be used to checkboxes
var prmstr = window.location.search.substr(1);
var prmarr = prmstr.split ("&");







