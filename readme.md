Qcloud
======

### 1.术语规范
+ QS  云端软件分发服务器
+ WS  webservice端软件
+ QC  客户端显示软件

### 2.项目的主要组成部分
+ 推送的webservice模块
+ 云端软件分发服务器
+ 客户端显示

### 3.WS与QS通信协议 
#### 第一部分： “GET”协议
说明：GET协议主要用于推送基本信息报文和心跳
##### 协议json规范：
1：WS -> QS

    {
         "wsc": 0, 
         "aid": 2
    }
  注：

  + wsc为0，心跳包
  + wsc为1，初始化数据包
  + aid，区域编号

2：QS -> WS

    {
         "qsc": 1, 
    }
  注：

  + qsc为0，成功
  + qsc为1，失败

3：WS -> QS 
    
    {
         "wsc": 1, 
         "aid": 2,
         "data": {
              "pas":  [
                 {
                    "gno": "2-1-1",
                    "name": "房门左侧",
                    "desc": "房门左侧的厨房",
                    "enable": true,
                    "status": 2,
                    "sct": 1329724898
                },
                {
                    "gno": "2-1-2",
                    "name": "房门右侧",
                    "desc": "房门右侧的厕所",
                    "enable": true,
                    "status": 2,
                    "sct": 1329724899
                },        
                ...
             ]
         }
    }
  注：

  + gno：全局唯一标识，为“区域-DC_ID-PA_ID”
  + name：防区名称
  + desc：防区备注
  + enable：开关状态
  + status：防区状态
    - 0：禁用
    - 1：断开
    - 2：运行
    - 3：预警
    - 4：告警
    - 5：断纤
    - 6：爆破
    - 7：拆盖
    - 8：机盖正常
    - 9：风雨
    - 10：启动
  + sct：状态变化时间 status change time

#### 第二部分：“POST”协议
说明：GET协议主要用于推送基本信息报文和心跳
##### 协议json规范：
1：发送状态数据 WS -> QS

    {
      "gno": "2-2-1",
      "status": 2,
      "sct": 1329724898
    }
  注：

  + gno：全局唯一标识
  + status：状态码
  + sct：状态发生时间

2：返回码 QS -> WS

    {
         "qsc": 1
    }
  注：

  + qsc为0，成功
  + qsc为1，失败

## **暂时不支持QS发报文修改WS的服务**
