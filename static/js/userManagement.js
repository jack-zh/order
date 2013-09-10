var userManagement={
	init:function(){
		$.getJSON('super/areaInfo',function(data){
			$(".alert").alert();
			
			userManagement.areaInfo=data;
			userManagement.loadUser();
			
			$('#editUserBtn').click(function(){	
				userManagement.addOptions();
			});
			
			$('#saveModify').click(userManagement.onSaveModifyBtnClick);
			
			$('#createUserModalBtn').click(userManagement.onCreateUserModalBtnClick);
			
			$('#editUserModalBtn').click(userManagement.onEditUserModalBtnClick);
			$('#deleteUserModalBtn').click(userManagement.onDeleteUserModalBtnClick);
			
			$('.closeModalBtn').click(function(){
				$('#createUserModal').modal('hide');
				$('#editUserModal').modal('hide');
			});
		})
	},
	loadUser:function(){
		$.getJSON('super/userInfo',function(data){
			var i=0,
				active=false;
			for(i;i<data.length;i++){
				var liTag=document.createElement('li'),
					aTag=document.createElement('a');
				$(aTag).attr('data-toggle','pill');
				$(aTag).attr('href','#'+data[i].username);
				$(aTag).text(data[i].username);
				$(liTag).append(aTag);
				$('ul').append(liTag);
				if(i==0){
					$(liTag).addClass('active');
					active=true;
					userManagement.currentModify=data[i].username;
				}else{
					active=false;
				}
				userManagement.loadArea(data[i].username,active);
				userManagement.loadUserArea(data[i].username);
			}
			$('tr').click(userManagement.onTrClick);
			$('li').click(userManagement.onLiClick);
		})
	},
	loadArea:function(id,active){
		/*
		<div class="tab-content">
			<div class="tab-pane" id="user3">      
				<table class="table table-bordered table-hover">
					<tr class="error"><td>防区1 </td></tr>
					<tr class="success"><td>防区4 <i class="icon-ok"></i> </td></tr>
				</table>    
			</div>
		</div>
		*/
		var divTag=document.createElement('div'),
			i=0,
			area=userManagement.areaInfo,
			tableTag=document.createElement('table');
		$(divTag).addClass('tab-pane');
		if(active){
			$(divTag).addClass('active');
		}
		$(divTag).attr('id',id);
		$(tableTag).addClass('table table-bordered table-hover');
		$(divTag).append(tableTag);
		for(i;i<area.length;i++){
			var trTag=document.createElement('tr'),
				tdTag=document.createElement('td');
			$(trTag).attr('id',id+','+area[i].areanum);
			$(trTag).addClass('error');
			$(tdTag).text(area[i].areaname);
			$(trTag).append(tdTag);
			$(tableTag).append(trTag);
		}
		$('.tab-content').append(divTag);
	},
	loadUserArea:function(user){
		$.getJSON('super/userAreaInfo',{'user':user},function(data){
			var i=0,
				trTags=$('#'+user).children('table').children().children('tr');
			for(i;i<data.length;i++){
				for(var j=0;j<trTags.length;j++){
					if(trTags[j].id==(data[i].username+','+data[i].areanum)){
						$(trTags[j]).click();
					}
				}
			}
		})
	},
	onTrClick:function(){
		if($(this).hasClass('success')){
			$(this).removeClass('success');
			$(this).addClass('error');
			$(this).children('td').children('i').remove();
		}else{
			$(this).removeClass('error');
			$(this).addClass('success');
			$(this).children('td').append('<i class="icon-ok"></i>')
		}
	},
	onLiClick:function(){
		var i=0,
			user=$(this).children('a').text(),
			trTags=$('#'+user).children('table').children().children('tr');
		userManagement.currentModify=user;
		for(i;i<trTags.length;i++){
			var trTag=$($(trTags)[i]);
			if(trTag.hasClass('success')){
				trTag.click();
			}
		}
		userManagement.loadUserArea(user);
	},
	onCreateBtnClick:function(){
		$('#createUserModal').modal({
			backdrop:true,    
			keyboard:true,    
			show:true
		});
	},
	onSaveModifyBtnClick:function(){
		if($(this).hasClass('disabled')) return;
		$(this).addClass('disabled');
		$(this).text('处理中…');
		var i=0,
			area='',
			divTag=$('.tab-pane.active')[0],
			trTags=$(divTag).children().children().children('tr'),
			user=divTag.id;
			
		for(i;i<trTags.length;i++){
			var trTag=trTags[i];
			if($(trTag).hasClass('success')){
				var userarea=trTag.id.split(','),
					areanum=userarea[1];
				if(!area){
					area=areanum.toString();
				}else{
					area+=':::;;;'+areanum;
				}
			}
		}
		$.post('super/userAreaInfo',{'data':area,'user':user},function(data){
			if(data=='Success'){
				$('#ModifyInfo').fadeIn(750).delay(2000).fadeOut(750);
				$('#saveModify').removeClass('disabled');
				$('#saveModify').text('');
				$('#saveModify').append('<i class="icon-hdd"></i>');
				$('#saveModify').append('保存修改');
			}
		});
	},
	onCreateUserModalBtnClick:function(){
		var name=document.getElementById('createName').value,
			data='';
			password=document.getElementById('createPassword').value,
			confirm=document.getElementById('createConfirm').value;
		$('#passworderror').hide();
		$('#passwordempty').hide();
		$('#usernameerror').hide();
		if(!name){
			$('#usernameerror').show();
			return;
		}
		if(!password){
			$('#passwordempty').show();
			return;
		}
		if(password!=confirm){
			$('#passworderror').show();
			return;
		}
		data=name+':::;;;'+password;
		$.post('super/userInfo',{'action':'addUser','data':data},function(data){
			if(data=='Success'){
				document.getElementById('createName').value='';
				document.getElementById('createPassword').value='';
				document.getElementById('createConfirm').value='';
				$('ul').empty();
				$('.tab-content').empty();
				userManagement.loadUser();
				$('#createUserModal').modal('hide');
			}else if(data=='Failure'){
				$('#usernameerror').show();
			}
		});
	},
	addOptions:function(){
		var i=0,
			text='',
			liTags = $('li');
		$('#editName').empty();
		for(i;i<liTags.length;i++){
			text=$(liTags[i]).children().text();
			var optionTag=document.createElement('option');
			$(optionTag).text(text);
			$('#editName').append(optionTag);
			if($(liTags[i]).hasClass('active')){
				document.getElementById('editName').options[i].selected = true;
			}
		}
	},
	onEditUserModalBtnClick:function(){
		var user=document.getElementById('editName').value,
			newPassword=document.getElementById('editPassword').value,
			passwordConfirm=document.getElementById('eidtConfirm').value;
		$('#modifypasswordempty').hide();
		$('#modifypassworderror').hide();
		if(!newPassword){
			$('#modifypasswordempty').show();
			return;
		}
		if(newPassword!=passwordConfirm){
			$('#modifypassworderror').show();
			return;
		}
		$.post('super/userInfo',{'action':'modifyUser','user':user,'newpassword':newPassword},function(data){
			if(data=='Success'){
				$('#ModifyPasswordInfo').fadeIn(750).delay(2000).fadeOut(750);
				document.getElementById('editPassword').value='';
				document.getElementById('eidtConfirm').value='';
			}
		})
	},
	onDeleteUserModalBtnClick:function(){
		var user=document.getElementById('editName').value;
		$.post('super/userInfo',{'action':'deleteUser','user':user},function(data){
			if(data=='Success'){
				$('ul').empty();
				$('.tab-content').empty();
				userManagement.loadUser();
				$('#editUserModal').modal('hide');
			}
		})
	}
}