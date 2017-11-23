/************** HISTOGRAM ***************/
var original_hist = {};
var truncated_hist = {};
var composition_hist = {};

// var truncated_hist = {};
function plot_histogram(data) {

    original_hist = {x: data["x"], y: data["y"]};
    console.log(original_hist);

    var hist_data = [{
        x: data["x"],
        y: data["y"],
        // {#                x: [1,2,3],#}
        // {#                y: [10,11,12],#}
        type: 'bar'
    }];
    Plotly.newPlot('histogram', hist_data);
}

function plot_truncated_histogram(data, min_thresh, max_thresh) {
    var range = parseInt(max_thresh) - parseInt(min_thresh);
    var x_arr = [];
    var y_arr = [];
    var j = parseInt(min_thresh);
    if (range > 100) {
        var step = parseInt(range / 100) + 1; //floor()

        for (i = 0; i < 100; i++) {
            var x = 0;
            var y = 0;
            while (j < i * step && j <= parseInt(max_thresh)) {
                x = i;
                y = y + data["y"][j];
                j++;
            }
            x_arr.push(x);
            y_arr.push(y);
        }
    }

    else {
        var step = parseInt(100/range);
        var i = 0;
        for (i = 0; i<100; i++){
            var x = i;
            var y = 0;

                if (i % step == 0) {
                    if (j < parseInt(max_thresh)) {
                        y = data["y"][j];
                        j++;
                    }
                }
            x_arr.push(x);
            y_arr.push(y);
            }

        }

    console.log(x_arr, y_arr);

    truncated_hist = {x: x_arr, y: y_arr};
    var hist_data = [{
        x: truncated_hist["x"],
        y: truncated_hist["y"],
        type: 'bar'
    }];
    Plotly.newPlot('truncated-histogram', hist_data);
}

function plot_composition(data, a, b){
    var step;
    var x_arr = [];
    var y_arr = [];
    var a = parseFloat(a);
    var b = parseInt(b);
    var data_length = parseInt(data["x"].length*a) + 1;

    if (a<1){
        var j =0;
        step = parseInt(1/a)+1;
        for (var i = 0; i<data_length; i++){
            var x = i;
            var y = 0;
            while (j<i*step && j<data["x"].length){
                y = y + data["y"][j];
                j++;
            }

            x_arr.push(x);
            y_arr.push(y);
        }
    }

    else {
        step = parseInt(a);
        var j = 0;
        for (var i = 0; i< data_length; i++){
            var x = i;
            var y = 0;
                if (i % step == 0) {
                    if (j < data["x"].length) {
                        y = data["y"][j];
                        j++;
                    }
                }
            x_arr.push(x);
            y_arr.push(y);
            }
        }

    // move the hist based on b value
    var new_x_arr = [];
    var new_y_arr = [];
    for (var i =0; i<b; i++){
        new_x_arr.push(0);
        new_y_arr.push(0);
    }
    for (var i = 0; i<x_arr.length; i++){
        new_x_arr.push(x_arr[i]+b);
        new_y_arr.push(y_arr[i]);
    }

     console.log(new_x_arr, new_y_arr);

    composition_hist = {x: new_x_arr, y: new_y_arr};
  var hist_data = [{
        x: composition_hist["x"],
        y: composition_hist["y"],
        type: 'bar'
    }];
    Plotly.newPlot('composition-histogram', hist_data);

}


/****************** THUMBNAIL ******************/
function disp_hist_thumbnail(data) {
    var hist_thumbnail_data_arr = data["thumbnail_arr"];
    $('#hist-thumbnail').empty();
    for (i = 0; i < hist_thumbnail_data_arr.length; i++) {
        var thumbnail_id = "thumb_" + i;
        $('#hist-thumbnail').prepend($('<img>', {
            id: thumbnail_id,
            class: "img-fluid centered thumbnail",
            src: "data:image/jpeg;charset=utf-8;base64," + hist_thumbnail_data_arr[i],
            onclick: "on_click_thumbnail(id)"
        }));
    }
}

