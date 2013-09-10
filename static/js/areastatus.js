areastatus={
	sortOrnot:false,
	sortIndex:'',
	reverse:false,
	pagelimit:25,
	historyData:[],
	init:function(user){
		$('thead tr td').click(areastatus.sortTable);
		$('#pageul>li').click(function(){
			var href=this.firstElementChild.href.split('#')[1],
				headTag=document.getElementById('head'),
				tailTag=document.getElementById('tail'),
				activeNode=document.querySelector('#pageul>li.active');
			if(href!='Prev'&&href!='Next'){
				activeNode.className='';
				this.className='active';
				areastatus.paginationDisplay();
			}else if(href=='Prev'){
				if(activeNode.previousElementSibling===headTag) return;
				activeNode.className='';
				activeNode.previousElementSibling.className='active';
				areastatus.paginationDisplay();
			}else if(href=='Next'){
				console.log(activeNode);
				console.log(activeNode.nextElementSibling);
				if(activeNode.nextElementSibling===tailTag) return;
				activeNode.className='';
				activeNode.nextElementSibling.className='active';
				areastatus.paginationDisplay();
			}
			href=document.querySelector('#pageul>li.active').firstElementChild.href.split('#')[1];
			if(parseInt(href)*areastatus.pagelimit<areastatus.historyData.length){
				areastatus.buildTable('historytable',areastatus.historyData.slice((parseInt(href)-1)*areastatus.pagelimit,parseInt(href)*areastatus.pagelimit-1),false);
			}else{
				areastatus.buildTable('historytable',areastatus.historyData.slice((parseInt(href)-1)*areastatus.pagelimit,-1),false);
			}
		});
		$('a[href=#historyModal]').click(function(){
			$.getJSON('history',{'user':user},function(data){
				var i,
					liTag,
					aTag,
					pagecount=Math.ceil(data.length/areastatus.pagelimit),
					headTag=document.getElementById('head'),
					tailTag=document.getElementById('tail'),
					ul=document.getElementById('pageul');
				$('li[index]').remove();
				for(i=0;i<pagecount;i++){
					liTag=document.createElement('li');
					$(liTag).attr('index',i);
					aTag=document.createElement('a');
					aTag.innerHTML=i+1;
					if(i==0) liTag.className='active';
					aTag.href='#'+(i+1);
					liTag.appendChild(aTag);
					ul.insertBefore(liTag,tailTag);
				}
				areastatus.historyData=data;
				areastatus.paginationDisplay();
				areastatus.buildTable('historytable',areastatus.historyData.slice(0,24),false);
			})
		})
		areastatus.getArea(user);
		if(window.WebSocket){
			var reg=/:\/\/[^\/]+\//g,
				text=location.href,socket;
			text=text.indexOf('http://')==-1?'http://'+text:text;
			text=text.match(reg)[0].replace('://','').replace('/','');
			socket=new WebSocket('ws://'+text+'/websocket_status/');
			socket.onopen=function(e){
				console.log('open');
			}
			socket.onclose=function(e){
				console.log('close');
			}
			socket.onerror=function(e){
				console.log('error');
			}
			socket.onmessage=function(e){
				var obj=JSON.parse(e.data),
					status=obj.status,
					trTag=document.getElementById(obj.gno),
					stc=obj.stc;
				trTag.lastElementChild.innerHTML=stc.slice(1,-2	);
				trTag.lastElementChild.previousElementSibling.innerHTML=areastatus.decodeStatus(trTag,status);
			}
		}else{
			window.setInterval(function(){
				areastatus.getArea(user);
			},5000);
		}
	},
	getArea:function(user){
		$.getJSON('status',{'user':user},function(data){
			areastatus.buildTable('statustable',data,true);
		})
	},
	sortTable:function(){
		var index,
			i,
			table=this.parentNode.parentNode.parentNode,
			tbody=table.children[1],
			trarray=new Array();
			attrList=['防区名','防区编号','区域','描述','状态','获取时间'];
		if(!areastatus.sortOrnot) areastatus.sortOrnot=true;
		for(i in attrList){
			if(this.innerHTML==attrList[i]){
				if(tbody.id='statustable') areastatus.sortIndex=i;
				index=i;
				break;
			}
		}
		for(i=0;i<tbody.childElementCount;i++){
			trarray.push(tbody.children[i]);
		}
		if(tbody.sortColl==index){
			if(tbody.id='statustable') areastatus.reverse=true;
			trarray.reverse();
		}else{
			if(tbody.id='statustable') areastatus.reverse=false;
			trarray.sort(function(tr1,tr2){
				var value1=tr1.children[index].innerHTML,
					value2=tr2.children[index].innerHTML;
				if(value1>value2){
					return 1;
				}else if(value1<value2){
					return -1;
				}else{
					return 0;
				}
			});
		}
		for(i=0;i<trarray.length;i++){
			tbody.appendChild(trarray[i]);
		}
		tbody.sortColl=index;
	},
	decodeStatus:function(trtag,status){
		var cls,statustext;
		switch(status){
			case 0:cls='muted';statustext='禁用';break;
			case 1:cls='muted';statustext='断开';break;
			case 2:cls='success';statustext='运行';break;
			case 3:cls='warning';statustext='预警';break;
			case 4:cls='error';statustext='告警';break;
			case 5:cls='warning';statustext='断纤';break;
			case 6:cls='error';statustext='爆破';break;
			case 7:cls='warning';statustext='拆盖';break;
			case 8:cls='success';statustext='机盖正常';break;
			case 9:cls='';statustext='风雨';break;
			case 10:cls='';statustext='启动';break;
		}
		if(cls) trtag.className=cls;
		return statustext;
	},
	buildTable:function(tableId,data,sortornot){
		var i,obj,trtag,nametag,gnotag,numtag,descstag,statustag,timetag,
				table=document.getElementById(tableId);
		$(table).children().remove();
		for(i in data){
			obj = data[i];
			trtag = document.createElement('tr');
			trtag.id=obj['gno'];
			//防区名
			nametag = document.createElement('td');
			nametag.innerHTML=obj['name'];
			//防区编号
			gnotag = document.createElement('td');
			gnotag.innerHTML=obj['gno'];
			//区域
			numtag = document.createElement('td');
			numtag.innerHTML=obj['areanum'];
			//描述
			descstag = document.createElement('td');
			descstag.innerHTML=obj['descs'];
			//状态
			statustag = document.createElement('td');
			statustag.innerHTML=areastatus.decodeStatus(trtag,obj['status']);
			//时间
			timetag = document.createElement('td');
			timetag.innerHTML=obj['stc'];
			
			trtag.appendChild(nametag);
			trtag.appendChild(gnotag);
			trtag.appendChild(numtag);
			trtag.appendChild(descstag);
			trtag.appendChild(statustag);
			trtag.appendChild(timetag);
			table.appendChild(trtag);
		}
		if(sortornot&&areastatus.sortOrnot){
			table.sortColl='';
			var thTag=table.previousElementSibling.firstElementChild.children[areastatus.sortIndex];
			console.log(thTag);
			if(areastatus.reverse) $(thTag).click();
			$(thTag).click();
		}	
	},
	paginationDisplay:function(){
		var headTag=document.getElementById('head'),
			tailTag=document.getElementById('tail'),
			activeNode=document.querySelector('#pageul>li.active');
		$('#pageul>li').hide();$(tailTag).show();$(headTag).show();
		$(activeNode).show();
		if(activeNode.previousElementSibling.previousElementSibling){
			$(activeNode.previousElementSibling.previousElementSibling).show();
		}
		if(activeNode.previousElementSibling){
			$(activeNode.previousElementSibling).show();
		}
		if(activeNode.nextElementSibling){
			$(activeNode.nextElementSibling).show();
		}
		if(activeNode.nextElementSibling.nextElementSibling){
			$(activeNode.nextElementSibling.nextElementSibling).show();
		}
	}
}