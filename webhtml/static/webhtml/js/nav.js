// JavaScript Document



function qiehuan(num) {
    
        for ( var id = 0; id <= 7; id++ ) {
            if ( document.getElementById("mynav" + id) != null) {
                 if (id == num) {
                    document.getElementById("mynav" + id).className = "nav_on";                   
                    
                }
                else {
                    document.getElementById("mynav" + id).className = "nav_off";
                    
                }
            }
        }
   
}


