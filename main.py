from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
<meta name="google-signin-client_id" content="493338842790-aune1juv34ikdrounspkev6m5egqdnum.apps.googleusercontent.com">
<script src="https://apis.google.com/js/platform.js" async defer></script>
         <style>
.mytext{
    border:0;padding:10px;background:whitesmoke;
}
.text{
    width:75%;display:flex;flex-direction:column;
}
.text > p:first-of-type{
    width:100%;margin-top:0;margin-bottom:auto;line-height: 13px;font-size: 12px;
}
.text > p:last-of-type{
    width:100%;text-align:right;color:silver;margin-bottom:-7px;margin-top:auto;
}
.text-l{
    float:left;padding-right:10px;
}        
.text-r{
    float:right;padding-left:10px;
}
.avatar{
    display:flex;
    justify-content:center;
    align-items:center;
    width:25%;
    float:left;
    padding-right:10px;
}
.macro{
    margin-top:5px;width:85%;border-radius:5px;padding:5px;display:flex;
}
.msj-rta{
    float:right;background:whitesmoke;
}
.msj{
    float:left;background:white;
}
.frame{
    background:#e0e0de;
    height:450px;
    overflow:hidden;
    padding:0;
}
.frame > div:last-of-type{
    position:absolute;bottom:0;width:100%;display:flex;
}
body > div > div > div:nth-child(2) > span{
    background: whitesmoke;padding: 10px;font-size: 21px;border-radius: 50%;
}
body > div > div > div.msj-rta.macro{
    margin:auto;margin-left:1%;
}
ul {
    width:100%;
    list-style-type: none;
    padding:18px;
    position:absolute;
    bottom:47px;
    display:flex;
    flex-direction: column;
    top:0;
    overflow-y:scroll;
}
.msj:before{
    width: 0;
    height: 0;
    content:"";
    top:-5px;
    left:-14px;
    position:relative;
    border-style: solid;
    border-width: 0 13px 13px 0;
    border-color: transparent #ffffff transparent transparent;            
}
.msj-rta:after{
    width: 0;
    height: 0;
    content:"";
    top:-5px;
    left:14px;
    position:relative;
    border-style: solid;
    border-width: 13px 13px 0 0;
    border-color: whitesmoke transparent transparent transparent;           
}  
input:focus{
    outline: none;
}        
::-webkit-input-placeholder { /* Chrome/Opera/Safari */
    color: #d4d4d4;
}
::-moz-placeholder { /* Firefox 19+ */
    color: #d4d4d4;
}
:-ms-input-placeholder { /* IE 10+ */
    color: #d4d4d4;
}
:-moz-placeholder { /* Firefox 18- */
    color: #d4d4d4;
}
body {
  margin: 0;
  background: url('https://i.pinimg.com/originals/61/76/18/61761851ceffa255b4131517c0681929.gif') no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  background-size: cover;
  color: #0a0a0b;
  overflow: hidden;
}  
</style>
    </head>
    <body>
        <h1 style="font-family: 'VT323', monospace; position:absolute;top:0px;right:25%;left:50%;margin-left:-130px;font-size: 45px; color:aquamarine">Sunset City Chat</h1>
        <h2 style="font-family: 'VT323', monospace; position:absolute;top:40px;right:25%;left:50%;margin-left:-155px;font-size: 40px; color:aquamarine">Your Username: <span id="ws-id"></span></h2>
        <h3 style="font-family: 'VT323', monospace; position:absolute;top:70px;right:25%;left:50%;margin-left:-180px;font-size: 45px; color:aquamarine">Enjoy your stay here....</h3>
        <form style="font-family: 'VT323', monospace; position:absolute;top:140px;right:25%;left:50%;margin-left:-140px;" action="" onsubmit="sendMessage(event)">
            <input style="width:269px;" placeholder="Enter you message here...." type="text" id="messageText" autocomplete="off"/>
            <button style="font-family: 'VT323', monospace;"id="btsubmit" disabled>Send</button>
        </form>
        <div class="g-signin2" style="position:absolute;top:0;right:0;" data-onsuccess="onSignIn"></div>
       <div class="col-sm-3 col-sm-offset-4 frame" style="position:absolute;top:170px;right:25%;left:50%;margin-left:-140px;
  background: url('https://64.media.tumblr.com/313f7d09ead1e10c2424152c96913831/tumblr_phtp88GfqM1rnbw6mo1_1280.gifv') no-repeat center center fixed;
  background-size: contain;
  color: #0a0a0b;
  overflow: hidden;">
            <ul></ul>
            
                
        </div>    
        <script>
        function onSignIn(googleUser) {
  var bt = document.getElementById("btsubmit");
  bt.disabled = false;
  }

	var me = {};
