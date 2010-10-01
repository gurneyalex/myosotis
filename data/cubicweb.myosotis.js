jQuery(document).ready(function(){
    tl_widgets = []
    jQuery(document).find('.widget').each(function() {
        if (this.getAttribute('cubicweb:loadtype') != 'auto') {
            tl_widgets[tl_widgets.length] = buildWidget(this);
        }
    });    
});


function setMinVisibleDate(date){
    for(var i = 0, length=tl_widgets.length; i < length; i++) {
        var tl = tl_widgets[i].tl;
        for (var j=0; j < tl.getBandCount(); j++){
            tl.getBand(j).setMinVisibleDate(date);
        }
    }
}
