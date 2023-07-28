export default function startPage() {
  const sp = `
        <h4 id="datetime" style="background-color: blanchedalmond;color: cadetblue;text-align: center;">更新時間:</h4>
        <h4 id="buzzer" style="background-color: red;">警報:</h4>
        <h4 id="temperature" style="background-color: blanchedalmond;color: cadetblue">溫度:(近五筆)</h4>
        <canvas id="tempChart" width="10px" height="5px"></canvas>
        
        <h4 id="gas" style="background-color: blanchedalmond;color: cadetblue">瓦斯:(近五筆)</h4>
        <canvas id="gasChart" width="10px" height="5px"></canvas>
        
        <h4 id="fire" style="background-color: blanchedalmond;color: cadetblue">火警:(近五筆)</h4>
        <canvas id="fireChart" width="10px" height="5px"></canvas>
        
        <h4 id="water" style="background-color: blanchedalmond;color: cadetblue">降水量:(近五筆)</h4>
        <canvas id="waterChart" width="10px" height="5px"></canvas>
    `;
  return sp;
}
