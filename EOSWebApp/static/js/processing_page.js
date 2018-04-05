// import {do_ajax_get, do_ajax_post_val_only, do_ajax_post} from 'utils.js';
/****************** THUMBNAIL ******************/
function disp_hist_thumbnail(data) {
    var hist_thumbnail_data_arr = data["thumbnail_arr"];
    $('#hist-thumbnail').empty();
    //remove all the zoom div
    //remove all the zoom div
    $('.zoomContainer').remove();
    for (i = 0; i < hist_thumbnail_data_arr.length; i++) {
        var thumbnail_id = "thumb_" + i;
        $('#hist-thumbnail').prepend($('<img>', {
            id: thumbnail_id,
            class: "img-fluid centered thumbnail",
            src: "data:image/jpeg;charset=utf-8;base64," + hist_thumbnail_data_arr[i]['image_data'],
            onmouseover: "on_hover_thumbnail(id)",
            onclick: "on_click_thumbnail(id)",

        }));

    }
}

function on_hover_thumbnail(thumbnail_id) {
    id = thumbnail_id.split("_")[1];
    var URL = "/large-thumbnail/" + id + "/";
    var large_thumbnail_src = '';
    var image = new Image();
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
            large_thumbnail_src = "data:image/jpeg;charset=utf-8;base64," + data['image_data'];
            image.src = large_thumbnail_src;
            console.log('image height', 'image width', image.height, image.width, thumbnail_id);
            document.getElementById(thumbnail_id).setAttribute('data-zoom-image', image.src);

            $("#" + thumbnail_id).elevateZoom({
                zoomWindowFadeIn: 0,
                zoomWindowFadeOut: 0,
                lensFadeIn: 500,
                lensFadeOut: 500,
                zoomWindowWidth: 640,
                zoomWindowHeight: 480,
                scrollZoom: true,
                //         zoomType				: "lens",
                // lensShape : "round",
                // lensSize    : 200,
            });
        },

        error: function (data) {
            alert('error');
        }

    });
}


function on_click_thumbnail(thumbnail_id) {
    console.log("thumbnail id: ", thumbnail_id);
    do_ajax_post_val_only([thumbnail_id], ['input'], '/img-from-thumbnail/');
}

function imageToDataUri(img, width, height) {

    // create an off-screen canvas
    var canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d');

    // set its dimension to target size
    canvas.width = width;
    canvas.height = height;

    // draw source image into the off-screen canvas:
    ctx.drawImage(img, 0, 0, width, height);

    // encode image to data-uri with base64 version of compressed image
    return canvas.toDataURL();
}


function disp_slider_val(dispDom, sliderDom) {
    $("#" + dispDom + "").val($("#" + sliderDom + "").val());
    return $("#" + sliderDom + "").val();
}

var clickableCtrlList = [];
var unclickableCtrlList = [];
var currentCtrlName = '';

function ctrlObject(ctrlDom, ctrlName) {
    this.ctrlDom = ctrlDom;
    this.ctrlName = ctrlName;

}

var ctrlUpload = new ctrlObject('btn_upload', 'upload');

var ctrlLaplacian = new ctrlObject('btn_laplacian', 'laplacian');

var ctrlLowThresh = new ctrlObject('slider-lower-thresh', 'lower thresholding');
var ctrlUpThresh = new ctrlObject('slider-upper-thresh', 'upper thresholding');

var ctrlKmeans = new ctrlObject('slider-kmeans', 'kmeans');
var ctrlExtrMask = new ctrlObject('btn_extract_crystal_mask', 'extract crystal mask');

var ctrlAllCrys = new ctrlObject('btn_all_crystal', 'show all crystals');
var ctrlTopCrys = new ctrlObject('btn_extract_top_crystal', 'top area crystals');

// var ctrlOpeningKer = new ctrlObject('slider-opening-kernel', 'opening');
// var ctrlOpeningIter = new ctrlObject('slider-opening-iter', 'opening');
//
// var ctrlClosingKer = new ctrlObject('slider-closing-kernel', 'closing');
// var ctrlClosingIter = new ctrlObject('slider-closing-iter', 'closing');
//
// var ctrlErosionKer = new ctrlObject('slider-erosion-kernel', 'erosion');
// var ctrlErosionIter = new ctrlObject('slider-erosion-iter', 'erosion');
//
// var ctrlDilationKer = new ctrlObject('slider-dilation-kernel', 'dilation');
// var ctrLDilationIter = new ctrlObject('slider-dilation-iter', 'dilation');

