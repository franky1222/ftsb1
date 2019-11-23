// document.getElementById('file').onchange = function () {
        // var imgfile = this.files[0];
        // var fr = new FileReader();
        // fr.onload = function () {
            // document.getElementById('img').src = fr.result;
        // };
        // fr.readAsDataURL(imgfile);
		
		// var files = document.getElementById("file").files ;
		// var fs = files.length ;
		// if (fs > 8)
		// {
			// alert("上传的文件数量超过8个了！请重新选择！") ;
			// return false;
		// }
    // };
	// function clearCanvas(){
		// var canvas1 = document.getElementById('canvas1');
        // var context1 = canvas1.getContext("2d");
		// canvas1.height=canvas1.height;  
		// var imgfile = this.files[0];
        // var fr = new FileReader();
		// fr.readAsDataURL(imgfile);
        // fr.onload = function () {
            // document.getElementById('img').src = fr.result;
        // };
	// }
    /*window.onload = function () {
        var canvas1 = document.getElementById('canvas1');
        var context1 = canvas1.getContext("2d");
        var img = document.getElementById('img');
		
        img.onload = function () {				//显示图片大小
            context1.drawImage(img, 0, 0,300,300);
			context1.drawImage(img, 0, 300,600,600);
        };
        canvas1.onclick = function (evt) {
		// context1.clearRect(0, 0,600,600);
         var x = evt.pageX - $('#canvas1').offset().left;
         var y = evt.pageY - $('#canvas1').offset().top;
         context1.moveTo(0,y);
         context1.lineTo(600,y);
         context1.moveTo(x,0);
         context1.lineTo(x,600);
         context1.strokeStyle="red";
         context1.stroke();
         var xli = document.getElementById('img').width/600;
         var yli = document.getElementById('img').height/600;
         document.getElementById('x').value=x*xli;
         document.getElementById('y').value=y*yli;
     }

    };*/
var filesname = "";
function checkPdf()
{
	var fileType = getFileType($('input[name="pdf"]').val());
	if($('input[name="pdf"]').val()==null || $('input[name="pdf"]').val()=='')
	{
	  alert("请上传pdf!");
	   return false;
	}
	else {
	   if("pdf" != fileType)
	   {
		  $('input[name="pdf"]').val("");
			alert("请上传pdf");
			 return false;
		} else {
			return true;
		}
	}
	
 }
 
document.getElementById('pdf_file').onchange = function (){
	pdf_name = document.getElementById("pdf_file").files[0].name ;
	filesname = filesname + pdf_name + ';';
	$(fm2.filesname2).val(filesname) ;
 
}
	 
function checkLength()
{
	var fileType = getFileType($('input[name="photo"]').val());
	if($('input[name="photo"]').val()==null || $('input[name="photo"]').val()=='')
	{
	  alert("请上传图片!");
	   return false;
	}
	else {
		if("jpg" != fileType && "jpeg" != fileType  && "png" != fileType)
		   {
			  $('input[name="photo"]').val("");
				alert("请上传JPG,JPEG,PNG格式的图片");
				 return false;
			}
		else {
				//获取附件大小（单位：KB）
				var fileSize = document.getElementById("file").files[0].size / 1024;
				if(fileSize > 2048)
							{
					alert("图片大小不能超过2MB");
				return false;}
				else
					return true;
		}
    }
}


function getFileType(filePath) {
	var startIndex = filePath.lastIndexOf(".");
	if(startIndex != -1)
		return filePath.substring(startIndex + 1, filePath.length).toLowerCase();
	else return "";
}
		// <!-- function test() -->
		// <!-- { -->
			// <!-- alert("测试") ; -->
		// <!-- } -->
function FileCountCheck()
{
	var files = document.getElementById("file").files ;
	var fs = files.length ;
	if (fs > 2)
	{
		alert("上传的文件数量超过2个了！请重新选择！") ;
		return false;
	}
}
	
	
document.getElementById('file').onchange = function () {		//判断上传的文件数量
	var files = document.getElementById("file").files ;
	var fs = files.length ;
	if (fs > 8)
	{
		alert("上传的文件数量超过8个了！请重新选择！") ;
		return false;
	}
	if (fs == 1){
		document.getElementById("canvas1").style.display = "block" ;
		document.getElementById("dd").style.display = "none" ;
		single_preview() ;
	}else{
		document.getElementById("canvas1").style.display = "none" ;
		document.getElementById("dd").style.display = "block" ;
		mult_preview();
	}	
	$(fm1.filesname).val(filesname) ;
};

function mult_preview(){
	//获取选择图片的对象并获取所有的图片文件
	var img_list = document.getElementById("file").files ;
	//后期显示图片区域的对象
	var dd = document.getElementById("dd");
	dd.innerHTML = "";
	//循环遍历
	for (var i = 0; i < img_list.length; i++) {    
		//动态添加html元素        
		dd.innerHTML += "<div style='float:left;padding:1px;' > <img id='img" + i + "'  /> </div>";
		//获取图片imgi的对象
		var imgObjPreview = document.getElementById("img"+i); 
		
		if (img_list && img_list[i]) {
			imgObjPreview.style.display = 'block';
			imgObjPreview.style.width = '300px';
			imgObjPreview.style.height = '280px';
			//imgObjPreview.src = docObj.files[0].getAsDataURL();
			imgObjPreview.src = window.URL.createObjectURL(img_list[i]);   //获取上传图片文件的物理路径
		}
		filesname = filesname + img_list[i].name + ';';
	}  
	return true;
}

function single_preview(){
	var imgfile = document.getElementById("file").files[0];
	var fr = new FileReader();
	fr.readAsDataURL(imgfile);
	fr.onload = function () {
		document.getElementById('img').src = fr.result;
	};
	filesname = filesname + imgfile.name + ';';
	var canvas1 = document.getElementById('canvas1');
	var context1 = canvas1.getContext("2d");
	var img = document.getElementById('img');
	
	img.onload = function () {				//显示图片大小
		context1.drawImage(img, 0, 0,600,600);
	};
	canvas1.onclick = function (evt) {
	// context1.clearRect(0, 0,600,600);
	 var x = evt.pageX - $('#canvas1').offset().left;
	 var y = evt.pageY - $('#canvas1').offset().top;
	 context1.moveTo(0,y);
	 context1.lineTo(600,y);
	 context1.moveTo(x,0);
	 context1.lineTo(x,600);
	 context1.strokeStyle="red";
	 context1.stroke();
	 var xli = document.getElementById('img').width/600;
	 var yli = document.getElementById('img').height/600;
	 document.getElementById('x').value=x*xli;
	 document.getElementById('y').value=y*yli;
 }
}