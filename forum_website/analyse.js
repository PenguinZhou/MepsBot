var back = 'The result is good!';
var candidates = ['','','','','','','','','','','','','','','','','',''];

var click_record = ''; // To store the click event, 0 - pre_rec; 1 - next_rec.
// var next_click_count = [];
var url = 'http://127.0.0.1:5000';

var questionNumber = -1;




var op_post_order = [2,0,1];

var initial_comment = '';
var submitted_comment = '';

var first_click = true;


intro_0 = 'Hi, <mark>MepsBot</mark> here!';
intro_1 = '<b>I can help check your comment and give you some feedbacks. I will securely protect your data.</b> <br> It is important to show <b>informational (e.g., advice, knowledge)</b> and <b>emotional (e.g., understanding, encouragement)</b> support in your comment. ';
intro_2 = '<b>I can recommend some good comments that could be similar to your current one. I will securely protect your data.</b> <br> It is important to show <b>informational (e.g., advice, knowledge)</b> or <b>emotional (e.g., understanding, encouragement) support</b> in your comment.';

var cur_ind = [0,1,2]
function getPy() {
//     // const pyOut = 'Hello word';
//     // console.log(pyOut);
    
    

    var sendVar = document.getElementById("reply").value;
    // Check if it is the first click in the task.
    
    if (sendVar == '') {return 0;}

    if (document.getElementById("preview_btn").innerHTML == 'Preview') {
        document.getElementById("preview_btn").innerHTML = 'Back to edit';
        document.getElementById("reply").disabled = true;
    }
    else {
        document.getElementById("preview_btn").innerHTML = 'Preview';
        document.getElementById("submit_btn").style.display = "None";
        document.getElementById("reply").disabled = false;
        return 0;
    }
    var with_record = sendVar + 'click event:' + click_record;
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
                
                // else {document.getElementById("title_box").style.display="None";}
                var IS = 'Medium';
                var ES = 'Medium';
                if (back.IS_score == 1) {IS = 'Low';} else if (back.IS_score == 3) {IS = 'High';}
                if (back.ES_score == 1) {ES = 'Low';} else if (back.ES_score == 3) {ES = 'High';}
                // console.log(back.IS_score)
                var feedback_1 = back.feedback_1;
                var feedback_2 = back.feedback_2;
                var score_script = intro_1 + '<br><br><b>Report on your comment:</b> <br>' + 'Informational Support: ' + '<mark>' + IS + '</mark>' + '<br>'
                            + 'Emotional Support: ' + '<mark>' + ES + '</mark>' + '<br>';
                document.getElementById("title_box").style.display="";
                // document.getElementById("title").innerHTML = intro_0;
                document.getElementById("intro").innerHTML = score_script;
                if (first_click == true) {
                    initial_comment = sendVar; 
                    
                    first_click = false;
                }            
                // var suggestion_script =  feedback_2;
                
                // document.getElementById("assess_box").style.display="";
                // document.getElementById("EvaluationResult").innerHTML = score_script;

                document.getElementById("feedback_box").style.display="";
                document.getElementById("feedback_1").innerHTML = feedback_1;
                document.getElementById("suggestion").innerHTML = feedback_2;
                
                document.getElementById("submit_btn").style.display="";
            }
            else if (back.mode == 'RE') {
                for (i = 0; i < candidates.length; i++) { 
                    var index = i.toString()
                    candidates[i] = back[index]
                }
                var re_feedback_script = intro_2 + '<br><br>' + back.feedback + '<br> <font color=blue>blue word</font> - personal pronouns <br> <mark><font color=green>green word</font></mark> - about family and friend <br> <mark><font color=red>red word</font></mark> - positive word';
                // else {document.getElementById("title_box").style.display="None";}
                // document.getElementById("re_feedback_box").style.display="";
                document.getElementById("title_box").style.display="";
                    // document.getElementById("title").innerHTML = intro_0;
                document.getElementById("intro").innerHTML = re_feedback_script;
                if (first_click == true) {
                    initial_comment = sendVar; 
                    
                    first_click = false;
                }
                // document.getElementById("re_feedback").innerHTML = ;
                // document.getElementById("re_note").innerHTML = 'Note: <br> <font color=blue>blue word</font> - personal nouns <br> <mark><font color=green>green word</font></mark> - about family and friend <br> <mark><font color=red>red word</font></mark> - positive word';

                document.getElementById("title_box").style.display="";
                // document.getElementById("title").innerHTML = 'Some good comments';
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
    http.send(with_record);

}