var ctrlOpening = new ctrlObject('slider-opening', 'opening');
var ctrlClosing = new ctrlObject('slider-closing', 'closing');
var ctrlErosion = new ctrlObject('slider-erosion', 'erosion');
var ctrlDilation = new ctrlObject('slider-dilation', 'dilation');

var ctrlUndo = new ctrlObject('', '');
var ctrlReset = new ctrlObject('btn_reset', 'reset');

var ctrlBrush = new ctrlObject('', '');

var ctrlHist = new ctrlObject('btn_histogram', 'plot histogram');
var ctrlTruncHist = new ctrlObject('btn_truncated_hist', 'plot truncated histogram');
var ctrlComp = new ctrlObject('btn_comp', 'plot composition');


function update_clickable_stt(currentCtrlName) {
    currentCtrlName = currentCtrlName;
    // var morphCtrlGrp = [ctrlErosionIter, ctrlErosionKer, ctrLDilationIter, ctrlDilationKer,
    //     ctrlClosingIter, ctrlClosingKer, ctrlOpeningIter, ctrlOpeningKer];
    var morphCtrlGrp = [ctrlOpening, ctrlClosing, ctrlErosion, ctrlDilation];
    var histCtrlGrp = [ctrlHist, ctrlTruncHist, ctrlComp];
    var crysCtrlGrp = [ctrlAllCrys, ctrlTopCrys];
    var threshCtrlGrp = [ctrlLowThresh, ctrlUpThresh];
    var kmeansCtrlGrp = [ctrlKmeans, ctrlExtrMask];

    console.log('case', currentCtrlName);
    switch (currentCtrlName) {

        case 'upload':
            clickableCtrlList = [ctrlLaplacian];
            clickableCtrlList = clickableCtrlList.concat(threshCtrlGrp);

            unclickableCtrlList = [ctrlKmeans, ctrlBrush];
            unclickableCtrlList = unclickableCtrlList.concat(crysCtrlGrp);

            break;
        // case 'laplacian':
        //     clickableCtrlList = [ctrlLaplacian];
        //     unclickableCtrlList = unclickableCtrlList.concat(morphCtrlGrp, histCtrlGrp, crysCtrlGrp, threshCtrlGrp, kmeansCtrlGrp);
        //     break;

        case 'kmeans':
            clickableCtrlList = kmeansCtrlGrp;

            unclickableCtrlList = [ctrlLaplacian, ctrlBrush];
            unclickableCtrlList = unclickableCtrlList.concat(morphCtrlGrp, histCtrlGrp, crysCtrlGrp, threshCtrlGrp);
            break;

        case 'extract crystal mask':
            clickableCtrlList = [ctrlBrush];
            clickableCtrlList = clickableCtrlList.concat(morphCtrlGrp, crysCtrlGrp);

            unclickableCtrlList = [ctrlLaplacian, ctrlBrush];
            unclickableCtrlList = unclickableCtrlList.concat(threshCtrlGrp, histCtrlGrp);
            break;

        default:
            clickableCtrlList = [ctrlBrush, ctrlLaplacian, ctrlUndo, ctrlReset];
            clickableCtrlList = clickableCtrlList.concat(morphCtrlGrp, histCtrlGrp, crysCtrlGrp, threshCtrlGrp, kmeansCtrlGrp);

            unclickableCtrlList = [];
    }
    console.log('unclickable control', unclickableCtrlList);

    set_click_ability(clickableCtrlList, true);
    set_click_ability(unclickableCtrlList, false);
}

function update_image(data) {
    document.getElementById('image').src = "data:image/jpeg;charset=utf-8;base64," + data["image_data"];
    canvasWrapper = document.getElementById('canvas-wrapper');
    canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
}

function update_clickable(data) {
    update_clickable_stt(data["func_name"]);
}

