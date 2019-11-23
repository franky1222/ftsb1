var data = document.getElementById("data").value;
data = data.split(" ");
var data1 = document.getElementById("merge").value;

if (data1 == "")
	data1 = data1.split("");
else
	data1 = data1.split(" ");
var line;
window.onload = function () {
    var c1 = document.getElementById("c1");
    var context1 = c1.getContext("2d");
    var c2 = document.getElementById("c2");
    var context2 = c2.getContext("2d");
    var fd = document.getElementById("fd");
    var contextfd = fd.getContext("2d");
    var img = document.getElementById("img");
    var btn = document.getElementById("btn");
    var xli = 600 / img.naturalWidth;
    var yli = 600 / img.naturalHeight;
    context1.drawImage(img, 0, 0, 600, 600);
    //context2.font = ("20px Arial");
	context2.font = ((data[0 + 4] - data[0 + 2]) * xli + "px" + " Arial");		//输出字体大小
    for (var i = 0; i < data.length; i = i + 5) {	
        context2.fillText(data[i], data[i + 1] * xli, data[i + 4] * yli);
    }

    c2.onclick = function (evt) {
        var x = evt.pageX - $('#c2').offset().left;
        var y = evt.pageY - $('#c2').offset().top;
        //alert(x + "," + y);
        //contextfd.clearRect(0,0,fd.width,fd.height);
        // fd.style.left = x+10+'px';
        // fd.style.top = y+10+'px';
        // fd.style.display="block";
        //contextfd.drawImage(img,x/xli,y/yli,50,50,0,0,200,200);
        for (var t = 0; t < data.length; t = t + 5) {
            if (x < data[t + 3] * xli && x > data[t + 1] * xli && y < data[t + 4] * yli && y > data[t + 2] * yli) {
                var change;
                change = prompt("您正在修改" + data[t]);
                if (change != null)
                    data[t] = change;
                context2.clearRect(data[t + 1] * xli + 10, data[t + 2] * yli + 10, (data[t + 3] - data[t + 1]) * xli, (data[t + 4] - data[t + 2]) * yli);
                context2.font = ((data[0 + 3] - data[0 + 1]) * xli + "px" + " Arial");
                context2.fillText(data[t], data[t + 1] * xli, data[t + 4] * yli);
            }
        }
    }
    c2.onmousemove = function (evt) {
        var x = evt.pageX - $('#c2').offset().left;
        var y = evt.pageY - $('#c2').offset().top;
        //alert(x + "," + y);
        contextfd.clearRect(0, 0, fd.width, fd.height);
        fd.style.left = x + 'px';
        fd.style.top = y + 'px';
        fd.style.display = "block";
        contextfd.drawImage(img, x / xli - 20, y / yli - 35, 100, 100, 0, 0, 200, 200);
    }
	btn.onclick = function () {
        $('#li4').css({color: "#1e4fcd"});
        $('#li4-t').css({color: "#1e4fcd"});
        var text = '';
        for (var t = 0; t < data.length; t++) {
            text = text + " " + data[t];

        }
		if (name[0] != '/'){
			var text2 = word_sort(data) ;		//对文字进行排序
			var text1 = '';
			for (var t = 0; t < text2.length; t = t + 5) {
				for (var i = 1; i<line.length-1; i++){
					if (t == (line[i]*5)){
						text1 = text1 + "     ";
					}
				}
				text1 = text1  + text2[t];
			}
			// for (var t = 0; t < text2.length-1; t++) {
				// text1 = text1 + " " + str(text2[t][0]);

			// }
			download(text1, "dlText.txt", "text/plain");
		}else{
			merging();
			if (name[3] == '4'){
				var text2 = word_sort(data1) ;		//对文字进行排序
				var text1 = '';
				for (var t = 0; t < text2.length; t = t + 5) {
					for (var i = 1; i<line.length-1; i++){
						if (t == (line[i]*5)){
							text1 = text1 + "     ";
						}
					}
					text1 = text1  + text2[t];
				}
				download(text1, "dlText.txt", "text/plain");
			}							
		}
		var text3 = data1.join(" ") ;
        var file_path = document.getElementById('ChangeUserName').value + '/' + document.getElementById("ChangePhotoName").value + ".jpg";
        $(fm.h1data).val(file_path);
        $(fm.h2data).val(text);
        $(fm.h3data).val(document.getElementById("ChangePhotoName").value);
		$(fm.h4data).val(text3) ;
        $(fm).submit();
    }

    
}