function on_click_thumbnail(thumbnail_id) {
    console.log("thumbnail id: ", thumbnail_id);
    do_ajax_post_val_only(thumbnail_id, 'input', '/img-from-thumbnail/');
}

/**************** UTIL FUNCTIONS ******************/
function do_ajax_post(e, domNameArr, inputNameArr, targetUrl) {
    e.preventDefault();
    // var json_data ="{"+inputName+":"+ $("#"+domName+"").val()+"}";
    var json_data = {};
    for (i = 0; i < domNameArr.length; i++) {
        inputName = inputNameArr[i];
        domName = domNameArr[i];
        json_data[inputName] = $("#" + domName + "").val();
    }
    var URL = targetUrl + get_temp_index() + "/";
    $.ajax({
        url: URL,
        type: "POST",
        // data: {inputName: $("#"+domName+"").val()},
        data: json_data,

        beforeSend: function () {
            document.body.style.cursor = "wait";
        },
        complete: function () {
            document.body.style.cursor = "default";
        },

        success: function (data) {
            update_image(data);
            disp_hist_thumbnail(data);
        },

        error: function (data) {
            alert('error');
        }
    });
}

function do_ajax_post_val_only(val, inputName, targetUrl) {
    // e.preventDefault();

    var json_data = {};
    json_data[inputName] = val;
    var URL = targetUrl + get_temp_index() + "/";
    $.ajax({
        url: URL,
        type: "POST",
        data: json_data,

        beforeSend: function () {
            document.body.style.cursor = "wait";
        },
        complete: function () {
            document.body.style.cursor = "default";
        },

        success: function (data) {
            update_image(data);
            disp_hist_thumbnail(data);
        },

        error: function (data) {
            alert('error');
        }
    });
}

function do_ajax_get(e, targetUrl) {
    e.preventDefault();
    var URL = targetUrl + get_temp_index() + "/";
    $.ajax({
        url: URL,
        type: "GET",

        beforeSend: function () {
            document.body.style.cursor = "wait";
        },
        complete: function () {
            document.body.style.cursor = "default";
        },
        success: function (data) {
            update_image(data);
            disp_hist_thumbnail(data);
        },

        error: function (data) {
            alert('error');
        }

    });
}

function disp_slider_val(dispDom, sliderDom) {
    $("#" + dispDom + "").val($("#" + sliderDom + "").val());
}

function update_image(data) {
    document.getElementById('image').src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
    canvasWrapper = document.getElementById('canvas-wrapper');
    canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
}

function get_temp_index() {
    tempIndexText = document.getElementById('temp-index').innerText.toString();
    return parseInt(tempIndexText);
}

/******************* DOM EVENT HANDLING *********************/
$("#slider-lower-thresh").change(function (e) {
    disp_slider_val('slider-val-lower-thresh', 'slider-lower-thresh');
    do_ajax_post(e, ['slider-lower-thresh'], ['input'], '/lower-thresholding/');
});

$("#btn_laplacian").click(function (e) {
    do_ajax_get(e, '/laplacian/');
});


$("#slider-upper-thresh").change(function (e) {
    disp_slider_val('slider-val-upper-thresh', 'slider-upper-thresh');
    do_ajax_post(e, ['slider-upper-thresh'], ['input'], '/upper-thresholding/');
});

$("#slider-kmeans").click(function (e) {
    disp_slider_val('slider-val-kmeans', 'slider-kmeans');
    do_ajax_post(e, ['slider-kmeans'], ['input'], '/kmeans/');
});


$("#btn_base64").click(function (e) {
    do_ajax_get(e, '/base64/');
})


$("#btn_undo").click(function (e) {
    do_ajax_get(e, '/undo/');
})


$("#btn_extract_crystal_mask").click(function (e) {
    do_ajax_post(e, ['crystal_label'], ['input'], '/extract-crystal-mask/');
});


$("#btn_all_crystal").click(function (e) {
    do_ajax_get(e, '/all-crystal/');
});


$("#btn_max_crystal").click(function (e) {
    do_ajax_get(e, '/max-crystal/');
});


$("#btn_reset").click(function (e) {
    do_ajax_get(e, '/reset/');
});

