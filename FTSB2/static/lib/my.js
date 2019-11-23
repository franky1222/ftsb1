function CheckUser() {
    var name = document.getElementById('getUserName').value;
    if (name == '') {
		 $(login).submit();
         alert("请您先登录，再使用系统");
    }
}
CheckUser();