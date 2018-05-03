const sendData = canvas => () => {
  const requestHeaers = new Headers({
    'Content-Type': 'application/json; charset=utf-8', 
  });

  fetch('/knn', {
    method: 'POST',
    headers: requestHeaers,
    body: JSON.stringify({ 'image': canvas.toDataURL() })
  })
  .then(response => response.json())
  .then(console.log)
  // .then(alert(text));
};

const contentLoaded = () => {
    let 
        isDrawing = false,
        points = [];

    const canvas = document.getElementById('canvas');
    const clearCanvasButton = document.getElementById('clear-canvas');
    const sendButton = document.getElementById('send');

    const ctx = canvas.getContext('2d');
    
    sendButton.addEventListener('click', sendData(ctx.canvas));

    clearCanvasButton.onclick = function(e) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        points = [];
    }
    
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
    ctx.lineWidth = 30;
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