$("#btn_histogram").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/histogram/" + get_temp_index() + "/",

        success: function (data) {
            plot_histogram(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});

$("#btn_truncated_hist").click(function (e) {
    e.preventDefault();
    hist_min_thresh = $("#hist_min_thresh").val();
    hist_max_thresh = $("#hist_max_thresh").val();
    console.log(hist_min_thresh, hist_max_thresh);

    var is_valid = true;
    if (parseInt(hist_min_thresh) <0 || parseInt(hist_min_thresh) >255){
       alert("min threshold value range should be in range [0-255]");
        is_valid = false;
    }

    if (parseInt(hist_max_thresh) <0 || parseInt(hist_max_thresh) >255){
        alert("max threshold value range should be in range [0-255]");
        is_valid = false;
    }

    if (parseInt(hist_min_thresh) >= parseInt(hist_max_thresh)){
        alert("min threshold should smaller than max threshold");
        is_valid = false;
    }
    if (is_valid){
        plot_truncated_histogram(original_hist, hist_min_thresh, hist_max_thresh);
    }
    else {
        alert("invalid range. please input range again");
    }

});

$("#btn_comp").click(function(e){
   e.preventDefault();
   a = $("#comp_a").val();
   b = $("#comp_b").val();
   console.log(a, b);


   var is_valid = true;
    if (parseFloat(a) <= 0 || parseFloat(b) < 0){
       alert("a should be positive and b should be non-negative");
        is_valid = false;
    }


    if (is_valid){
         plot_composition(truncated_hist, a, b);
    }

    else{
        alert("invalid composition value. Please input again.")
    }
});

$("#slider-opening-kernel").change(function (e) {
    disp_slider_val('slider-opening-val-kernel', 'slider-opening-kernel');
    do_ajax_post(e, ['slider-opening-kernel', 'slider-opening-iter'], ['kernel_size', 'num_of_iter'], '/opening/');
});


$("#slider-opening-iter").change(function (e) {
    disp_slider_val('slider-opening-val-iter', 'slider-opening-iter');
    do_ajax_post(e, ['slider-opening-kernel', 'slider-opening-iter'], ['kernel_size', 'num_of_iter'], '/opening/');
});


$("#slider-closing-kernel").change(function (e) {
    disp_slider_val('slider-closing-val-kernel', 'slider-closing-kernel');
    do_ajax_post(e, ['slider-closing-kernel', 'slider-closing-iter'], ['kernel_size', 'num_of_iter'], '/closing/');
});


$("#slider-closing-iter").change(function (e) {
    disp_slider_val('slider-closing-val-iter', 'slider-closing-iter');
    do_ajax_post(e, ['slider-closing-kernel', 'slider-closing-iter'], ['kernel_size', 'num_of_iter'], '/closing/');
});


$("#slider-erosion-kernel").change(function (e) {
    disp_slider_val('slider-erosion-val-kernel', 'slider-erosion-kernel');
    do_ajax_post(e, ['slider-erosion-kernel', 'slider-erosion-iter'], ['kernel_size', 'num_of_iter'], '/erosion/');
});


$("#slider-erosion-iter").change(function (e) {
    disp_slider_val('slider-erosion-val-iter', 'slider-erosion-iter');
    do_ajax_post(e, ['slider-erosion-kernel', 'slider-erosion-iter'], ['kernel_size', 'num_of_iter'], '/erosion/');
});


$("#slider-dilation-kernel").change(function (e) {
    disp_slider_val('slider-dilation-val-kernel', 'slider-dilation-kernel');
    do_ajax_post(e, ['slider-dilation-kernel', 'slider-dilation-iter'], ['kernel_size', 'num_of_iter'], '/dilation/');
});


$("#slider-dilation-iter").change(function (e) {
    disp_slider_val('slider-dilation-val-iter', 'slider-dilation-iter');
    do_ajax_post(e, ['slider-dilation-kernel', 'slider-dilation-iter'], ['kernel_size', 'num_of_iter'], '/dilation/');
});


