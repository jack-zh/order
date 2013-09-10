var login={
	init:function(){
		$('.btn-primary').click(login.doLogin);
	},
	doLogin:function(e){
		var user=document.getElementById('inputUser').value,
			password=document.getElementById('inputPassword').value;
		e.preventDefault();
		$('.errorInfo').hide();
		if(!user&&!password){
			$('.errorInfo').show();
			return;
		}
		$.post('login',{'user':user,'password':password},function(data){
			if(data=='error'){
				$('.errorInfo').show();
			}else if(data=='Administrator'){
				location.href='/super';
			}else{
				location.href='/areastatus';
			}
		})
		
	}
}