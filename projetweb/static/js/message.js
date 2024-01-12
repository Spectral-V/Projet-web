//function to change the open for a room
function openandclose(rid) {
    var a = "/openandclose/"+rid+"";
    $.ajax({
        type: 'GET',
        url : a,
        success: function(data){
        
        },
        error: function(data){
          
        }
    });
}

//function to change the permission in a room for an user make admin if other than admin and normal if admin
function admin(uid,rid) {
    var a = "/adm/"+uid+"/"+rid+"";
    $.ajax({
        type: 'GET',
        url : a,
        success: function(data){
            console.log(data) 
        },
        error: function(data){
        }
    });
    
}
//function to change the permission in a room for an user ban if unban and unban if ban
function ban(uid,rid) {
    var a = "/ban/"+uid+"/"+rid+"";
    $.ajax({
        type: 'GET',
        url : a,
        success: function(data){
            console.log(data) 
        },
        error: function(data){ 
        }
    });
    
}
//function to change the permission in a room for an user mute if unmute and unmute if mute
function mute(uid,rid) {
    var a = "/mute/"+uid+"/"+rid+"";
    $.ajax({
        type: 'GET',
        url : a,
        success: function(data){
            console.log(data) 
        },
        error: function(data){
        }
    });
    
}

//function to delete a message with it's id from the table
function delmess(id) {
    
    var b = "/deletemessage/"+id+"";
    $.ajax({
        type: 'GET',
        url : b,
        success: function(data){ 
            console.log(data)   
        },
        error: function(data){
        }
    });
    
}
//display the message for a specifique room
function display_data () {
    $.ajax({
        type: 'GET',
        url : "/getMessages/"+room_id+"/",
        success: function(response){

            console.log(response);
            $("#display").empty();
            display_mess_1(response);
            
            
            
        },
        error: function(response){
            alert('An error occured')

           
        }
    });
    setInterval(function(){
        $.ajax({
            type: 'GET',
            url : "/getMessages/"+room_id+"/",
            success: function(response){

                console.log(response);
                $("#display").empty();
                display_mess(response);                
                
                
            },
            error: function(response){
                alert('An error occured')
    
               
            }
        });
    
    
    },1000);

}
$(document).ready(function(){
    display_data()
    
})
