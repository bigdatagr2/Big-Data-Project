        function startTime() {
            var xt = setInterval(xtimer, 1000);
            var xt3 = setInterval(bibi, 1000);
        }
        
        function bibi() {
            var xdate = new Date();
            document.getElementById('start_x').innerHTML = "++++" + xdate;
            document.getElementById('debug_x').innerHTML = "debug time " + xdate;
        }

        function xtimer() {
            var today = new Date();
            var h = today.getHours();
            var m = today.getMinutes();
            var s = today.getSeconds();
            var x = "from jsondata .. {{ data }}";
            m = checkTime(m);
            s = checkTime(s);
            document.getElementById('horloge').innerHTML =
            h + ":" + m + ":" + s;
            document.getElementById('idmsg').innerHTML = "<strong>Message from timer : </strong>" + x ;

        }

        function checkTime(i) {
            if (i < 10) {i = "0" + i};  
          // add zero in front of numbers < 10;
            return i;
        }


        function clearInterval() {
         }



//get_Lastdata();
//window.location = "./";
//{{ xmessage }};
//sleep(3000);