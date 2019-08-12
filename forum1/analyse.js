var back = 'The result is good!';
var candidates = ['','','','','','','','','','','','','','','','','',''];
var cur_ind = [0,1,2]
var pre_click_count = []; // To store the click event.
var next_click_count = [];
var url = 'http://127.0.0.1:5000';

var questionNumber =1;

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


function changeQuestion() {
    if(questionNumber == 2) {
        document.getElementById("OP-name").value = 'jenava';
        document.getElementById("OP-title").value = 'The only emotions I feel anymore are anger and sadness.';
        document.getElementById("OP-content").value = 'Even minor inconveniences either make me incredibly angry or incredibly sad.';
    }
    else if (questionNumber == 3) {
        document.getElementById("OP-name").value = 'cjiofne';
        document.getElementById("OP-title").value = 'Does anyone else feel like being themselves takes effort';
        document.getElementById("OP-content").value = 'I just, feel I like trying to be anything at all like how ' +
            'I was before this all started is such a effort. I’ve become so bland and apathetic about anything and if I want' +
            ' anyone to like me I have to put on like this fake version of myself that’s what they’re used to. But it takes so' +
            ' much energy out of me that after a day of doing it I have to not see anyone for a few days to recover.';
    }
    else {
        //pass
    }
}

// function changeDefaultReply() {
//     if (questionNumber == 2) {
//         document.getElementById("reply").placeholder = 'Thank you for your answer in task 1! What are your thoughts  ';
//     }
//     else if (questionNumber == 3) {
//
//     }
//     else {
//         document.getElementById("reply").value = 'Thank you! You have finished all the tasks! Please inform the researcher.';
//     }
// }


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
        // Change question and change reply in the blank table
        questionNumber ++;
        changeQuestion();
        // changeDefaultReply();
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




function changePage(id){
    var page1 = document.getElementById('Page1');
    var page2 = document.getElementById('Page2');
    var page3 = document.getElementById('Page3');
    var page4 = document.getElementById('Page4');
    var page5 = document.getElementById('Page5');
    var page6 = document.getElementById('Page6');
    var page7 = document.getElementById('Page7');
    var page8 = document.getElementById('Page8');
    var page9 = document.getElementById('Page9');
    var page10 = document.getElementById('Page10');
    var pageList = new Array(page1, page2, page3, page4, page5, page6, page7, page8, page9, page10);
    var count = pageList.length;
    switch (id) {
        case "bp1":
            for(var item in pageList) {
                if (pageList[item] == page1) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp2":
            for(var item in pageList) {
                if (pageList[item] == page2) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp3":
            for(var item in pageList) {
                if (pageList[item] == page3) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp4":
            for(var item in pageList) {
                if (pageList[item] == page4) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp5":
            for(var item in pageList) {
                if (pageList[item] == page5) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp6":
            for(var item in pageList) {
                if (pageList[item] == page6) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp7":
            for(var item in pageList) {
                if (pageList[item] == page7) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp8":
            for(var item in pageList) {
                if (pageList[item] == page8) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp9":
            for(var item in pageList) {
                if (pageList[item] == page9) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
        case "bp10":
            for(var item in pageList) {
                if (pageList[item] == page10) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
    }
}