$("#btn_extract_top_crystal").click(function (e) {
    do_ajax_post(e, ['num_crystal_label'], ['input'], '/top-crystal/');
});


/*********************** CANVAS **************************/
var image = document.getElementById('image');
var canvasWrapper = document.getElementById('canvas-wrapper');
var canvasToolbar = document.getElementById('canvas-toolbar');
var naturalWidth = image.naturalWidth;
var naturalHeight = image.naturalHeight;
var canvasHidden = Object.create(null);


image.addEventListener("change", updateImageChange);

function elt(name, attributes) {
    var node = document.createElement(name);
    // {#            var node = document.getElementById(name);#}
    if (attributes) {
        for (var attr in attributes)
            if (attributes.hasOwnProperty(attr))
                node.setAttribute(attr, attributes[attr]);
    }
    for (var i = 2; i < arguments.length; i++) {
        var child = arguments[i];
        if (typeof child == "string")
            child = document.createTextNode(child);
        node.appendChild(child);
    }
    return node;
}

var controls = Object.create(null);

function initPaint(parent) {
    setCanvasWrapperSize();
    canvasWrapperSize = getElementSize('canvas-wrapper');
    var canvasMain = elt("canvas", {
        width: canvasWrapperSize.width,
        height: canvasWrapperSize.height,
        id: 'canvas-main'
    });
    // canvasHidden = elt("canvas", {width: naturalWidth, height: naturalHeight, id: 'canvas-hidden'});
    canvasHidden = elt("canvas", {
        width: naturalWidth,
        height: naturalHeight,
        id: 'canvas-hidden',
        hidden: true
    });
    // {#    var canvas = document.getElementById("myCanvas");#}
    // {#    var canvas = elt("myCanvas", {width: 500, height: 300});#}
    var cx = canvasMain.getContext("2d");

    var color = cx.fillStyle, size = cx.lineWidth;
    color = 'rgb(0, 255, 0)';
    // cx.canvas.width = image.width;
    // cx.canvas.height = image.height;
    // cx.canvas.width = naturalWidth;
    // cx.canvas.height = naturalHeight;
    // {#            cx.drawImage(image, 0, 0);#}
    cx.fillStyle = color;
    cx.strokeStyle = color;
    cx.lineWidth = size;
    var toolbar = elt("div", {class: "toolbar"});
    for (var name in controls)
        toolbar.appendChild(controls[name](cx));

    // var panel = elt("div", {class: "picturepanel"}, canvas);

    // parent.appendChild(elt("div", null, panel, toolbar));
    canvasWrapper.appendChild(canvasMain);
    canvasWrapper.appendChild(canvasHidden);
    canvasToolbar.appendChild(toolbar);
    updateImageChange()
}

var tools = Object.create(null);

controls.tool = function (cx) {
    var select = elt("select");
    for (var name in tools)
        select.appendChild(elt("option", null, name));

    cx.canvas.addEventListener("mousedown", function (event) {
        if (event.which == 1) {
            tools[select.value](event, cx);
            event.preventDefault();
        }
    });

    return elt("span", null, "Tool: ", select);
};

function relativePos(event, element) {
    var rect = element.getBoundingClientRect();
    return {
        x: Math.floor(event.clientX - rect.left),
        y: Math.floor(event.clientY - rect.top)
    };
}

function trackDrag(onMove, onEnd) {
    function end(event) {
        removeEventListener("mousemove", onMove);
        removeEventListener("mouseup", end);
        if (onEnd)
            onEnd(event);
    }

    addEventListener("mousemove", onMove);
    addEventListener("mouseup", end);
}

tools.Line = function (event, cx, onEnd) {
    cx.lineCap = "round";

    var pos = relativePos(event, cx.canvas);
    trackDrag(function (event) {
        cx.beginPath();
        cx.moveTo(pos.x, pos.y);
        pos = relativePos(event, cx.canvas);
        cx.lineTo(pos.x, pos.y);
        cx.stroke();
    }, onEnd);
};

tools.Erase = function (event, cx) {
    cx.globalCompositeOperation = "destination-out";
    tools.Line(event, cx, function () {
        cx.globalCompositeOperation = "source-over";
    });
};

