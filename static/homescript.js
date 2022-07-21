var x = 0;                                                      //image counter
images = ["static/1.jpg", "static/2.jpg", "static/3.jpg", "static/4.jpg", "static/5.jpg"];                                    //Array of pictures

function imgUpdateForward() {                                   //forward button
    x = x + 1;
    if (x === 4) { x = 0; }                                     //if the counter reaches the top of the array, put it at the bottom
    document.getElementById("housePic").src = images[x];        //display the array item
};

function imgUpdateBack() {
    x = x - 1;
    if (x < 0) { x = 3; }                                       //if the counter reaches the bottom of the array, put it at the top
    document.getElementById("housePic").src = images[x];
};