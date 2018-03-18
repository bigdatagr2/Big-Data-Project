        function loadsocket() {
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            socket.on('connect', function() {
                // we emit a connected message to let knwo the client that we are connected.
                socket.emit('client_connected', {data: 'New client!'});
                    });

            socket.on('message', function(msg) {
                $('#counter_x').append('<p>Received: ' + msg.data + '</p>');
                alert('Le serveur a un message pour vous : ' + message);

                });

            $('#poke').click(function () {
                    socket.emit('message', 'Salut serveur, ca va ?');
                })
        }
            

