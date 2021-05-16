import random

def fill_in_question(questions, index):
    numbers = []
    question_with_numbers = []
    for section in questions[index].split("_"):
            question_with_numbers.append(section)
            numbers.append(random.randrange(1, 100)*10)
            question_with_numbers.append(str(numbers[-1]))
    del question_with_numbers[-1]
    questions[index] = ''.join(question_with_numbers)
    return questions, numbers

def randomiseQuestions(questions,answers):
    # question 4
    questions, nums = fill_in_question(questions, 3)
    answers[3] = nums[0]+nums[1]+nums[2]
    # question 5
    questions, nums = fill_in_question(questions, 4)
    answers[4] = round((nums[0]*nums[1]*nums[2])/(nums[0]*nums[1]+nums[0]*nums[2]+nums[1]+nums[2]),2)
    #question 6
    questions, nums = fill_in_question(questions, 5)
    answers[5] = round(nums[0]+((nums[1]*nums[2])/(nums[1]+nums[2]))+nums[3],2)
    #questions 7
    questions, nums = fill_in_question(questions, 6)
    answers[6] = round(((nums[0]*nums[1])/(nums[0]+nums[1]))+nums[2]+((nums[3]*nums[4])/(nums[3]+nums[4])),2)
    return questions, answers
     
def get_Questions():
    questions = {
        0:"Which of these images is NOT a resistor?",
        1:"Does this circuit have any parts that are in series?",
        2:"Does the same circuit from above have any parts that are in parallel?",
        3:"Find the total resistance (Ω) of this circuit if R1 = _ Ω, R2 = _ Ω, and R3 = _ Ω.",
        4:"Find the total resistance (Ω) of this circuit if R1 = _ Ω, R2 = _ Ω, and R3 = _ Ω. Round to two decimal places.",
        5:"Find the total resistance (Ω) of this circuit if R1 = _ Ω, R2 = _ Ω, R3 = _ Ω, and R4 = _ Ω. Round to two decimal places.",
        6:"Find the total resistance (Ω) of this circuit if R1 = _ Ω, R2 = _ Ω, R3 = _ Ω, R4 = _ Ω. and R5 = _ Ω. Round to two decimal places."
    }

    # used on results page to provide feedback and teaching to the user
    hints = {
        0:"This question was answered incorrectly. If you need some help, refer to topic one: Resistors.",
        1:"This question was answered incorrectly. If you need some help, refer to topic two: Series.",
        2:"This question was answered incorrectly. If you need some help, refer to topic three: Parallel.",
        3:"This question was answered incorrectly. Did you use the formula Rt = R1 + R2 + R3? If you need some help, refer to topic two: Series.",
        4:"This question was answered incorrectly. Did you use the formula Rt = (R1 * R2 * R3) / (R1 * R2 + R1 * R3 + R2 * R3)? If you need some help, refer to topic three: Parallel.",
        5:"This question was answered incorrectly. Did you use the formula Rt = R1 + ((R2 * R3) / (R2 + R3)) + R4? If you need some help, refer to topic four: All Together.",
        6:"This question was answered incorrectly. Did you use the formula Rt = ((R1 * R2) / (R1 + R2)) + R3 + ((R4 * R5) / (R4 + R5))? If you need some help, refer to topic four: All Together."
    }

    images = {
        0:["static/img/Quiz0.png"],
        1:["static/img/Quiz1.png"],
        2:["static/img/Quiz1.png"],
        3:["static/img/Quiz2.png"],
        4:["static/img/Quiz3.png"],
        5:["static/img/Quiz4.png"],
        6:["static/img/Quiz5.png"]
    }

    answers = {
        0: "A",
        1: "Yes",
        2: "No"
    }

    questions, answers = randomiseQuestions(questions, answers)
    return (list(questions.values()), list(images.values()), list(answers.values()), list(hints.values()))


