const robotSocket = new WebSocket (window.WS_ROUTE);

robotSocket.onopen = function(e){
    console.log("User has been successfully connected to control panel");
}

robotSocket.onmessage = function(e){
    const data = JSON.parse(e.data)
    data = data.data;
    if(data.status = "SUCCESS"){
        if (data.data){
            const type = data.data.type;
            data = data.data.data;

            type = type.split("_")
            
            if (type[0] == "camera"){

            }else{
                switch(type){
                    case "position":
                        break;
                    case "goal":
                        break;
                    case "vlm_request":
                        break;
                    default:
                        break;
                }
            }
        }else{

        }
        
        
    }else {
        
    }
}

socket.robotSocket.onclose = function(e){

}

socket.robotSocket.onerror = function(e){

}