function merging(){		//将4个分割部分写在一个数组里
	if (name[3] == '1'){
		for (var i=0; i<data.length-1; i=i+5){
			data1.push(data[i]) ;
			data1.push(parseInt(data[i+1])) ;
			data1.push(parseInt(data[i+2])) ;
			data1.push(parseInt(data[i+3])) ;
			data1.push(parseInt(data[i+4])) ;
		}
	}else if(name[3] == '2'){
		for (var i=0; i<data.length-1; i=i+5){
			data1.push(data[i]) ;
			data1.push(parseInt(data[i+1])+500) ;
			data1.push(parseInt(data[i+2])) ;
			data1.push(parseInt(data[i+3])) ;
			data1.push(parseInt(data[i+4])) ;
		}
	}else if(name[3] == '3'){
		for (var i=0; i<data.length-1; i=i+5){
			data1.push(data[i]) ;
			data1.push(parseInt(data[i+1])) ;
			data1.push(parseInt(data[i+2])+500) ;
			data1.push(parseInt(data[i+3])) ;
			data1.push(parseInt(data[i+4])) ;
		}
	}else{
		for (var i=0; i<data.length-1; i=i+5){
			data1.push(data[i]) ;
			data1.push(parseInt(data[i+1])+500) ;
			data1.push(parseInt(data[i+2])+500) ;
			data1.push(parseInt(data[i+3])) ;
			data1.push(parseInt(data[i+4])) ;
		}
	}
	// document.write(data) ;
	// document.write("<br/>");
	// document.write(data1) ;
	// document.write("<br/>");
}

//////////////////////////////////////////////
function word_sort(data0){
	var sort_data = new Array() ;
	for (var i=0; i<data0.length; i=i+5){		//按字存放，二维数组
		data0[i+1] = parseInt(data0[i+1]) ;
		data0[i+2] = parseInt(data0[i+2]) ;
		data0[i+3] = parseInt(data0[i+3]) ;
		data0[i+4] = parseInt(data0[i+4]) ;
		sort_data.push(data0.slice(i,i+5)) ;
	}
	sort_data.sort(function(x, y){		//由大到小排序，按x坐标
	  return y[1] - x[1];
	});
	// var temp = sort_data[0] ;
	// for (var j=1; j<sort_data.length; j++){		//计算一列有几个字,最终j为一列的字数
		// if (temp[1]-sort_data[j][1] > 20)
			// break ;
	// }
	
	var number = [0] ;					//計算每列有多少个字，number用于存储每列首字是第几个字
	for (var i=0; i<sort_data.length; i++){
		var temp = sort_data[i] ;
		for (var j=i+1; j<sort_data.length; j++){
			if (temp[1]-sort_data[j][1]>40)			//若有文字排列出错，可将40改大一些
				break ;
		}
		number.push(j) ;
		i = j ;
	}
	line = [].concat(number) ;
	// document.write(line) ;		//用于查看每个字的坐标，可用来检查错误
	// document.write("<br/>");
	// document.write(number) ;
	// document.write("<br/>");
	for (var j=0; j<number.length-1; j++){		//对每一列进行排序
		var i = number[j] ;
		var tt = sort_data.slice(i,number[j+1]) ;
		tt.sort(function(x, y){		//由小到大排序，按y
		  return x[2] - y[2];
		});
		for (var k=0; k<number[j+1]-i; k++){
			sort_data[i+k] = tt[k] ;
		}								
	}
	sort_data = [].concat.apply([],sort_data) ;		//把数组化为一维数组
	return sort_data ;
}
///////////////////////////////////////////////

/**
 * 显示是第几张切割图片
 * */
var name = document.getElementById('ChangePhotoName').value.slice(-4)
function changebackground(id){
	$('#'+id).css({color: "#f16f20"});
	$('#'+id+'-t').css({color: "#f16f20"});
};
function show() {
    if (name[3] == '1'||name[3] == '2'||name[3] == '3'|| name[3] == '4')
        $('#li_pn').css({display:"block"})
    if (name[3] == '2'){
        changebackground('li6')
    }
    else if (name[3] == '3'){
        changebackground('li6')
        changebackground('li7')
    }
    else if (name[3] == '4'){
        changebackground('li6')
        changebackground('li7')
        changebackground('li8')
    }
}
// show()
if(name[0] == '/')
	show() ;