function update_gray_levels(data) {

    var grayLevelDom = document.getElementById('label-extraction');
    if (!document.getElementById('gray-level-list')) {
        var grayLevelList = elt("div", {id: "gray-level-list"});
        grayLevelList.className += "dropdown-menu";

        grayLevelDom.appendChild(grayLevelList);
    }
    else {
        var grayLevelList = document.getElementById('gray-level-list');
    }

    //update the list content
    //update with new list content if kmeans is done
    if (data['gray_levels'] != '') {
        grayLevelList.innerHTML = '';
        var grayLevels = data["gray_levels"];
        for (var i = 0; i < grayLevels.length; i++) {
            // var style = "background-color: rgb("+grayLevels[i].toString()+");";
            var style = "background-color: rgb(" + grayLevels[i] + "," + grayLevels[i] + "," + grayLevels[i] + ");";
            var listElement = elt("li", {value: i, style: style}, "region: " + i);
            listElement.className += "dropdown-item";


            listElement.addEventListener("click", extract_mask, false);
            console.log(listElement);
            grayLevelList.appendChild(listElement);
        }
    }

    else {
        //clear the list if not extract mask clicked
        if (currentCtrlName != 'extract crystal mask') {

            // while (grayLevelDom.firstChild){
            //     grayLevelDom.remove(firstChild);
            // }
            grayLevelList.innerHTML = '';
            var listElement = elt("li", null, "No region to choose");
            listElement.className += "dropdown-item";
            grayLevelList.appendChild(listElement);

        }
    }
}

function extract_mask() {
    var label_index = this.value;
    do_ajax_post_val_only([label_index], ['input'], '/extract-crystal-mask/', [label_index]);
    console.log("label: ", label_index);
}

function get_temp_index() {
    // tempIndexText = document.getElementById('temp-index').innerText.toString();
    // return parseInt(tempIndexText);
    return ''
}

function set_click_ability(ctrlList, clickable) {
    var style = "";
    var opacity = "";
    if (clickable) {
        style = "auto";
        opacity = 1.0;
    }
    else {
        style = "none";
        opacity = 0.4;
    }
    for (var i = 0; i < ctrlList.length; i++) {
        var ctrlElement = ctrlList[i];
        var element = document.getElementById(ctrlElement.ctrlDom);
        // console.log(element);
        if (element != null) {
            element.style.pointerEvents = style;
            element.style.opacity = opacity;
        }

    }
}


function morphCtrlMapping(input) {
    var kernel = 1;
    var iter = 1;
    image = document.getElementById('image');
    var naturalWidth = image.naturalWidth;
    var coeff = Math.floor(naturalWidth / 2000) + 1; //base case: width = 500 -> coeff =1

    input = parseInt(input);
    switch (input) {
        case 1:
            kernel = 1;
            iter = 1;
            break;
        case 2:
            kernel = 2;
            iter = 1;
            break;
        case 3:
            kernel = 3;
            iter = 1;
            break;
        case 4:
            kernel = 4;
            iter = 1;
            break;
        case 5:
            kernel = 3;
            iter = 2;
            break;
        case 6:
            kernel = 4;
            iter = 2;
            break;
        case 7:
            kernel = 5;
            iter = 2;
            break;
        case 8:
            kernel = 6;
            iter = 2;

            break;
        case 9:
            kernel = 4;
            iter = 3;
            break;
        case 10:
            kernel = 5;
            iter = 3;
            break;
        case 11:
            kernel = 6;
            iter = 3;
            break;
        case 12:
            kernel = 7;
            iter = 3;
            break;
        case 13:
            kernel = 5;
            iter = 4;
            break;
        case 14:
            kernel = 6;
            iter = 4;
            break;
        case 15:
            kernel = 7;
            iter = 4;
            break;
        default:
            kernel = 1;
            iter = 1;
            break;
    }
    return {'kernel_size': kernel * coeff, 'num_of_iter': iter};
}

/******************* DOM EVENT HANDLING *********************/
$("#btn_laplacian").click(function (e) {
    do_ajax_get(e, '/laplacian/', {'update_image': true});
});


$("#slider-lower-thresh-white").change(function (e) {
    disp_slider_val('slider-val-lower-thresh-white', 'slider-lower-thresh-white');
    do_ajax_post(e, ['slider-lower-thresh-white'], ['input'], '/lower-thresholding-white/', ['slider-val-lower-thresh-white', 'slider-lower-thresh-white'], {'update_image': true});
});

$("#slider-upper-thresh-white").change(function (e) {
    disp_slider_val('slider-val-upper-thresh-white', 'slider-upper-thresh-white');
    do_ajax_post(e, ['slider-upper-thresh-white'], ['input'], '/upper-thresholding-white/', ['slider-val-upper-thresh-white', 'slider-upper-thresh-white'], {'update_image': true});
});

$("#slider-lower-thresh-black").change(function (e) {
    disp_slider_val('slider-val-lower-thresh-black', 'slider-lower-thresh-black');
    do_ajax_post(e, ['slider-lower-thresh-black'], ['input'], '/lower-thresholding-black/', ['slider-val-lower-thresh-black', 'slider-lower-thresh-black'], {'update_image': true});
});

