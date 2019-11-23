var data=document.getElementById("data").value;
        data=data.split(" ");
        window.onload = function () {
            var c1 = document.getElementById("c1");
            var context1 = c1.getContext("2d");
            var c2 = document.getElementById("c2");
            var context2 = c2.getContext("2d");
            var img = document.getElementById("img");
            var btn = document.getElementById("btn");
            var xli = 600/img.naturalWidth;
            var yli = 600/img.naturalHeight;
            context1.drawImage(img, 0, 0,600,600);
            context2.font = ("20px Arial");
            for (var i = 0; i < data.length; i=i+5) {
                context2.fillText(data[i], data[i+1]*xli, data[i+4]*yli);
            }

            c2.onclick = function (evt) {
                var x = evt.pageX - $('#c2').offset().left;
                var y = evt.pageY - $('#c2').offset().top;
                //alert(x + "," + y);
                for (var t = 0; t < data.length; t=t+5) {
                    if (x < data[t+1]*xli + 10 && x > data[t+1]*xli - 10 && y < data[t+4]*yli + 10 && y > data[t+4]*yli - 10) {
                        var change;
                        change = prompt("您正在修改" + data[t]);
                        if (change != null)
                            data[t] = change;
                        context2.clearRect(data[t+1]*xli - 10, data[t+4]*yli - 10, 20, 20);
                        context2.fillText(data[t], data[t+1]*xli, data[t+4]*yli);
                    }
                }
            }

            btn.onclick = function () {
                var text = '';
                for (var t = 0; t < data.length; t=t+5) {
                    text = text + data[t];
                }
                download(text, "dlText.txt", "text/plain");
            }
        }