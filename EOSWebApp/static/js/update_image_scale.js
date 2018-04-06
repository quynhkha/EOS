// use this canvas wrapper to display image as background image.
// Canvas will overlay this background image
// because the image and canvas are resized by css to fit view,
// so far it is only workable way for both of them having same size
var canvasWrapper = document.getElementById('canvas-wrapper');

// hidden image (to have img src for later drawing)
var image = document.getElementById("scale-canvas-img");

// original image size
var imageNaturalWidth = image.naturalWidth;
var imageNaturalHeight = image.naturalHeight;

// current image size (resized by css to fit the screen view)
var imageWidth = image.width;
var imageHeight = image.height;


var canvas = document.getElementById("scale-canvas");
var ctx = canvas.getContext("2d");

// set canvas size to current image size
canvas.width = imageWidth;
canvas.height = imageHeight;

var startX, startY, mouseX, mouseY;
var isDown = false;


function initScaleCanvas() {
    ctx.strokeStyle = "green";
    ctx.lineWidth = 3;
    // set the wrapper size to current canvas size
    setCanvasWrapperSize();

    // draw the image to canvas wrapper
    drawTheImage();


    $("#scale-canvas").mousedown(function (e) {
        handleMouseDown(e);
    });
    $("#scale-canvas").mousemove(function (e) {
        handleMouseMove(e);
    });
    $("#scale-canvas").mouseup(function (e) {
        handleMouseUp(e);
    });
    $("#scale-canvas").mouseout(function (e) {
        handleMouseUp(e);
    });


}

function draw() {
    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // redraw the image
    drawTheImage();

    // draw the current line
    drawLine({x1: startX, y1: startY, x2: mouseX, y2: mouseY});
}

function drawTheImage() {
    canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
}

function drawLine(line) {
    ctx.beginPath();
    ctx.moveTo(line.x1, line.y1);
    ctx.lineTo(line.x2, line.y2);
    ctx.stroke();
}

// track the mouse position on the canvas
function relativePos(event, element) {
    var rect = element.getBoundingClientRect();
    return {
        x: Math.floor(event.clientX - rect.left),
        y: Math.floor(event.clientY - rect.top)
    };
}

function handleMouseDown(e) {
    e.stopPropagation();
    e.preventDefault();

    var pos = relativePos(e, ctx.canvas);
    mouseX = pos.x;
    mouseY = pos.y;

    startX = mouseX;
    startY = mouseY;
    isDown = true;
}

function handleMouseUp(e) {
    e.stopPropagation();
    e.preventDefault();

    isDown = false;
    console.log(startX, startY, mouseX, mouseY);
    console.log(mouseX - startX, mouseY - startY);
    updateDistance();
}

function handleMouseMove(e) {
    if (!isDown) {
        return;
    }
    e.stopPropagation();
    e.preventDefault();
    // mouseX = parseInt(e.clientX - offsetX);
    // mouseY = parseInt(e.clientY - offsetY);
    var pos = relativePos(e, ctx.canvas);
    mouseX = pos.x;
    mouseY = pos.y;
    // Put your mousemove stuff here
    draw();
}

function getElementSize(elementId) {
    var element = document.getElementById(elementId);
    var boundingBox = element.getBoundingClientRect();
    var elementWidth = boundingBox.right - boundingBox.left;
    var elementHeight = boundingBox.bottom - boundingBox.top;
    return {width: elementWidth, height: elementHeight};
}


function setCanvasWrapperSize() {
    canvasWrapperSize = getElementSize('canvas-wrapper');
    var canvasWrapperHeight = Math.floor(imageHeight * canvasWrapperSize.width / imageWidth) + 1;
    canvasWrapper.style.height = canvasWrapperHeight.toString() + 'px';
}


function updateDistance() {
    var relativeDist = Math.sqrt((mouseX - startX) * (mouseX - startX) +
        (mouseY - startY) * (mouseY - startY));
    var realPixelDist = parseInt(relativeDist * imageNaturalWidth / imageNaturalWidth);
    $("#pixel-dist").val(realPixelDist);
    console.log('realPixelDist', realPixelDist);
}


$("#update_scale").click(function (e){
     URL = '/update-scale/';
     var json_data = {};
        json_data['image_id'] = $("#image_id").val();
         json_data['pixel_dist'] = $("#pixel-dist").val();
         json_data['real_dist'] =  $("#real-dist").val();
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
                alert("Image scale updated!");
        },

        error: function (data) {
            alert('error');
        }

    });
});