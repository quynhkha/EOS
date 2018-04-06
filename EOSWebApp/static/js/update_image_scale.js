function initScaleCanvas() {

    // hidden image (to have img src for later drawing)
    var image = document.getElementById("scale-canvas-img");
    image.onload = start;

    // original image size
    var imageNaturalWidth = image.naturalWidth;
    var imageNaturalHeight = image.naturalHeight;

    // current image size (resized by css to fit the screen view)
    var imageWidth = image.width;
    var imageHeight = image.height;

    // use this canvas wrapper to display image as background image.
    // Canvas will overlay this background image
    // because the image and canvas are resized by css to fit view,
    // so far it is only workable way for both of them having same size
    var canvasWrapper = document.getElementById('canvas-wrapper');

    var canvas = document.getElementById("scale-canvas");
    var ctx = canvas.getContext("2d");

    // set canvas size to current image size
    canvas.width = imageWidth;
    canvas.height = imageHeight;

    // set canvas mouse offset (for later calculation of mouse pos)
    var canvasOffset = $("#scale-canvas").offset();
    var offsetX = canvasOffset.left;
    var offsetY = canvasOffset.top;

    var startX, startY, mouseX, mouseY;
    var isDown = false;

    // set the wrapper size to current canvas size
    setCanvasWrapperSize();

    function start() {
        ctx.strokeStyle = "green";
        ctx.lineWidth = 3;

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

        // draw the image to canvas wrapper
        drawTheImage(image);

    }

    function draw(toX, toY) {
        // clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // redraw the image
        drawTheImage(image);

        // draw the current line
        drawLine({x1: startX, y1: startY, x2: mouseX, y2: mouseY});
    }

    function drawTheImage(image) {
        canvasWrapper.style.backgroundImage = "url('" + image.src + "')";
    }

    function drawLine(line) {
        ctx.beginPath();
        ctx.moveTo(line.x1, line.y1);
        ctx.lineTo(line.x2, line.y2);
        ctx.stroke();
    }


    function handleMouseDown(e) {
        e.stopPropagation();
        e.preventDefault();
        mouseX = parseInt(e.clientX - offsetX);
        mouseY = parseInt(e.clientY - offsetY);

        // Put your mousedown stuff here
        startX = mouseX;
        startY = mouseY;
        isDown = true;
    }

    function handleMouseUp(e) {
        e.stopPropagation();
        e.preventDefault();

        // Put your mouseup stuff here
        isDown = false;
        // lines.push({x1: startX, y1: startY, x2: mouseX, y2: mouseY});
        // console.log(lines);
        console.log(startX, startY, mouseX, mouseY);
        console.log(mouseX - startX, mouseY - startY);
        calScale();
    }

    function handleMouseMove(e) {
        if (!isDown) {
            return;
        }
        e.stopPropagation();
        e.preventDefault();
        mouseX = parseInt(e.clientX - offsetX);
        mouseY = parseInt(e.clientY - offsetY);

        // Put your mousemove stuff here
        draw(mouseX, mouseY);
    }

    function calScale() {
        var relativeDist = Math.sqrt((mouseX - startX) * (mouseX - startX) +
            (mouseY - startY) * (mouseY - startY));
        var realDist = parseInt(relativeDist * imageNaturalWidth / imageNaturalWidth);
        console.log('realDist', realDist);
    }

    function getElementSize(elementId) {
        var element = document.getElementById(elementId);
        var boundingBox = element.getBoundingClientRect();
        var elementWidth = boundingBox.right - boundingBox.left;
        var elementHeight = boundingBox.bottom - boundingBox.top;
        return {width: elementWidth, height: elementHeight};
    }


    function setCanvasWrapperSize() {

        // var boundingBox = canvasWrapper.getBoundingClientRect();
        // var canvasWrapperColWidth = boundingBox.right -boundingBox.left;
        canvasWrapperSize = getElementSize('canvas-wrapper');
        var canvasWrapperHeight = Math.floor(imageHeight * canvasWrapperSize.width / imageWidth) + 1;
        canvasWrapper.style.height = canvasWrapperHeight.toString() + 'px';

    }
}