# This file is about of M1 Model - Modules (Description)

from flask import Flask, render_template, request

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

app = Flask(__name__)



# def load_classifiers(multi_labels=False):
#     FB1 = AutoModelForSequenceClassification.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\FB1')
#     tokenizer1 = AutoTokenizer.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\FB1')
#     fb_classifier = pipeline("zero-shot-classification", model=FB1, tokenizer=tokenizer1,multi_label = multi_labels)
#     ML2 = AutoModelForSequenceClassification.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\ML2')
#     tokenizer2 = AutoTokenizer.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\ML2')
#     ML_classifier = pipeline("zero-shot-classification", model=ML2, tokenizer=tokenizer2,multi_label = multi_labels)
#     SL3 = AutoModelForSequenceClassification.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\SL3')
#     tokenizer3 = AutoTokenizer.from_pretrained(r'D:\Projects\Colan\FixedBid\Bobby\Demo\Models\SL3')
#     SL_classifier = pipeline("zero-shot-classification", model=SL3, tokenizer=tokenizer3,multi_label = multi_labels)
#     return [fb_classifier, ML_classifier,SL_classifier]


Modules_description = {
    "Greetings": {
        "keywords": [],
        "description": ""
    },

    "End of the conversation": {
        "keywords": [],
        "description": ""
    },

    "Common Investigates": {
        "keywords": [],
        "description": "Common questions about School Related only"
    },

    "Out of Scopes": {
        "keywords": [],
        "description": "GK question to gain knowledge thing which is not about school's things"
    },

    "Attendance": {
        "keywords": [],
        "description": "Come & Exists Log, Presentees, absentees, Leave"
    },

    "Homework": {
        "keywords": [],
        "description": "Studies, Work & TO DO which is given from schools"
    },

    "Class Schedule": {
        "keywords": [],
        
        "description": "predetermined timetable that outlines the Class Timing"
    },

    "Fees_module": {
        "keywords": [], 
        "description": "It refers about Money or payment especially relavant in schools related to the monetary payments required from students or their parents/guardians for various Purposes or Classes"
    }
}



# Modules = ["Greetings",
#            "End of the conversation",
#            "Common Investigates",
#            "Out of Scopes", 
#            "Attendance", 
#            "Homework", 
#            "Class Schedule", 
#            "Fees"]

def classifier(Model_path,multi_labels=False):
    ML2_1 = AutoModelForSequenceClassification.from_pretrained(Model_path)
    tokenizer2_1 = AutoTokenizer.from_pretrained(Model_path)
    ML_classifier2 = pipeline("zero-shot-classification", model=ML2_1, tokenizer=tokenizer2_1,multi_label = multi_labels)
    return ML_classifier2


def flow(module):
    if module == "Attendance":
        actions = ["Attendance report", "Condition Based"]
    elif module == 'Homework':
        actions = ["Homework Report", "Show Homework"]
    elif module == 'Cafeteria':
        actions = ["Show Menu", "Order Food"]
    elif module == 'Fees':
        actions = ["Payment Report", "Pending Payment", "Completed Payment"]
    elif module == 'Class Schedule':
        actions = ["Show Timetable", "Set Reminder"]
    elif module == 'Greetings':
        actions = ["Hi How can I help you?"]
    elif module == 'End of the conversation':
        actions = ["Have a nice day!"]
    else:
        actions = []
    return actions

def Modules(Modules_description):
    Modules_List = []
    for i,j in Modules_description.items():
        Modules_List.append(f"{i}_({j['description']})")
    return Modules_List

def clean_module(name):
    module = name.split("_")[0]
    return module

def identify_module(query, classifier,Modules_List):
    result = classifier(query, Modules_List)
    Labels = [clean_module(i) for i in result['labels']]
    makeup_result = result.copy()
    makeup_result['labels'] = Labels
    print(makeup_result)
    Final_result = clean_module(result['labels'][0])
    return Final_result


@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            Modules_List = Modules(Modules_description)
            detected_module = identify_module(user_input, classifiers_loaded,Modules_List)
            # print(detected_module)
            possible_actions = flow(detected_module)
            return render_template('chat.html', user_input=user_input, detected_module=detected_module, possible_actions=possible_actions)
        else:
            return "No input provided."
    else:
        return render_template('chat.html', user_input=None, detected_module=None, possible_actions=None)

if __name__ == "__main__":
    Model_path = r'D:\Projects\Colan\FixedBid\Bobby\AvatarBot Project\Trials\Avatar Bot\M1 Model\Moritz(DB variants)\Moritz(DBRT)_L'
    classifiers_loaded = classifier(Model_path,multi_labels=True)
    app.run(debug=True)
