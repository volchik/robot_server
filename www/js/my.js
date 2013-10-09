function logout()
{
        /**** NEW CODE */
        try {
                $.ajax({
                        url: '/',
                        username: 'reset',
                        password: 'reset',
                        statusCode: { 401: function() {} }
                });
        } catch (exception) {
                document.execCommand("ClearAuthenticationCache");
        }
        /**** END NEW CODE */
        return false;
}

function send(data)
{
       $.ajax({
                type: "POST",
                url: "/",
                data: "action="+data,
                success: function(html) {
                        $("#result").empty();
                        $("#result").append("Последняя комманда: <b>"+html+"</b>");
                }
        });
}

function keyEvent()
{
  status='Unicode= '+event.keyCode+' Символ='+String.fromCharCode(event.keyCode);
  switch (event.keyCode) //Анализ Unicode клавиш
  {
        case 37: {send("mot-left"); break} // "Стрелка влево"
        case 40: {send("mot-rev"); break}  // "Стрелка вниз"
        case 39: {send("mot-right"); break} // "Стрелка вправо"
        case 38: {send("mot-fwd"); break}  // "Стрелка вверх"
        default: switch (String.fromCharCode(event.keyCode)) //Анализ клавиши
                 {
                      case 'W': {send("cam-up"); break}   //Камера вверх
                      case 'Z': {send("cam-down"); break} //Камера вниз
                      case 'A': {send("cam-left"); break} //Камера влево
                      case 'S': {send("cam-right"); break} //Камера вправо
                      default: {send(String.fromCharCode(event.keyCode)); break}
                 }
  }
  $("#key").empty();
  $("#key").append(status);
}
var g_nIndex = 0;
function OnBtnRefresh()
{
        document.getElementById("imgDisplay").src = "/?action=jpeg&_="+g_nIndex;
        g_nIndex = g_nIndex + 1;
}

function OnImgLoad()
{
        setTimeout("OnBtnRefresh()",50);
}

function SetResolution(r)
{
       if (r == null) r = document.getElementById("resolution").value
       $.ajax({
                type: "POST",
                url: "/",
                data: "resolution="+r,
                success: function(html) {
                }
        });
}

var isLightOn = 0;
function LightOn()
{
  if (isLightOn)
  {
    document.getElementById("imgLight").src = "img/light-off.png";
    send("light-off");
  }
  else
  {
    document.getElementById("imgLight").src = "img/light-on.png";
    send("light-on");
  }
  isLightOn = 1-isLightOn;
}


function ShowTemperature()
{
        $.ajax({
                type: "GET",
                url: "/",
                data: "action=temperature",
                cache: false,
                success: function(html){
                        $("#temperature").empty();
                        $("#temperature").append("Температура: <b>"+html+"</b> грудусов Цельсия");
                }
        });
}

function ShowPressure()
{
        $.ajax({
                type: "GET",
                url: "/",
                data: "action=pressure",
                cache: false,
                success: function(html){
                        $("#pressure").empty();
                        $("#pressure").append("Давление: <b>"+html+"</b> мм. рт. ст.");
                }
        });
}

function Show()
{
        ShowTemperature();
        ShowPressure();
}

$(document).ready(function(){
        Show();
        setInterval('Show()',10000);
});