controls.option = function (cx) {
    // var input = elt("input", {type: "color"});
    // input.addEventListener("change", function () {
    //     cx.fillStyle = input.value;
    //     cx.strokeStyle = input.value;
    // });
    // return elt("span", null, "Color: ", input);
    var input = elt("select");
    var options = {'add': 'rgb(0, 255, 0)', 'remove': 'rgb(255, 64, 64)'};
    for (option in options) {

        input.appendChild(elt("option", {value: options[option]}, option));

    }

    input.addEventListener("change", function () {
        cx.fillStyle = input.value;
        cx.strokeStyle = input.value;
    });
    return elt("span", null, "Option: ", input);
};

controls.brushSize = function (cx) {
    var select = elt("select");
    var sizes = [1, 2, 3, 5, 8, 12, 25, 35, 50, 75, 100];
    sizes.forEach(function (size) {
        select.appendChild(elt("option", {value: size},
            size + " pixels"));
    });
    select.addEventListener("change", function () {
        cx.lineWidth = select.value;
    });
    return elt("span", null, "Brush size: ", select);
};


function updateImageChange() {
    //
    // {#            var color = cx.fillStyle, size = cx.lineWidth;#}
    // {#                cx.canvas.width = image.width;#}
    // {#                cx.canvas.height = image.height;#}
    // {#            cx.drawImage(image, 0, 0);#}
    // {#            cx.fillStyle = color;#}
    // {#            cx.strokeStyle = color;#}
    // {#            cx.lineWidth = size;#}

    canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
}

controls.updateImage = function (cx) {

    var form = elt("form", null,
        elt("button", {type: "submit"}, "Load brush"));
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        cx.canvas.style.display = "block";
        updateImageChange();
    });
    return form;
};

function saveCanvas(cx) {
    // var data = cx.getImageData(0, 0, cx.canvas.width, cx.canvas.height).data;
    // console.log(data);
    // console.log(JSON.stringify(data));

    // var jpegUrl = cx.canvas.toDataURL("image/jpeg");

    var jpegUrl = convertCanvasData(cx);
    // console.log(jpegUrl);

    // return data;
    // var image = document.getElementById('image');
    // image.src = jpegUrl;

    do_ajax_post_val_only(jpegUrl, 'mask', '/update-mask/');
    // setCanvasWrapperSize();
    cx.canvas.style.display = "none";

}

controls.saveDrawing = function (cx) {
    var form = elt("form", null,
        elt("button", {type: "submit"}, "Do brush"
        ));
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        saveCanvas(cx);
    });
    return form;
};

function randomPointInRadius(radius) {
    for (; ;) {
        var x = Math.random() * 2 - 1;
        var y = Math.random() * 2 - 1;
        if (x * x + y * y <= 1) {
            return {x: x * radius, y: y * radius};
        }
    }
};

function getElementSize(elementId) {
    var element = document.getElementById(elementId);
    var boundingBox = element.getBoundingClientRect();
    var elementWidth = boundingBox.right - boundingBox.left;
    var elementHeight = boundingBox.bottom - boundingBox.top;
    return {width: elementWidth, height: elementHeight};
}

function convertCanvasData(cx) {
    var hiddenContext = canvasHidden.getContext("2d");
    hiddenContext.drawImage(cx.canvas, 0, 0, hiddenContext.canvas.width, hiddenContext.canvas.height);
    var hiddenCanvasData = hiddenContext.canvas.toDataURL("image/jpeg");
    return hiddenCanvasData;
}


function setCanvasWrapperSize() {

    // var boundingBox = canvasWrapper.getBoundingClientRect();
    // var canvasWrapperColWidth = boundingBox.right -boundingBox.left;
    canvasWrapperSize = getElementSize('canvas-wrapper');
    var imageWidth = image.width;
    var imageHeight = image.height;
    var canvasWrapperHeight = Math.floor(imageHeight * canvasWrapperSize.width / imageWidth) + 1;
    canvasWrapper.style.height = canvasWrapperHeight.toString() + 'px';

}

