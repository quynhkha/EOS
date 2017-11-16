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
        }))
    }
}

function plot_histogram(data) {

    var hist_data = [{
        x: data["x"],
        y: data["y"],
        // {#                x: [1,2,3],#}
        // {#                y: [10,11,12],#}
        type: 'bar'
    }];
    Plotly.newPlot('histogram', hist_data);
}

function on_click_thumbnail(thumbnail_id) {
    console.log("thumbnail id: ", thumbnail_id);
    $.ajax({
        url: "img-from-thumbnail/", // the endpoint
        type: "POST", // http method
        data: {input: thumbnail_id}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });

}

//
//
// {#}
// {#$("#ex5").slider();#}
// {##}
// {##}
$("#slider-lower-thresh").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-val-lower-thresh").val($("#slider-lower-thresh").val());
    e.preventDefault();
    console.log("value", $('#slider-lower-thresh').val());
    $.ajax({
        url: "lower-thresholding/", // the endpoint
        type: "POST", // http method
        data: {input: $('#slider-lower-thresh').val()}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});

$("#btn_laplacian").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/laplacian",

        success: function (data) {
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});


// AJAX for posting
$("#slider-upper-thresh").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-val-upper-thresh").val($("#slider-upper-thresh").val());
    e.preventDefault();
    console.log("value", $('#slider-upper-thresh').val());
    $.ajax({
        url: "upper-thresholding/", // the endpoint
        type: "POST", // http method
        data: {input: $('#slider-upper-thresh').val()}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#upper_thresh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});

$("#slider-kmeans").click(function (e) {
    $("#slider-val-kmeans").val($("#slider-kmeans").val());
    e.preventDefault();
    $.ajax({
        url: "kmeans/",
        type: "POST", // http method
        data: {input: $("#slider-kmeans").val()}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#slider-kmeans').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#btn_base64").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/base64",
        success: function (data) {
            var image = document.createElement('img');
            image.src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            document.querySelector('#imageContainer').innerHTML = image.outerHTML;//where to insert your image
            // {#                    console.log(data);#}
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    })
})


$("#btn_undo").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/undo",
        success: function (data) {
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    })
})