function preview(){
    getPy();
}

op_title = ["How did you find your interested area and establish your goals?", "I must be the most failure failed Ph.D. student in the world", "Just want someone to talk to", "Thank you for our time"];
op_content = ["Most people around me have specific goals or something to work toward, but I have no idea what my goal is. It seems that everyone around me know what they really want to do in the future and they all have specific life plan. Some of them want to be a professor, some of them want to be an engineer, and they are pursuing their dreams step by step, making progress along their expected path every day. I really admire and appreciate them. It is a shame to admit that although I am no longer an undergraduate student, I still have no idea what is my love. For most time of my life, I am more like a follower, rather than a leader, or at least have a big picture about which stage am I at. I went to school, attended activities, trying to be the top students among others. I was successful to get some high scores, but still, I have no idea about my future. <br><br> Achievements in frontier research is more important than good performance in courses, in my opinion. I have tried some research fields, but finally none of them became my interest. Now I am trying something new, so far, I don’t have that kind of disgusting feeling, but I am not sure whether it is my love. Everyone around me told that you need to have pure love, you need to be really interested in some area, otherwise your motivation is not strong. But the question is I still have no idea about what type of feeling is true interest. I was also suspicious that whether I am just escaping from something since I lost interest in almost everything you have tried. Sorry if I brought you down. I just needed to put it out there. I'm tired of being asked what my goals are in life and what I want. I hate the feeling of working hard every day like a robot but seems to be aimless efforts. Has anyone else felt like this? How did you find your interested area? How did you establish your life goal? Any advice would be much appreciated.", 
            "I am a senior Ph.D. student without any paper, living with sadness and depression. It's my sixth time to fail to finish the experiment before the submission deadline. I am aware that I am nothing but a pile of academic rubbish which even has no value for recycling.  Compared to my friends, my classmates or even anyone standing in the hall of the conference, I felt embarrassed and no reason for me to exist in this world. I am now helplessly laying on the bed, waiting for another sunrise. I have no contribution to the world. My life is not worth a straw.",
            "I have worked continuously for half a month without a break. I want to take a break but I can’t. My labmates are hardworking. I want to earn a lot of money to live a better life in the future. All I can do now is working hard. I tried to invest money in the stock before but I lost a lot of money in the end. I tried to save money by eating cheap food, but failed because I can not control myself on that. <br> <br> The bad feeling is that I worry even though I work hard, I can not have a good result. Recently I turned to be angry easily, even with the voice from a small dog. I am worried about how to earn money now and future. My girlfriend said we should buy a house before wedding. My family is still in debt and I want to pay for my father. But now I could do nothing, just sitting in the lab, and can not sleep well at night. I went to the therapy before. It worked for several days. But now I don’t think I have time for that. Maybe I am in another cycle of depression.",
            "Really appreciate your participation."]
op_author_name = ['jenava', 'cjiofne', 'circinia', 'Harry'];


