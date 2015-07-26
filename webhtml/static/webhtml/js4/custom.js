// toggle slide1 & slide2 in section2
function getstatus(){
    var viewing = $('body').attr('class');
    return viewing;
}
function slide(n){
    $('.fp-slidesNav.bottom li:nth-child('+n+') a').trigger('click');
}
var interval = 8000;
var toggle = setInterval(function(){
    if (getstatus()=='fp-viewing-page2-slide1') {setTimeout(function(){
        slide(2);
    },interval)};
    if (getstatus()=='fp-viewing-page2-slide2') {setTimeout(function(){
        slide(1);
    },interval)};
},interval);
// some animates
var monitor = 100;
var test = setInterval(function(){
    var viewing = getstatus();
    if (viewing=='fp-viewing-page2-slide1') {
        setTimeout(function(){
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
        },0);
    };
    if (viewing=='fp-viewing-page2-slide2') {
        setTimeout(function(){
            $('.intro-soft h1').addClass('animated bounceIn slow');
        },monitor);
    };
    if (viewing=='fp-viewing-page2-slide3') {
        toggle = window.clearInterval(toggle);//stop toggle
        setTimeout(function(){
            $('.value-title h1').addClass('animated bounceIn slow');
        },monitor);
    };
    if (viewing=='fp-viewing-page2-slide4') {
        toggle = window.clearInterval(toggle);//stop toggle
        setTimeout(function(){
            $('.app-title h1').addClass('animated bounceIn slow');
        },monitor);
    };
    if (viewing=='fp-viewing-page4') {
        setTimeout(function(){
            $('#barcode').addClass('animated bounceIn slow');
            $('#mobile-word').addClass('animated fadeIn slow');
        },monitor);
    };
    if (viewing=='fp-viewing-page5') {
        setTimeout(function(){
            $('.media h1').addClass('animated bounceIn slow');
        },monitor);
    };
    if (viewing=='fp-viewing-page6') {
        setTimeout(function(){
            $('.contact h1').addClass('animated bounceIn slow');
        },monitor);
    };
},monitor);


// jquery.waterwheelCarousel.min.js
(function(){
  var carousel = $("#carousel").waterwheelCarousel({
    flankingItems: 3,
    forcedImageWidth: 300,
    forcedImageHeight: 600,
    separation: 200,
    horizon: 300,
    // horizonOffset: 0,
    // autoPlay: 3000,
  });
  var app_toggle = setInterval(function(){
      carousel.next();
  },3000);
}());