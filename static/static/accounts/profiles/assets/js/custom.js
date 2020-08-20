
/*=============================================================
    Authour URI: www.binarytheme.com
    License: Commons Attribution 3.0

    http://creativecommons.org/licenses/by/3.0/

    100% Free To use For Personal And Commercial Use.
    IN EXCHANGE JUST GIVE US CREDITS AND TELL YOUR FRIENDS ABOUT US

    ========================================================  */

(function ($) {
    "use strict";
    var mainApp = {
        scroll_fun: function () {

            /*====================================
             SCROLL SCRIPTS
            ======================================*/
            $(function () {
                $('.move-me a').bind('click', function (event) { //just pass move-me in design and start scrolling
                    var $anchor = $(this);
                    $('html, body').stop().animate({
                        scrollTop: $($anchor.attr('href')).offset().top
                    }, 1000, 'easeInOutQuad');
                    event.preventDefault();
                });
            });



        },

        gallery_fun: function () {
            /*====================================
                 FOR IMAGE/GALLERY POPUP
            ======================================*/
            $("a.preview").prettyPhoto({
                social_tools: false
            });

            /*====================================
            FOR IMAGE/GALLERY FILTER
            ======================================*/

            // MixItUp plugin
            // http://mixitup.io

            $('#port-folio').mixitup({
                targetSelector: '.portfolio-item',
                filterSelector: '.filter',


            });
        },
        vedio_fun:function()
        {
            $(function () {
                $(".player").mb_YTPlayer();
            });
        },

        nice_scroll_fun:function()
        {
            $("html").niceScroll();
        },
        custom_fun:function()
        {
            /*====================================
             WRITE YOUR   SCRIPTS  BELOW
            ======================================*/




        },

    }


    $(document).ready(function () {
        mainApp.scroll_fun();
        mainApp.gallery_fun();
        mainApp.vedio_fun();
        mainApp.nice_scroll_fun();
        mainApp.custom_fun();

    });
}(jQuery));

$(document).ready(function(){
    window_width = $(window).width();

    // Make the images from the card fill the hole space
    hipster_cards.fitBackgroundForCards();

});

hipster_cards = {
    misc:{
        navbar_menu_visible: 0
    },

    fitBackgroundForCards: function(){
        $('[data-background="image"]').each(function(){
            $this = $(this);

            background_src = $this.data("src");

            if(background_src != "undefined"){
                new_css = {
                    "background-image": "url('" + background_src + "')",
                    "background-position": "center center",
                    "background-size": "cover"
                };

                $this.css(new_css);
            }
        });

        $('.card .header img').each(function(){
            $card = $(this).parent().parent();
            $header = $(this).parent();

            background_src = $(this).attr("src");

            if(background_src != "undefined"){
                new_css = {
                    "background-image": "url('" + background_src + "')",
                    "background-position": "center center",
                    "background-size": "cover"
                };

                $header.css(new_css);
            }
        });

    },
}

$(document).ready(function(){
  JEEFACEFILTERAPI.init({
  canvasId: 'jeeFaceFilterCanvas',
  NNCpath: '/accounts/facefilter/dist/', //path to JSON neural network model (NNC.json by default)
  callbackReady: function(errCode, spec){
      if (errCode){
          console.log('AN ERROR HAPPENS. ERROR CODE =', errCode);
          return;
      }
      [init scene with spec...]
      console.log('INFO: JEEFACEFILTERAPI IS READY');
  }, //end callbackReady()

  //called at each render iteration (drawing loop)
  callbackTrack: function(detectState){
      //render your scene here
      [... do something with detectState]
  } //end callbackTrack()
});//end init call

JeelizResizer.size_canvas({
  canvasId: 'jeeFaceFilterCanvas',
    callback: function(isError, bestVideoSettings){
        JEEFACEFILTERAPI.init({
          videoSettings: bestVideoSettings,
          //...
          //...
        });
    }
});


});

JEEFACEFILTERAPI.init({
canvasId: 'jeeFaceFilterCanvas',
NNCpath: '/accounts/facefilter/dist/NNC.json', //path to JSON neural network model (NNC.json by default)
callbackReady: function(errCode, spec){
    if (errCode){
        console.log('AN ERROR HAPPENS. ERROR CODE =', errCode);
        return;
    }
    [init scene with spec...]
    console.log('INFO: JEEFACEFILTERAPI IS READY');
}, //end callbackReady()

//called at each render iteration (drawing loop)
callbackTrack: function(detectState){
    //render your scene here
    [... do something with detectState]
} //end callbackTrack()
});//end init call
