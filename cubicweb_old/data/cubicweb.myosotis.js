Widgets.MyosotisTimelineWidget = defclass("TimelineWidget", null, {
    __init__: function(wdgnode) {
        var tldiv = DIV({
            id: "tl",
            style: 'height: 400px; border: 1px solid #ccc;'
        });
        wdgnode.appendChild(tldiv);
        var tlunit = wdgnode.getAttribute('cubicweb:tlunit') || 'YEAR';
        var eventSource = new Timeline.DefaultEventSource();
        var bandData = {
            eventPainter: Timeline.CubicWebEventPainter,
            eventSource: eventSource,
            width: "100%",
            intervalUnit: Timeline.DateTime[tlunit.toUpperCase()],
            intervalPixels: 100
        };
        var bandInfos = [Timeline.createBandInfo(bandData)];
        this.tl = Timeline.create(tldiv, bandInfos);
        var loadurl = wdgnode.getAttribute('cubicweb:loadurl');
        Timeline.loadJSON(loadurl, function(json, url) {
            eventSource.loadJSON(json, url);
        });

    }
});

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
