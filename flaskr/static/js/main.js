const contentLoaded = () => {
    let 
        isDrawing = false,
        points = [];

    const canvas = document.getElementById('canvas');
    const clearCanvasButton = document.getElementById('clear-canvas');

    clearCanvasButton.onclick = function(e) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        points = [];
    }
    
    ctx = canvas.getContext('2d');    

    canvas.onmousedown = function(e) {
        isDrawing = true;

        points.push({
            x: e.clientX - this.offsetLeft,
            y: e.clientY - this.offsetTop,
        });

        redraw(ctx, points);        
    };

    canvas.onmousemove = function(e) {
        if (!isDrawing) return;

        points.push({
            x: e.clientX - this.offsetLeft,
            y: e.clientY - this.offsetTop,
            isDraging: true,
        });

        redraw(ctx, points);
    };

    canvas.onmouseup = function() {
        isDrawing = false;
    };
};

const redraw = (ctx, points) => {
    ctx.lineWidth = 10;
    ctx.lineJoin = ctx.lineCap = 'round';

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (var i = 1; i < points.length; i++) {
        if (points[i].isDraging) {
            ctx.lineTo(points[i].x, points[i].y);
        } else {
            ctx.moveTo(points[i].x, points[i].y);
        }
    }

    ctx.stroke();
}

document.addEventListener("DOMContentLoaded", contentLoaded);
