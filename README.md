# UTILITIES
1. Referring to our git clone link: `git clone https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker.git`
2. Referring to our libraries used: `pip install -q -r requirements.txt`
3. Referring to running our project: `python main.py`

# COMPILING

## 1. Open - game setting 

When you open our game, our agent will ask you to choose whether you want the game is forced - capture or not. Originally, the game was set to be forced - capture.
![force_capture](force_capture.jpg)


After you choose your game setting, here it goes our game's interface. The purple squares represents the old position of the moved pieces while the blue one represents where did it go.
![interface](interface.jpg)


## 2. Moving

To play the game, first, you would have to choose which pieces you would like to move by entering its coordinate (y-axis before x-axis). For example, here I chose the 50 pieces to move.

Your pieces' chosen square will turn into blue and our agent will suggest you available move in white square. You will choose one of these white square and submit it. 
![choosing](choosing.jpg)

If you choose the wrong coordinate, our agent will return "Selection is not invalid. Try again" and ask you to submit another choice.
![invalid1](invalid1.jpg)
![invalid2](invalid2.jpg)

If you or your opponent execute a capturing moves, it will be represented by two purple square (position you went through) and a blue square (position you jumped to)
![capturing](capturing.jpg)

Since this is a forced - capture game, when you are in a capturable position, our agent will set by default that you have to move that pieces, which is the blue square one.
![force](force.jpg)

## 3. Promoting
When you execute a promoting move, your pieces will turn from x (the "men" piece) to X (the "king" piece, which can move backward)
![promoting1](promoting.jpg)
![promoting2](promoting2.jpg)