$("#btn_extract_crystal_mask").click(function (e) {
    e.preventDefault();
    $.ajax({
        url: "extract-crystal-mask/",
        type: "POST", // http method
        data: {input: $("#crystal_label").val()}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $('#lower_thesh_input').val(''); // remove the value from the input
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#btn_all_crystal").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "all-crystal/",

        success: function (data) {
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#btn_max_crystal").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "max-crystal/",

        success: function (data) {
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#btn_reset").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/reset",

        success: function (data) {
            $('#histogram').empty();
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});


$("#btn_histogram").click(function (e) {
    e.preventDefault();
    $.ajax({
        type: "GET",
        url: "/histogram",

        success: function (data) {
            plot_histogram(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});


$("#slider-opening-kernel").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-opening-val-kernel").val($("#slider-opening-kernel").val());
    e.preventDefault();
    console.log("value", $('#slider-opening-kernel').val());
    $.ajax({
        url: "opening/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-opening-kernel').val(),
            num_of_iter: $('#slider-opening-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-opening-iter").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-opening-val-iter").val($("#slider-opening-iter").val());
    e.preventDefault();
    console.log("value", $('#slider-opening-iter').val());
    $.ajax({
        url: "opening/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-opening-kernel').val(),
            num_of_iter: $('#slider-opening-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-closing-kernel").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-closing-val-kernel").val($("#slider-closing-kernel").val());
    e.preventDefault();
    console.log("value", $('#slider-closing-kernel').val());
    $.ajax({
        url: "closing/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-closing-kernel').val(),
            num_of_iter: $('#slider-closing-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-closing-iter").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-closing-val-iter").val($("#slider-closing-iter").val());
    e.preventDefault();
    console.log("value", $('#slider-closing-iter').val());
    $.ajax({
        url: "closing/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-closing-kernel').val(),
            num_of_iter: $('#slider-closing-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-erosion-kernel").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-erosion-val-kernel").val($("#slider-erosion-kernel").val());
    e.preventDefault();
    console.log("value", $('#slider-erosion-kernel').val());
    $.ajax({
        url: "erosion/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-erosion-kernel').val(),
            num_of_iter: $('#slider-erosion-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-erosion-iter").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-erosion-val-iter").val($("#slider-erosion-iter").val());
    e.preventDefault();
    console.log("value", $('#slider-erosion-iter').val());
    $.ajax({
        url: "erosion/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-erosion-kernel').val(),
            num_of_iter: $('#slider-erosion-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-dilation-kernel").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-dilation-val-kernel").val($("#slider-dilation-kernel").val());
    e.preventDefault();
    console.log("value", $('#slider-dilation-kernel').val());
    $.ajax({
        url: "dilation/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-dilation-kernel').val(),
            num_of_iter: $('#slider-dilation-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#slider-dilation-iter").change(function (e) {
    // {#            alert($("#slider").val());#}
    $("#slider-dilation-val-iter").val($("#slider-dilation-iter").val());
    e.preventDefault();
    console.log("value", $('#slider-dilation-iter').val());
    $.ajax({
        url: "closing/", // the endpoint
        type: "POST", // http method
        data: {
            kernel_size: $('#slider-dilation-kernel').val(),
            num_of_iter: $('#slider-dilation-iter').val()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


$("#btn_extract_top_crystal").click(function (e) {
    e.preventDefault();
    $.ajax({
        url: "top-crystal/",
        type: "POST", // http method
        data: {input: $("#num_crystal_label").val()}, // data sent with the post request

        // handle a successful response
        success: function (data) {
            // {#                    $('#lower_thesh_input').val(''); // remove the value from the input#}
            document.getElementById("image").src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (data) {
            alert('error');
        }
    });
});


/**
 * Created by long on 10/11/17.
 */
var image = document.getElementById('image');
var naturalWidth = image.naturalWidth;
var naturalHeight = image.naturalHeight;

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

function createPaint(parent) {
    var canvas = elt("canvas", {width: 500, height: 400});
    // {#    var canvas = document.getElementById("myCanvas");#}
    // {#    var canvas = elt("myCanvas", {width: 500, height: 300});#}
    var cx = canvas.getContext("2d");
    var image = document.getElementById("image");
    var color = cx.fillStyle, size = cx.lineWidth;
    color = 'rgb(0, 255, 0)';
    // cx.canvas.width = image.width;
    // cx.canvas.height = image.height;
    cx.canvas.width = naturalWidth;
    cx.canvas.height = naturalHeight;
    // {#            cx.drawImage(image, 0, 0);#}
    cx.fillStyle = color;
    cx.strokeStyle = color;
    cx.lineWidth = size;
    var toolbar = elt("div", {class: "toolbar"});
    for (var name in controls)
        toolbar.appendChild(controls[name](cx));

    // var panel = elt("div", {class: "picturepanel"}, canvas);
    var canvasWrapper = document.getElementById('canvas-wrapper');
    // parent.appendChild(elt("div", null, panel, toolbar));
    canvasWrapper.appendChild(canvas);
    var canvasToolbar = document.getElementById('canvas-toolbar');
    canvasToolbar.appendChild(toolbar);
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
    var options = {'add': 'rgb(0, 255, 0)', 'remove': 'rgb(255, 64, 64)' };
    for (option in options){

            input.appendChild(elt("option", {value: options[option]}, option ));

    };
    input.addEventListener("change", function(){
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


function updateImageChange(cx) {
    var image = document.getElementById("image");
    //
    // {#            var color = cx.fillStyle, size = cx.lineWidth;#}
    // {#                cx.canvas.width = image.width;#}
    // {#                cx.canvas.height = image.height;#}
    // {#            cx.drawImage(image, 0, 0);#}
    // {#            cx.fillStyle = color;#}
    // {#            cx.strokeStyle = color;#}
    // {#            cx.lineWidth = size;#}
    var canvasWrapper = document.getElementById('canvas-wrapper');
    canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
}

controls.updateImage = function (cx) {

    var form = elt("form", null,
        elt("button", {type: "submit"}, "Load image changes"));
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        updateImageChange(cx);
    });
    return form;
};

function saveCanvas(cx) {
    var data = cx.getImageData(0, 0, cx.canvas.width, cx.canvas.height).data;
    console.log(data);
    // console.log(JSON.stringify(data));
    var jpegUrl = cx.canvas.toDataURL("image/jpeg");
    console.log(jpegUrl);

    // return data;
    var image = document.getElementById('image');
    // image.src = jpegUrl;

    $.ajax({
        url: "update-mask/",
        type: "POST",
        data: {
            mask: jpegUrl,
        },
        success: function(data){
            image.src =  "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
            disp_hist_thumbnail(data);
        },
        error: function(data){
            alert('error');
        }
    });
}

controls.saveDrawing = function (cx) {
    var form = elt("form", null,
        elt("button", {type: "submit"},"Save the drawing"
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
        


