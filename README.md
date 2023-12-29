# UTILITIES
1. Referring to our git clone link: `git clone https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker.git`
2. Referring to our libraries used: `pip install -q -r requirements.txt`
3. Referring to running our project: `python main.py`

# COMPILING

## 1. Open - game setting 

When you open our game, our agent will ask you to choose whether you want the game is forced - capture or not. Originally, the game was set to be forced - capture.
![force_capture](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/1e6d8d15-485d-401c-9eb8-e20cb8690511)


After you choose your game setting, here it goes our game's interface. The purple squares represents the old position of the moved pieces while the blue one represents where did it go.
![interface](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/03ed9794-6057-44b5-bccd-ee9e4ed4ef82)

## 2. Moving

To play the game, first, you would have to choose which pieces you would like to move by entering its coordinate (y-axis before x-axis). For example, here I chose the 50 pieces to move.

Your pieces' chosen square will turn into blue and our agent will suggest you available move in white square. You will choose one of these white square and submit it. 
![choosing](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/f8e3b6ac-a60d-4142-b808-75fc0514f5d7)

If you choose the wrong coordinate, our agent will return "Selection is not invalid. Try again" and ask you to submit another choice.
![invalid1](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/f743ee84-5558-4196-8e98-b98735612438)
![invalid2](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/e0fce3ed-2e31-4967-870d-14d983b2631e)

If you or your opponent execute a capturing moves, it will be represented by two purple square (position you went through) and a blue square (position you jumped to)
![capturing](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/db655057-ab53-417f-b305-825689fee401)

Since this is a forced - capture game, when you are in a capturable position, our agent will set by default that you have to move that pieces, which is the blue square one.
![force](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/af4296e7-59a9-440f-a5f0-27f8af951127)

## 3. Promoting
When you execute a promoting move, your pieces will turn from x (the "men" piece) to X (the "king" piece, which can move backward)
![promoting](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/9a8208cb-6703-4547-92a6-d70e8150b540)
![promoting2](https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/163c8825-51f1-470c-965d-f4970cfa14ea)


## 4. Explaining rules video
https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/ea9508de-eb53-41e5-b4d4-37dab2e3b858

## 5. How we improve our agent
https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker/assets/102193912/27c3d8f7-789e-4575-92ce-f418ffe261c9


