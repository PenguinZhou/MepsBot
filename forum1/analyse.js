var back = 'The result is good!';
var candidates = ['','','','','','','','','','','','','','','','','',''];
var cur_ind = [0,1,2]
var pre_click_count = []; // To store the click event.
var next_click_count = [];
var url = 'http://127.0.0.1:5000';

function getPy() {
//     // const pyOut = 'Hello word';
//     // console.log(pyOut);
    var sendVar = document.getElementById("reply").value;
    if (sendVar == '') {return 0;}
    // console.log(sendVar);
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
//Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            // values
            var result = http.responseText;
            // console.log(result + ": result here");
            back = JSON.parse(result);
            if (back.mode == 'AF') {
                var IS = 'Medium';
                var ES = 'Medium';
                if (back.IS_score == 1) {IS = 'Low';} else if (back.IS_score == 3) {IS = 'High';}
                if (back.ES_score == 1) {ES = 'Low';} else if (back.ES_score == 3) {ES = 'High';}
                // console.log(back.IS_score)
                var dialogue = back.feedback;
                
                var score_script = 'Informational Support: ' + IS + '<br>'
                            + 'Emotional Support: ' + ES + '<br>';
                            
                var suggestion_script =  dialogue;
                document.getElementById("title_box").style.display="";
                document.getElementById("title").innerHTML = 'Writing help';

                document.getElementById("assess_box").style.display="";
                document.getElementById("EvaluationResult").innerHTML = score_script;

                document.getElementById("feedback_box").style.display="";
                document.getElementById("suggestion").innerHTML = suggestion_script;
                
                document.getElementById("submit_btn").style.display="";
            }
            else if (back.mode == 'RE') {
                for (i = 0; i < candidates.length; i++) { 
                    var index = i.toString()
                    candidates[i] = back[index]
                }
                
                document.getElementById("title_box").style.display="";
                document.getElementById("title").innerHTML = 'Some good comments';
                document.getElementById("pre_rec").style.display="";
                document.getElementById("next_rec").style.display="";
                
                document.getElementById("help_box_1").style.display="";
                document.getElementById("rec_1").innerHTML = candidates[0]
                document.getElementById("help_box_2").style.display="";
                document.getElementById("rec_2").innerHTML = candidates[1]
                document.getElementById("help_box_3").style.display="";
                document.getElementById("rec_3").innerHTML = candidates[2]
                document.getElementById("submit_btn").style.display="";
            }
           
            // const outVal = sendResponse({response: result});
        }
    };
    http.send(sendVar);

}

function showResult(){
    getPy();
}


function submit_one(){
    // console.log('hahah')
    var sendVar = document.getElementById("reply").value;
    var final_com = 'Yeah final' + sendVar;
    var http = new XMLHttpRequest();
    http.open('POST', url, true);
//Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        // values
        var result = http.responseText;
        back = result;
        // console.log(back)
        
        document.getElementById("submit_btn").style.display="None";
        document.getElementById("title_box").style.display="None";
        document.getElementById("assess_box").style.display="None";
        document.getElementById("feedback_box").style.display="None";
        document.getElementById("help_box_1").style.display="None";
        document.getElementById("help_box_2").style.display="None";
        document.getElementById("help_box_3").style.display="None";
        document.getElementById("reply").value = 'Thank you! You have finished the current task! Please inform the researcher.';
        //Refresh the post, and the reply box.
        //Coding here
    }
    };
    http.send(final_com);
}

function pre_rec(){
    if (cur_ind[0]==0){;}
    else{
        cur_ind[0] = cur_ind[0] - 3; cur_ind[1] = cur_ind[1] - 3; cur_ind[2] = cur_ind[2] - 3;
    }
    document.getElementById("rec_1").innerHTML = candidates[cur_ind[0]]
    document.getElementById("rec_2").innerHTML = candidates[cur_ind[1]]
    document.getElementById("rec_3").innerHTML = candidates[cur_ind[2]]
}

function next_rec(){
    if (cur_ind[2]==17){;}
    else{
        cur_ind[0] = cur_ind[0] + 3; cur_ind[1] = cur_ind[1] + 3; cur_ind[2] = cur_ind[2] + 3;
        document.getElementById("rec_1").innerHTML = candidates[cur_ind[0]]
        document.getElementById("rec_2").innerHTML = candidates[cur_ind[1]]
        document.getElementById("rec_3").innerHTML = candidates[cur_ind[2]]
    }
}


function changePage1(){
    var secondPage = document.getElementById('secondPage');
    var firstPage = document.getElementById('firstPage');
    var thirdPage = document.getElementById('thirdPage');
    secondPage.style = "display: none";
    firstPage.style = "display: inline";
    thirdPage.style = "display: none";
    firstPage.className = "col-lg-8 col-md-8";
    secondPage.className = "col-lg-8 col-md-8";
    thirdPage.className = "col-lg-8 col-md-8";
}


function changePage2(){
    var secondPage = document.getElementById('secondPage');
    var firstPage = document.getElementById('firstPage');
    var thirdPage = document.getElementById('thirdPage');
    secondPage.style = "display: inline";
    firstPage.style = "display: none";
    thirdPage.style = "display: none";
    firstPage.className = "col-lg-8 col-md-8";
    secondPage.className = "col-lg-8 col-md-8";
    thirdPage.className = "col-lg-8 col-md-8";
}

function changePage3(){
    var secondPage = document.getElementById('secondPage');
    var firstPage = document.getElementById('firstPage');
    var thirdPage = document.getElementById('thirdPage');
    secondPage.style = "display: none";
    firstPage.style = "display: none";
    thirdPage.style = "display: inline";
    firstPage.className = "col-lg-8 col-md-8";
    secondPage.className = "col-lg-8 col-md-8";
    thirdPage.className = "col-lg-8 col-md-8";
}