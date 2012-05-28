var map;

function init(){
    map = new OpenLayers.Map("map");
    map.addControl(new OpenLayers.Control.LayerSwitcher());

var shaded = new OpenLayers.Layer.VirtualEarth("Shaded", {
    type: VEMapStyle.Shaded
});
var hybrid = new OpenLayers.Layer.VirtualEarth("Hybrid", {
    type: VEMapStyle.Hybrid
});
var aerial = new OpenLayers.Layer.VirtualEarth("Aerial", {
        type: VEMapStyle.Aerial
    });

    map.addLayers([shaded, hybrid, aerial]);

    map.setCenter(new OpenLayers.LonLat(-110, 45), 3);
    
    map.zoomToMaxExtent();
}