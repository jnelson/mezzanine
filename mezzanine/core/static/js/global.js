$(function() {
    
    // Wrap a span around the last part of the
    // logotype so we can adjust it's color.
        
    var $brand = $('.navbar-brand'),
        text = $brand.text(),
        start = text.substr(0, text.length - 4),
        end = text.substr(-4);
        
    $brand.html(start + "<span>" + end + "</span>");
    
});