$("#slider-upper-thresh-black").change(function (e) {
    disp_slider_val('slider-val-upper-thresh-black', 'slider-upper-thresh-black');
    do_ajax_post(e, ['slider-upper-thresh-black'], ['input'], '/upper-thresholding-black/', ['slider-val-upper-thresh-black', 'slider-upper-thresh-black'], {'update_image': true});
});


$("#slider-kmeans").click(function (e) {
    disp_slider_val('slider-val-kmeans', 'slider-kmeans');
    do_ajax_post(e, ['slider-kmeans'], ['input'], '/kmeans/', ['slider-val-kmeans', 'slider-kmeans'], {'update_image': true});
});

$("#btn_extract_crystal_mask").click(function (e) {
    do_ajax_post(e, ['crystal_label'], ['input'], '/extract-crystal-mask/', ['crystal_label'], {'update_image': true});
});

$("#slider-opening").click(function (e) {
    input_val = disp_slider_val('slider-val-opening', 'slider-opening');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/opening/', ['slider-val-opening', 'slider-opening'], {'update_image': true});
});

$("#slider-closing").click(function (e) {
    input_val = disp_slider_val('slider-val-closing', 'slider-closing');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/closing/', ['slider-val-closing', 'slider-closing'], {'update_image': true});
});

$("#slider-erosion").click(function (e) {
    input_val = disp_slider_val('slider-val-erosion', 'slider-erosion');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/erosion/', ['slider-val-erosion', 'slider-erosion'], {'update_image': true});
});

$("#slider-dilation").click(function (e) {
    input_val = disp_slider_val('slider-val-dilation', 'slider-dilation');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/dilation/', ['slider-val-dilation', 'slider-dilation'], {'update_image': true});
});

$("#slider-morphgrad").click(function (e) {
    input_val = disp_slider_val('slider-val-morphgrad', 'slider-morphgrad');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/morphgrad/', ['slider-val-morphgrad', 'slider-morphgrad'], {'update_image': true});
});
$("#slider-tophat").click(function (e) {
    input_val = disp_slider_val('slider-val-tophat', 'slider-tophat');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/tophat/', ['slider-val-tophat', 'slider-tophat'], {'update_image': true});
});
$("#slider-blackhat").click(function (e) {
    input_val = disp_slider_val('slider-val-blackhat', 'slider-blackhat');
    kernel_iter_val = morphCtrlMapping(input_val);
    console.log(input_val, kernel_iter_val);
    do_ajax_post_val_only([kernel_iter_val['kernel_size'], kernel_iter_val['num_of_iter']], ['kernel_size', 'num_of_iter'], '/blackhat/', ['slider-val-blackhat', 'slider-blackhat'], {'update_image': true});
});
// $("#slider-opening-kernel").change(function (e) {
//     disp_slider_val('slider-opening-val-kernel', 'slider-opening-kernel');
//     do_ajax_post(e, ['slider-opening-kernel', 'slider-opening-iter'], ['kernel_size', 'num_of_iter'], '/opening/');
// });
//
//
// $("#slider-opening-iter").change(function (e) {
//     disp_slider_val('slider-opening-val-iter', 'slider-opening-iter');
//     do_ajax_post(e, ['slider-opening-kernel', 'slider-opening-iter'], ['kernel_size', 'num_of_iter'], '/opening/');
// });
//
//
// $("#slider-closing-kernel").change(function (e) {
//     disp_slider_val('slider-closing-val-kernel', 'slider-closing-kernel');
//     do_ajax_post(e, ['slider-closing-kernel', 'slider-closing-iter'], ['kernel_size', 'num_of_iter'], '/closing/');
// });
//
//
// $("#slider-closing-iter").change(function (e) {
//     disp_slider_val('slider-closing-val-iter', 'slider-closing-iter');
//     do_ajax_post(e, ['slider-closing-kernel', 'slider-closing-iter'], ['kernel_size', 'num_of_iter'], '/closing/');
// });
//
//
// $("#slider-erosion-kernel").change(function (e) {
//     disp_slider_val('slider-erosion-val-kernel', 'slider-erosion-kernel');
//     do_ajax_post(e, ['slider-erosion-kernel', 'slider-erosion-iter'], ['kernel_size', 'num_of_iter'], '/erosion/');
// });
//
//
// $("#slider-erosion-iter").change(function (e) {
//     disp_slider_val('slider-erosion-val-iter', 'slider-erosion-iter');
//     do_ajax_post(e, ['slider-erosion-kernel', 'slider-erosion-iter'], ['kernel_size', 'num_of_iter'], '/erosion/');
// });
//
//
// $("#slider-dilation-kernel").change(function (e) {
//     disp_slider_val('slider-dilation-val-kernel', 'slider-dilation-kernel');
//     do_ajax_post(e, ['slider-dilation-kernel', 'slider-dilation-iter'], ['kernel_size', 'num_of_iter'], '/dilation/');
// });
//
//
// $("#slider-dilation-iter").change(function (e) {
//     disp_slider_val('slider-dilation-val-iter', 'slider-dilation-iter');
//     do_ajax_post(e, ['slider-dilation-kernel', 'slider-dilation-iter'], ['kernel_size', 'num_of_iter'], '/dilation/');
// });

