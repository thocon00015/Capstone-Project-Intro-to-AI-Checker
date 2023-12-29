# UTILITIES
1. Referring to our git clone link: `git clone https://github.com/thocon00015/Capstone-Project-Intro-to-AI-Checker.git`
2. Referring to our libraries used: `pip install -q -r requirements.txt`
3. Referring to running our project: `python main.py`

# COMPILING

## 1. Open - game setting 

When you open our game, our agent will ask you to choose whether you want the game is forced - capture or not. Originally, the game was set to be forced - capture.
![force_capture](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/cae0fb35-529d-4559-9a7c-9008af63a04c)


After you choose your game setting, here it goes our game's interface. The purple squares represents the old position of the moved pieces while the blue one represents where did it go.
![interface](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/a08ffdae-b20d-4e16-8f50-2df43dfce83f)

## 2. Moving

To play the game, first, you would have to choose which pieces you would like to move by entering its coordinate (y-axis before x-axis). For example, here I chose the 50 pieces to move.

Your pieces' chosen square will turn into blue and our agent will suggest you available move in white square. You will choose one of these white square and submit it. 
![choosing](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/e3c69c9b-9dba-452c-a430-be214b5717c8)

If you choose the wrong coordinate, our agent will return "Selection is not invalid. Try again" and ask you to submit another choice.
![invalid1](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/50e0f728-c223-4596-9c99-74a91091779b)
![invalid2](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/6b34277c-b9dc-4400-9f94-449e004bc9a6)

If you or your opponent execute a capturing moves, it will be represented by two purple square (position you went through) and a blue square (position you jumped to)
![capturing](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/0c7fd8e1-45e6-4d25-9a1b-53aff895fdd4)

Since this is a forced - capture game, when you are in a capturable position, our agent will set by default that you have to move that pieces, which is the blue square one.
![force](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/cbcc397f-12e5-4a1e-92c1-0a838867bc15)

## 3. Promoting
When you execute a promoting move, your pieces will turn from x (the "men" piece) to X (the "king" piece, which can move backward)
![promoting](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/7c60c2d0-cbe5-4275-a728-56ab22d56e21)
![promoting2](https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/577b1372-a740-42e1-be3f-3dc286856df5)

## 4. Explaining rules video
https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/b9003540-2b37-4fed-b0cd-c1efa0552778

## 5. How we improve our agent
https://github.com/thocon00015/Intro-to-AI-Capstone-Project-Checker/assets/102193912/7008bd7d-0f35-4ec4-a200-bb525906033d



