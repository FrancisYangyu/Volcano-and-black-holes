"use strict";
var timeCycle;
// Cycles through overlayes
function cycleOverlay(map, mapOverlays) {
    // Create the first overlay and add to map
    var cnt = 0;
    var overlays=[];
    // Changes overlay every 1.5 seconds
    timeCycle = setInterval(function () {
        map.removeOverlay(overlay);
        map.clearOverlays();
        if (cnt == 24)
            cnt = 0;
        if(mapOverlays[cnt].length==0){
        	cnt+=1;
       	}
        createLabel(cnt);
        for (overlay in overlays) {
            map.removeOverlay(overlays[overlay]);
            overlays.splice(overlay, 1);
        }


        for (var overlay in mapOverlays[cnt]) {
        	//console.log(overlay)
            //console.log(mapOverlays.length);
            var points = [
                getMapPoints(mapOverlays[cnt][overlay].coordinates[0]),
                getMapPoints(mapOverlays[cnt][overlay].coordinates[1])
            ];

            overlay = createOverlay(mapOverlays[cnt][overlay].type, points);
            overlays.push(overlay);
            map.addOverlay(overlay);
        }
        cnt += 1;
    }, 1500);
}

// Converts coordinates into BMap.Point
//coordinates array<Float> Array containing latitude and longitude
// Returns BMap.Point
function getMapPoints(coordinates) {
    return new BMap.Point(coordinates.lat, coordinates.lng);
}

// Creates a map
// locationPoint BMap.Point(lat,lng) The centre point for the map
// Returns a BMap.Map object
function createMap(locationPoint) {
    var map = new BMap.Map('allmap');

    map.centerAndZoom(locationPoint, 13);
    map.enableScrollWheelZoom();
    map.addControl(new BMap.NavigationControl());
    map.addControl(new BMap.ScaleControl());
    map.addControl(new BMap.OverviewMapControl());
    map.addControl(new BMap.MapTypeControl());

    return map;
}

// Creates an overlay for the map
// coordinates array<BMap.Point> An array of length 2 containing the south-west and North-East points
// of the overlay
// Returns a BMap.GroundOverlay object
function createOverlay(type, coordinates) {
    // Options for the overlay
    // TODO: Set colour for overlay
    var overlayOptions = {
        opacity: 0.7,
        displayOnMinLevel: 10,
        displayOnMaxLevel: 20,
    }

    var overlay = new BMap.GroundOverlay(new BMap.Bounds(coordinates[0], coordinates[1]), overlayOptions);

    if (type == 0) {
        overlay.setImageURL('images/volcano.png');
    } else {
        overlay.setImageURL('images/blackhole.png');
    }
    return overlay;
}
//Create Label for mentioning the time when cycling
function createLabel(cnt) {
    var time = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "24:00"];
    document.getElementById("time").innerHTML = "Time:  " + time[cnt] + "-" + time[cnt + 1];
    //console.log(label);
}

var map = createMap(getMapPoints({
    'lat': -73.937297,
    'lng': 40.750026
}));
var url = 'http://localhost/volcano/NYC.php';
var overlays = [];

function getText() {
    var getY = $("#year option:selected"); //获取选中的项
    var getM = $("#month option:selected"); //获取选中的项
    var getD = $("#day option:selected"); //获取选中的项
    var year = getY.val(); //拿到选中项的值
    var month = getM.val();
    if (getM.val() < 10)
        month = "0" + month;
    var day = getD.val();
    if (getD.val() < 10)
        day = "0" + day;
    //console.log(year, month, day);
    //sent data to php server and get the data which you choose
    $.post(url, {
        "year": year,
        "month": month,
        "day": day
    },function(data,status){
        //console.log(data[0]);
        overlays=[];
        console.log(status);
        if (status=="success") {
            for (var i = 0; i < data.length; i++) {
            //console.log(data);
            var arr = [];
            for (var j = 0, k = 0; j < data[i].length; j = j + 5, k++) {
                var overlay = {
                    'type': data[i][j],
                    'coordinates': [{
                            'lat': data[i][j + 1],
                            'lng': data[i][j + 2]
                            },
                        {
                            'lat': data[i][j + 3],
                            'lng': data[i][j + 4]
                            }
                        ]
                };
                //console.log(overlay);
                arr.push(overlay);
            }
            //console.log(arr);
            overlays.push(arr);
            //console.log(overlays);
            clearInterval(timeCycle);
            cycleOverlay(map, overlays);
            }
        }
        else{
            alert("Please try to select another date");
        }
        
        
    });
}
