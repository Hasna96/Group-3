// This makes the text objects fade in and out at random intervals, positions and sizes

(function fadeInDiv(){
    var divs = $('.fadeIn');
    var divsize = ((Math.random()*200) + 50).toFixed();
    var posx = (Math.random() * ($(document).width() - divsize)).toFixed();
    var posy = (Math.random() * ($(document).height() - divsize)).toFixed();
    var maxSize = 80;
    var minSize = 5;
    var size = (Math.random()*maxSize+minSize)
    
    var elem = divs.eq(Math.floor(Math.random()*divs.length));
    
    if (!elem.is(':visible')){
        elem.fadeIn(Math.floor(Math.random()*1500),fadeInDiv);
        elem.css({
            'position':'absolute',
            'left':posx+'px',
            'top':posy+'px',
            'font-size': size+'px'
        });
    } else {
        elem.fadeOut(Math.floor(Math.random()*1500),fadeInDiv); 
    }
})();