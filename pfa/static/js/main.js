
setTimeout(function() {
  $('#message').fadeOut('slow');
}, 2000);



    $(document).ready(function() {
        // messages timeout for 10 sec 
        setTimeout(function() {
            $('.message_container').fadeOut('slow');
        }, 3000); // <-- time in milliseconds, 1000 =  1 sec

});
