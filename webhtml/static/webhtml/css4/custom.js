// toggle slide1 & slide2 in section2
function getstatus(){
    var viewing = $('body').attr('class');
    return viewing;
}
var interval = 16000;
var toggle = setInterval(function(){
    if (getstatus()=='fp-viewing-page2-slide1') {$.fn.fullpage.moveSlideRight();};
    if (getstatus()=='fp-viewing-page2-slide2') {$.fn.fullpage.moveSlideLeft();};
},interval);
// custom animations
var monitor = 100;
var test = setInterval(function(){
    if (getstatus()=='fp-viewing-page2-slide1') {
        $('.intro-body').show();
        $('.intro-body-2').delay(0).queue(function(){
            $(this).show().addClass('animated pulse slow').dequeue();
        }).delay(2000).queue(function(){
            $('.intro-body-1').delay(0).queue(function(){
                $(this).show().addClass('animated rotateIn slow').dequeue();
            }).delay(2000).queue(function(){
                $('.intro-body-3').delay(0).queue(function(){
                    $(this).show().addClass('animated bounceInLeft slow').dequeue();
                }).delay(2000).queue(function(){
                    $('.intro-body-4').delay(0).queue(function(){
                        $(this).show().addClass('animated bounceInRight slow').dequeue();
                    });
                });
            });
        });
    } else {$('.intro-body').hide();};
    if (getstatus()=='fp-viewing-page2-slide2') {
        $('.intro-soft h1').addClass('animated bounceIn slow');
    } else {$('.intro-soft h1').removeClass('animated bounceIn slow');};
    if (getstatus()=='fp-viewing-page2-slide3') {
        toggle = window.clearInterval(toggle);//stop toggle
        $('.value-title h1').addClass('animated bounceIn slow');
    } else {$('.value-title h1').removeClass('animated bounceIn slow');};
    if (getstatus()=='fp-viewing-page2-slide4') {
        toggle = window.clearInterval(toggle);//stop toggle
        $('.app-title h1').addClass('animated bounceIn slow');
    } else {$('.app-title h1').removeClass('animated bounceIn slow');};
    if (getstatus()=='fp-viewing-page4') {
        $('#barcode').addClass('animated bounceIn slow');$('#mobile-word').addClass('animated fadeIn slow');
    } else {$('#barcode').removeClass('animated bounceIn slow');$('#mobile-word').removeClass('animated fadeIn slow');};
    if (getstatus()=='fp-viewing-page5') {
        $('.media h1').addClass('animated bounceIn slow');
    } else {$('.media h1').removeClass('animated bounceIn slow');};
    if (getstatus()=='fp-viewing-page6') {
        $('.contact h1').addClass('animated bounceIn slow');
    } else {$('.contact h1').removeClass('animated bounceIn slow');};
},monitor);
// config jquery.waterwheelCarousel.min.js
(function(){
  var carousel = $("#carousel").waterwheelCarousel({
    flankingItems: 3,
    forcedImageWidth: 300,
    forcedImageHeight: 600,
    separation: 200,
    horizon: 300,
    // autoPlay: 3000,
  });
  var app_toggle = setInterval(function(){
      carousel.next();
  },3000);
}());