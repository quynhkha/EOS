// $("#btn_table_1").onclick(function(e){
//     e.preventDefault();
//     mask_id = document.getElementById('mask_id');
//     url
//     }
//
// );
$(".btn_modal_show_individual_crystal").click(function (e) {
        e.preventDefault();
      crystal_id = $(this).val();
    $.ajax({
        type: "GET",
        url: '/modal-show-individual-crystal/'+ crystal_id.toString() + "/",
         beforeSend: function () {
            document.body.style.cursor = "wait";
            document.getElementById('modal-crystal-img').src ='';
        },
           complete: function () {
            document.body.style.cursor = "default";
        },
        success: function (data) {
          document.getElementById('modal-crystal-img').src = "data:image/jpeg;charset=utf-8;base64,"+data['image_data'];
          document.getElementById('modal-crystal-name').innerText = data['image_name'];
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});

function plot_confusion_graph(data){
    var graph_data = [
  {
    x: data['labels'],
    y: data['similarities'],
    type: 'bar'
  }
];

Plotly.newPlot('confusion-graph', graph_data);
}

$(".btn_modal_show_conf_graph").click(function (e) {
    e.preventDefault();
    id = $(this).val();
    $.ajax({
        type: "GET",
        url: "/modal-show-conf-graph/" + id.toString() + "/" ,

        success: function (data) {
            plot_confusion_graph(data);
            console.log(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});



/************** HISTOGRAM ***************/
var original_hist = {};
var truncated_hist = {};
var composition_hist = {};

// var truncated_hist = {};
function plot_pixel_histogram(data) {

    original_hist = {x: data["x"], y: data["y"]};
    console.log(original_hist);

    var hist_data = [{
        x: data["x"],
        y: data["y"],
        // {#                x: [1,2,3],#}
        // {#                y: [10,11,12],#}
        type: 'bar'
    }];
    Plotly.newPlot('pixel_histogram', hist_data);
}

function plot_area_histogram(data) {

    original_hist = {x: data["x"], y: data["y"]};
    console.log(original_hist);

    var hist_data = [{
        x: data["x"],
        y: data["y"],
        // {#                x: [1,2,3],#}
        // {#                y: [10,11,12],#}
        type: 'bar'
    }];
    Plotly.newPlot('area_histogram', hist_data);
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
        var step = parseInt(100 / range);
        var i = 0;
        for (i = 0; i < 100; i++) {
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
    Plotly.newPlot('histogram', hist_data);
}

function plot_composition(data, a, b) {
    var step;
    var x_arr = [];
    var y_arr = [];
    var a = parseFloat(a);
    var b = parseInt(b);
    var data_length = parseInt(data["x"].length * a) + 1;

    if (a < 1) {
        var j = 0;
        step = parseInt(1 / a) + 1;
        for (var i = 0; i < data_length; i++) {
            var x = i;
            var y = 0;
            while (j < i * step && j < data["x"].length) {
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
        for (var i = 0; i < data_length; i++) {
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
    for (var i = 0; i < b; i++) {
        new_x_arr.push(0);
        new_y_arr.push(0);
    }
    for (var i = 0; i < x_arr.length; i++) {
        new_x_arr.push(x_arr[i] + b);
        new_y_arr.push(y_arr[i]);
    }

    console.log(new_x_arr, new_y_arr);

    composition_hist = {x: new_x_arr, y: new_y_arr};
    var hist_data = [{
        x: composition_hist["x"],
        y: composition_hist["y"],
        type: 'bar'
    }];
    Plotly.newPlot('histogram', hist_data);
    return composition_hist

}


$("#btn_pixel_histogram").click(function (e) {
     e.preventDefault();
       mask_id = $(this).val();
    $.ajax({
        type: "GET",
        url: "/pixel_histogram/" + mask_id.toString() + "/" ,

        success: function (data) {
            plot_pixel_histogram(data);
            console.log(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});

$("#btn_area_histogram").click(function (e) {
     e.preventDefault();
       mask_id = $(this).val();
    $.ajax({
        type: "GET",
        url: "/area_histogram/" + mask_id.toString() + "/" ,

        success: function (data) {
            plot_area_histogram(data);
            console.log(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});

// $(".btn_modal_show_histogram").click(function (e) {
//     e.preventDefault();
//        mask_id = $(this).val();
//     $.ajax({
//         type: "GET",
//         url: "/histogram/" + mask_id.toString() + "/" ,
//
//         success: function (data) {
//             plot_histogram(data);
//             console.log(data);
//         },
//         error: function (data) {
//             console.log(data);
//             alert('error');
//         }
//     });
// });

//
// // TODO: not using ajax
// $(".btn_process_crystal").click(function (e) {
//     e.preventDefault();
//        mask_id = $(this).val();
//     url= "/crystal_processing/" + mask_id.toString() + "/" ;
//     $('.form_process_crystal').attr('action', url).submit();
// });

$("#btn_truncated_hist").click(function (e) {
    e.preventDefault();
    hist_min_thresh = $("#hist_min_thresh").val();
    hist_max_thresh = $("#hist_max_thresh").val();
    console.log(hist_min_thresh, hist_max_thresh);

    var is_valid = true;
    if (parseInt(hist_min_thresh) < 0 || parseInt(hist_min_thresh) > 255) {
        alert("min threshold value range should be in range [0-255]");
        is_valid = false;
    }

    if (parseInt(hist_max_thresh) < 0 || parseInt(hist_max_thresh) > 255) {
        alert("max threshold value range should be in range [0-255]");
        is_valid = false;
    }

    if (parseInt(hist_min_thresh) >= parseInt(hist_max_thresh)) {
        alert("min threshold should smaller than max threshold");
        is_valid = false;
    }
    if (is_valid) {
        plot_truncated_histogram(original_hist, hist_min_thresh, hist_max_thresh);
    }
    else {
        alert("invalid range. please input range again");
    }

});

$("#btn_comp").click(function (e) {
    e.preventDefault();
    a = $("#comp_a").val();
    b = $("#comp_b").val();
    console.log(a, b);


    var is_valid = true;
    if (parseFloat(a) <= 0 || parseFloat(b) < 0) {
        alert("a should be positive and b should be non-negative");
        is_valid = false;
    }


    if (is_valid) {
        composition_hist=plot_composition(truncated_hist, a, b);

    }

    else {
        alert("invalid composition value. Please input again.")
    }
});

// function send_composition(composition_hist){
//      $.ajax({
//         type: "GET",
//         url: '/update-composition/'+ mask_id.toString() + "/",
//          beforeSend: function () {
//             document.body.style.cursor = "wait";
//             document.getElementById('modal-crystal-img').src ='';
//         },
//            complete: function () {
//             document.body.style.cursor = "default";
//         },
//         success: function (data) {
//           document.getElementById('modal-crystal-img').src = "data:image/jpeg;charset=utf-8;base64,"+data['image_data'];
//           document.getElementById('modal-crystal-name').innerText = data['image_name'];
//         },
//         error: function (data) {
//             console.log(data);
//             alert('error');
//         }
//     });
// }

//
// function post(path, params, method) {
//     method = method || "post"; // Set method to post by default if not specified.
//
//     // The rest of this code assumes you are not using a library.
//     // It can be made less wordy if you use one.
//     var form = document.createElement("form");
//     form.setAttribute("method", method);
//     form.setAttribute("action", path);
//
//     for(var key in params) {
//         if(params.hasOwnProperty(key)) {
//             var hiddenField = document.createElement("input");
//             hiddenField.setAttribute("type", "hidden");
//             hiddenField.setAttribute("name", key);
//             hiddenField.setAttribute("value", params[key]);
//
//             form.appendChild(hiddenField);
//         }
//     }
//
//     document.body.appendChild(form);
//     form.submit();
// }


$("#gen_crystal_processing_result").click(function(e){
   var overall_thresh = $("#overall_thresh").val();
   var pair_thresh = $("#pair_thresh").val();
   var trunc_min = $("#hist_min_thresh").val();
   var trunc_max = $("#hist_max_thresh").val();
   var comp_a = $("#comp_a").val();
   var comp_b = $("#comp_b").val();


   post('/gen-crystal-processing-result', {})
});