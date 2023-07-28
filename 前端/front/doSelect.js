export default function doSelect() {
  axios.get("http://localhost/MVC/rpi/backend/index.php?action=getValues")
    .then(res=>{
      let response = res.data;
      var datetime=[];
      var buzzer=[];
      var temperature=[];
      var gas=[];
      var fire=[];
      var water_Ao=[];
      
      for(let i=(response['result'].length-5);i<response['result'].length;i++){
        datetime.push(response['result'][i]['datetime']);
        buzzer.push(response['result'][i]['buzzer']);
        temperature.push(response['result'][i]['temperature']);
        gas.push(response['result'][i]['gas']);
        fire.push(response['result'][i]['fire']);
        water_Ao.push(response['result'][i]['water_Ao']);
      }

      switch (response['status']){
        case 200:
          var content_datetime='更新時間:'+datetime[4];
          var content_buzzer='警報:(近五筆)'+buzzer[4];
          var content_temp='溫度:(近五筆)'+temperature;
          var content_gas='瓦斯:(近五筆)'+gas;
          var content_fire='火警:(近五筆)'+fire;

          var content_water_Ao='降水量:(近五筆)'+water_Ao;
          
      }
      $("#datetime").html(content_datetime);
      $("#buzzer").html(content_buzzer)
      console.log(datetime[4]);
      console.log(response);
      $("#temperature").html(content_temp);
      var chart_temp=$("#tempChart");
      var tempChart=new Chart(chart_temp, {
        type: 'line',
        data: {
          labels: datetime,
          datasets: [{
            label: '氣溫(攝氏)',
            data: temperature,
            //圖表背景色
            backgroundColor: [
              'rgba(125, 206, 86, 0.2)',
            ],
            //圖表外框線色
            borderColor: [
              'rgba(125, 206, 86, 1)',
            ],
            //外框線寬度
            borderWidth: 3
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                responsive: true //符合響應式
              }
            }]
          }
        }
      });

      $("#gas").html(content_gas);
      var chart_gas=$("#gasChart");
      var gasChart=new Chart(chart_gas, {
        type: 'line',
        data: {
          labels: datetime,
          datasets: [{
            label: '可燃氣體(ppmm)',
            data: gas,
            //圖表背景色
            backgroundColor: [
              'rgba(125, 100, 86, 0.2)',
            ],
            //圖表外框線色
            borderColor: [
              'rgba(125, 100, 86, 1)',
            ],
            //外框線寬度
            borderWidth: 3
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                responsive: true //符合響應式
              }
            }]
          }
        }
      });

      $("#fire").html(content_fire);
      var chart_fire=$("#fireChart");
      var fireChart=new Chart(chart_fire, {
        type: 'line',
        data: {
          labels: datetime,
          datasets: [{
            label: '火(0:無, 1:有)',
            data: fire,
            stepped: true,
            //圖表背景色
            backgroundColor: [
              'rgba(255, 159, 64, 0.2)',
            ],
            //圖表外框線色
            borderColor: [
              'rgba(255, 159, 64, 1)',
            ],
            //外框線寬度
            borderWidth: 3
          }]
        },
        options: {
          responsive: true,
          interaction: {
            intersect: false,
            axis: 'x'
          },
        }
      });

      $("#water").html(content_water_Ao);
      var chart_gas=$("#waterChart");
      var waterChart=new Chart(chart_gas, {
        type: 'line',
        data: {
          labels: datetime,
          datasets: [{
            label: '降水量(%)',
            data: water_Ao,
            //圖表背景色
            backgroundColor: [
              'rgba(75, 192, 192, 0.2)',
            ],
            //圖表外框線色
            borderColor: [
              'rgba(75, 192, 192, 1)',
            ],
            //外框線寬度
            borderWidth: 3
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                responsive: true //符合響應式
              }
            }]
          }
        }
      });


    })
}







//axios回傳為JSON物件,可取值[],但物件不可顯示,如需顯示必須JSON.stringify()將JSON物件轉換為JSON字串才可顯示
//ajax回傳為JSON字串,不可取值[],但字串可顯示,如需取值必須先JSON.parse()將JSON字串轉為JSON物件

/*
  $.ajax({
    type:"GET",
    url:"http://localhost/MVC/rpi/backend/index.php?action=getValues",

    success:function(response){
      /*switch(response['status']){
        case 200:
          let content='<h4>'+response['result']['temperature']+'</h4>';
          const rows=response['result'];
          /*rows.forEach(element=>{
            content+=element['temperature'];
          });
          content+=;
          $("#temperature").html(response);
        }
        $("#temperature").html(response);
    },
    error:function(err){
      $("#temperature").html("Error:"+err);
    }
  })
}*/