$("#btn_fourier").click(function (e) {
    do_ajax_get(e, '/fourier/', {'update_image': true})
});

$("#btn_backproj").click(function (e) {
    do_ajax_get(e, '/backproj/', {'update_image': true})
});
$("#btn_noise_removal").click(function (e) {
    do_ajax_post(e, ['area_thresh'], ['input'], '/noise-removal/', ['area_thresh'], {'update_image': true})
});

// $("#btn_fill_hole").click(function (e) {
//     do_ajax_post(e, ['fill_lo', 'fill_hi', 'fill_conn', 'fill_fixed_range'],['lo','hi', 'conn', 'fixed_range'], '/fill-holes/', {'update_image': true});
// });

$("#btn_fill_hole").click(function (e) {
    do_ajax_get(e, '/fill-holes/', {'update_image': true});
});

$("#btn_all_crystal").click(function (e) {
    do_ajax_get(e, '/all-crystal/', {'update_image': true});
});

$("#btn_extract_top_crystal").click(function (e) {
    do_ajax_post(e, ['num_crystal_label'], ['input'], '/top-crystal/', ['num_crystal_label'], {'update_image': true});
});


// $("#btn_max_crystal").click(function (e) {
//     do_ajax_get(e, '/max-crystal/');
// });


$("#btn_reset").click(function (e) {
    do_ajax_get(e, '/reset/', {'update_image': true});
});

$("#btn_base64").click(function (e) {
    do_ajax_get(e, '/base64/', {'update_image': true});
});

$("#btn_save_crystal").click(function (e) {
    e.preventDefault();
    json_data = {'name': $("#crystal_name").val()};
    $.ajax({
        type: "POST",
        url: '/save-processed/',
        data: json_data,
        success: function (data) {
            alert("Image saved sucessfully!");
            document.getElementById('mask_id').value = data['mask_id'];
            set_click_ability([ctrlToCrysProcess], true); //now user can process to next page
            console.log(data);
        },
        error: function (data) {
            console.log(data);
            alert('error');
        }
    });
});
/************* TO CRYSTAL PROCESSING PAGE ************/
var ctrlToCrysProcess = new ctrlObject("btn_to_crystal_process", "To crystal process");
//init set the clickable to false
set_click_ability([ctrlToCrysProcess], false);
//
// $("#btn_to_crystal_process").click(function(e){
//     mask_id
// });


/************ UNDO/RESET ************************/
function reset_func_setting(data) {
    func_setting = data['func_setting'];
    if (data['func_setting'] != "") {
        func_setting = JSON.parse(func_setting);
        if (Array.isArray(func_setting)) {
            for (var i = 0; i < func_setting.length; i++) {
                setting = func_setting[i];

                $("#" + setting['domName'] + "").val(setting['domVal']);
            }
        }
    }

}


$("#btn_undo").click(function (e) {

    // do_ajax_get(e, '/undo/', {'update_image': true});
    URL = '/undo/';
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
            update_clickable(data);
            disp_hist_thumbnail(data);
            update_gray_levels(data);
            reset_func_setting(data);
        },

        error: function (data) {
            alert('error');
        }

    });
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
        document.body.style.cursor = "cursor: url(cursor.png)";
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

    do_ajax_post_val_only([jpegUrl], ['mask'], '/update-mask/', []);
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

controls.clearDrawing = function (cx) {
    var form = elt("form", null,
        elt("button", {type: "submit"}, "Clear drawing"
        ));
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        //if canvas is shown
        if (cx.canvas.style.display == "block") {
            cx.clearRect(0, 0, cx.canvas.width, cx.canvas.height);
        }
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