me.avatar = "https://purepng.com/public/uploads/large/purepng.com-ninjashinobininjacovert-agentassassinationguerrilla-warfaresamuraiclip-artblack-ninja-14215269606870qvcf.png";

var you = {};
you.avatar = "https://purepng.com/public/uploads/large/purepng.com-ninjashinobininjacovert-agentassassinationguerrilla-warfaresamuraiclip-artblack-ninja-14215269606870qvcf.png"
function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                        '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /></div>' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+you.avatar+'" /></div>' +                                
                  '</li>';
    }
    setTimeout(
        function(){                        
            $("ul").append(control).scrollTop($("ul").prop('scrollHeight'));
        }, time);
    
}

function resetChat(){
    $("ul").empty();
}
            function getQueryString() {
            var result = {}, queryString = location.search.slice(1),
                re = /([^&=]+)=([^&]*)/g, m;

                while (m = re.exec(queryString)) {
                result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
             }

            return result;
            }
            
            var client_id = getQueryString()["client_id"];
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            
           
            
            ws.onmessage = function(event) {
                
                insertChat("me",event.data)
               
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
	            insertChat("you",input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

html2 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My chat room</title>
    <meta name="google-signin-client_id" content="493338842790-aune1juv34ikdrounspkev6m5egqdnum.apps.googleusercontent.com">
<script src="https://apis.google.com/js/platform.js" async defer></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
<style>
body {
  margin: 0;
  background: url('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/12cbe8a4-f55c-4b40-85bb-d8e1405e7b84/d98qb8z-56df9d2f-1a24-41d4-ad7d-e4244cc189be.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzEyY2JlOGE0LWY1NWMtNGI0MC04NWJiLWQ4ZTE0MDVlN2I4NFwvZDk4cWI4ei01NmRmOWQyZi0xYTI0LTQxZDQtYWQ3ZC1lNDI0NGNjMTg5YmUuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Nd7Pghx-n6PtcGxt3q1iXKcSmh0AlSH0jkMzXViaWqE') no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  background-size: cover;
  color: #0a0a0b;
  overflow: hidden;
}
</style>
</head>
<body>
    <h1 style="position:absolute;top:80px;right:25%;left:50%;margin-left:-95px; font-family: 'VT323', monospace; font-size: 35px;"><b>Sunset City Chat</b></h1>
    <form style="position:absolute;top:170px;right:25%;left:50%;margin-left:-120px;" action="/chat" method="get">
         <div>
            <label style="font-family: 'VT323', monospace; font-size: 20px;">Enter Username:</label>
            <input type="text" name="client_id">
        </div>
        <button style="font-family: 'VT323', monospace; font-size: 20px;" type="submit" id="btsubmit" disabled>send</button>
    </form>
<div class="g-signin2" style="position:absolute;bottom:0px;right:25%;left:50%;margin-left:-60px;" data-onsuccess="onSignIn"></div>
</body>
<script>
function onSignIn(googleUser) {
  var bt = document.getElementById("btsubmit");
  bt.disabled = false;
  }

</script>
</html>
'''

html3="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <meta name="google-signin-client_id" content="493338842790-aune1juv34ikdrounspkev6m5egqdnum.apps.googleusercontent.com">
<script src="https://apis.google.com/js/platform.js" async defer></script>
    <style>
        @import url('https://fonts.googleapis.com/css?family=Lato:400,700');

*, *:before, *:after {
  -webkit-box-sizing: inherit;
  -moz-box-sizing: inherit;
  box-sizing: inherit;
}

::-webkit-input-placeholder {
  color: #56585b;
}

::-moz-placeholder {
  color: #56585b;
}

:-moz-placeholder {
  color: #56585b;
}

html {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

body {
  font-family: 'Lato', sans-serif;
  margin: 0;
  background: url('https://cutewallpaper.org/21/pixel-art-background-1920x1080/8-Bit-City-Background-1920x1080-Drkenfreedmanblog.xyz.gif') no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  background-size: cover;
  color: #0a0a0b;
  overflow: hidden;
}

ul, nav{
  list-style: none;
  padding: 0;
}

a {
  color: #fff;
  text-decoration: none;
  cursor: pointer;
  opacity: 0.9;
}

a:hover {
  opacity: 1;
}

h1 {
  font-size: 3rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 1.5rem;
}

i {
  font-size: 1.3rem;
}

header {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
  padding: 10px 100px 0;
}

header nav ul {
  display: flex;
}

header nav li{
  margin: 0 15px;
}

header nav li:first-child{
  margin-left: 0;
}

header nav li:last-child{
  margin-right: 0;
}

a.btn {
  color: #fff;
  padding: 10px;
  border: 1px solid rgba(255,255,255,0.5);
  -webkit-transition: all 0.2s;
  -moz-transition: all 0.2s;
  transition: all 0.2s;
}

a.btn:hover {
  background: #d73851;
  border: 1px solid #d73851;
  color: #fff;
}

.cover  {
  height: 100vh;
  width: 100%;
  background: -webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,0.05)), to(rgba(0,0,0,0)));
  background: -webkit-linear-gradient(top, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0) 100%);
  background: linear-gradient(to bottom, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0) 100%);
  padding: 20px 50px;
  display: -webkit-box;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  flex-direction: column;
  -webkit-box-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  align-items: center;
}

.flex-form input[type="submit"] {
  background: #ef3f5a;
  border: 1px solid #ef3f5a;
  color: #fff;
  padding: 0 30px;
  cursor: pointer;
  -webkit-transition: all 0.2s;
  -moz-transition: all 0.2s;
  transition: all 0.2s;
}

.flex-form input[type="submit"]:hover {
  background: #d73851;
  border: 1px solid #d73851;
}

.flex-form {
  display: -webkit-box;
  display: flex;
  z-index: 10;
  position: relative;
  width: 500px;
  box-shadow: 4px 8px 16px rgba(0, 0, 0, 0.3);
}

.flex-form > * {
  border: 0;
  padding: 0 0 0 10px;
  background: #fff;
  line-height: 50px;
  font-size: 1rem;
  border-radius: 0;
  outline: 0;
  -webkit-appearance: none;
}

input[type="search"] {
  flex-basis: 500px;
}

#madeby {
  position: absolute;
  bottom: 0;
  right: 0;
  padding: 25px 100px;
  color: #fff;
}

@media all and (max-width:800px) {
  body {
    font-size: 0.9rem;
  }

  .flex-form {
    width: 100%;
  }

  input[type="search"] {
    flex-basis: 100%;
  }

  .flex-form > * {
    font-size: 0.9rem;
  }

  header {
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column;
    padding: 10px !important;
  }

  header h2 {
    margin-bottom: 15px;
  }

  h1 {
    font-size: 2rem;
  }

  .cover {
    padding: 20px;
  }

  #madeby {
    padding: 30px 20px;
  }
}

@media all and (max-width:360px) {
  header nav li{
    margin: 0 10px;
  }

  .flex-form {
    display: -webkit-box;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column;
  }

  input[type="search"] {
    flex-basis: 0;
  }

  label {
    display: none;
  }
}
    </style>
</head>
<body>
    <div class="container">

  <header>
    <h2><a href="#"><i></i> </a></h2>

  </header>

  <div class="cover">
    <h1>Sign in with Google to continue</h1>
    <div class="g-signin2" data-onsuccess="onSignin"></div>

  </div>

</div>
</body>
<script>
    function onSignin(googleUser){
    location.replace('/index');
    }
</script>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        pass

    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if connection == websocket:
                continue
            await connection.send_text(message)





manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html3)


@app.get("/index")
async def get():
    return HTMLResponse(html2)

@app.get('/chat')
async def chat(client_id: str):
    if client_id:
        return HTMLResponse(html)
    else:
        return RedirectResponse(html2)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        await manager.broadcast(f"{client_id} has joined the chat...", websocket)
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"<b>{client_id}:</b><br>"
                                    f"{data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} has left the chat...", websocket)