function changeQuestion() {
    console.log(op_author_name[op_post_order[questionNumber]])
    document.getElementById("OP-name").innerHTML = op_author_name[op_post_order[questionNumber]];
    document.getElementById("OP-title").innerHTML = op_title[op_post_order[questionNumber]];
    document.getElementById("OP-content").innerHTML = op_content[op_post_order[questionNumber]];
        // document.getElementById("OP-name").value = 'jenava';
        // document.getElementById("OP-title").value = 'The only emotions I feel anymore are anger and sadness.';
        // document.getElementById("OP-content").value = 'Even minor inconveniences either make me incredibly angry or incredibly sad.';

        // document.getElementById("OP-name").value = 'cjiofne';
        // document.getElementById("OP-title").value = 'Does anyone else feel like being themselves takes effort';
        // document.getElementById("OP-content").value = 'I just, feel I like trying to be anything at all like how ' +
        //     'I was before this all started is such a effort. I’ve become so bland and apathetic about anything and if I want' +
        //     ' anyone to like me I have to put on like this fake version of myself that’s what they’re used to. But it takes so' +
        //     ' much energy out of me that after a day of doing it I have to not see anyone for a few days to recover.';
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

function refresh(){
    document.getElementById("submit_btn").style.display="None";
    document.getElementById("title_box").style.display="None";
    document.getElementById("assess_box").style.display="None";
    document.getElementById("feedback_box").style.display="None";
    document.getElementById("pre_rec").style.display="None";
    document.getElementById("next_rec").style.display="None";
    document.getElementById("help_box_1").style.display="None";
    document.getElementById("help_box_2").style.display="None";
    document.getElementById("help_box_3").style.display="None";
    document.getElementById("re_feedback_box").style.display="None";
    document.getElementById("reply").value = '';
    document.getElementById("reply").placeholder = 'What are your thoughts?';
}


AF_link = ['https://ust.az1.qualtrics.com/jfe/form/SV_cSeQp6Vp3HD5mq9', 'https://ust.az1.qualtrics.com/jfe/form/SV_3duYolI1lpVeU0R', 'https://ust.az1.qualtrics.com/jfe/form/SV_3awSXNNJMUds7u5'];
RE_link = ['https://ust.az1.qualtrics.com/jfe/form/SV_6yDq7gEQBj154oJ', 'https://ust.az1.qualtrics.com/jfe/form/SV_5opGe34GORLPiGF', 'https://ust.az1.qualtrics.com/jfe/form/SV_b1Jf6bgo3s6BwMZ'];
AF_final_link = 'https://ust.az1.qualtrics.com/jfe/form/SV_7VBbK0ElQijHoi1';
RE_final_link = 'https://ust.az1.qualtrics.com/jfe/form/SV_cBxm2Vo0YLXif1r';



function submit_one(){
    document.getElementById("reply").disabled = false;
    document.getElementById("preview_btn").innerHTML = 'Preview';
    if (questionNumber == -1) {refresh(); questionNumber ++; changeQuestion(); first_click = true;}
    else {
        var sendVar = document.getElementById("reply").value;
        submitted_comment = sendVar;
        var final_com = 'Yeah final' + sendVar + 'click event:' + click_record;
        var http = new XMLHttpRequest();
        http.open('POST', url, true);
    //Send the proper header information along with the request
        http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            // values
            var result = http.responseText;
            // back = result;  
            back = JSON.parse(result);
            refresh();
            // console.log(document.getElementById("com_initial"));
            // document.getElementById("com_initial").innerHTML = initial_comment;
            // document.getElementById("com_final").innerHTML = submitted_comment;
            // document.getElementById("reply").value = 'Thank you! You have finished the current task! Please inform the researcher.';
            //Refresh the post, and the reply box.
            //Coding here
            // Change question and change reply in the blank table
            // document.getElementById("initial_com_box").style.display="";
            // document.getElementById("submitted_com_box").style.display="";
            // document.getElementById("survey_box").style.display="";
            // document.getElementById("initial_com").innerHTML = initial_comment;
            // document.getElementById("submitted_com").innerHTML = submitted_comment;
            // document.getElementById("survey_msg").innerHTML="Please fill in the survey in this link: <br>";
            // document.getElementById("link").href = survey_link[questionNumber];
            // document.getElementById("survey_msg_1").innerHTML = 'You need to refer the initial comment and final submitted comment in this page when filling the survey.' + '<br>'
            //                                                 + 'When you finish, click the \'Next task\' button to start next task';
            click_record = '';
            if (back.mode == 'AF') {window.open(AF_link[questionNumber], '_blank');}
            if (back.mode == 'RE') {window.open(RE_link[questionNumber], '_blank');}
            questionNumber ++;
            changeQuestion();
            first_click = true;
            
            
            if (questionNumber == 3) {refresh(); 
                document.getElementById("OP-name").innerHTML = 'Harry';
                document.getElementById("OP-title").innerHTML = 'Thank you for your participation.';
                document.getElementById("OP-content").innerHTML = 'Really appreciate you.'; 
                
                if (back.mode == 'AF') {document.getElementById("reply").value = 'Link to final survey: ' + AF_final_link;}
                if (back.mode == 'RE') {document.getElementById("reply").value = 'Link to final survey: ' + RE_final_link;}
            }
                
        }
        };
        http.send(final_com);
    }
}



