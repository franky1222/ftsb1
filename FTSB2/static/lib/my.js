function CheckUser() {
    var name = document.getElementById('getUserName').value;
    if (name == '') {
		 $(login).submit();
         alert("�����ȵ�¼����ʹ��ϵͳ");
    }
}
CheckUser();