function next_task(){
    // document.getElementById("initial_com_box").style.display="None";
    // document.getElementById("submitted_com_box").style.display="None";
    // document.getElementById("survey_box").style.display="None";
    questionNumber ++;
    changeQuestion();
    first_click = true;
    if (questionNumber == 3) {refresh(); 
        document.getElementById("OP-name").innerHTML = 'Harry';
        document.getElementById("OP-title").innerHTML = 'Thank you for your participation.';
        document.getElementById("OP-content").innerHTML = 'Really appreciate you.'; 
        document.getElementById("reply").value = 'Thank you! You have finished all the tasks.';}
}






function pre_rec(){
    if (cur_ind[0]==0){;}
    else{
        cur_ind[0] = cur_ind[0] - 3; cur_ind[1] = cur_ind[1] - 3; cur_ind[2] = cur_ind[2] - 3;
        click_record = click_record + '0 '
    }
    document.getElementById("rec_1").innerHTML = candidates[cur_ind[0]]
    document.getElementById("rec_2").innerHTML = candidates[cur_ind[1]]
    document.getElementById("rec_3").innerHTML = candidates[cur_ind[2]]
}

function next_rec(){
    if (cur_ind[2]==17){;}
    else{
        cur_ind[0] = cur_ind[0] + 3; cur_ind[1] = cur_ind[1] + 3; cur_ind[2] = cur_ind[2] + 3;
        click_record = click_record + '1 '
        document.getElementById("rec_1").innerHTML = candidates[cur_ind[0]]
        document.getElementById("rec_2").innerHTML = candidates[cur_ind[1]]
        document.getElementById("rec_3").innerHTML = candidates[cur_ind[2]]
    }
}

function deactiveNumber() {
    document.getElementById('tp1').className = "";
    document.getElementById('tp2').className = "";
    document.getElementById('tp3').className = "";
    document.getElementById('tp4').className = "";
    document.getElementById('tp5').className = "";
    document.getElementById('tp6').className = "";
    document.getElementById('tp7').className = "";
    document.getElementById('tp8').className = "";
    document.getElementById('tp9').className = "";
    document.getElementById('tp10').className = "";
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

    // The following code is too redundant, but I am so tired that I don't want to modify any.
    // for(var item in pageList) {
    //     pageList[item].style = "display: none";
    //     pageList[item].className = "col-lg-8 col-md-8";
    // }

    deactiveNumber()
    switch (id) {
        case "bp1":
            for(var item in pageList) {
                if (pageList[item] == page1) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                    document.getElementById(id).childNodes[0].className = "active";
                }
            }
            break;
        case "bp8":
            for(var item in pageList) {
                if (pageList[item] == page8) {
                    pageList[item].style = "display: inline";
                    pageList[item].className = "col-lg-8 col-md-8";
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
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
                    document.getElementById(id).childNodes[0].className = "active";
                }
                else {
                    pageList[item].style = "display: none";
                    pageList[item].className = "col-lg-8 col-md-8";
                }
            }
            break;
    }
}



