# This file is about to trials of M1 that is about to detect Modules (List)

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

def classifier(Model_path,multi_labels=False):
    ML2_1 = AutoModelForSequenceClassification.from_pretrained(Model_path)
    tokenizer2_1 = AutoTokenizer.from_pretrained(Model_path)
    ML_classifier2 = pipeline("zero-shot-classification", model=ML2_1, tokenizer=tokenizer2_1,multi_label = multi_labels)
    return ML_classifier2

Modules = ["Greetings",
           "End of the conversation",
           "Common Investigates_(Common questions about School Related only)",
           "Out of Scopes_(GK question to gain knowledge thing which is not about school's things)", 
           "Attendance_(Come & Exists Log, Presentees, absentees, Leave )", 
           "Homework_(Studies, Work & TO DO which is given from schools)", 
           "Cafeteria_(Food & Food Items, Snacks, Menu, Specials)", 
           "Class Schedule_(Class Timing)", 
           "payment_(Money & Currency)", 
           "Grade_(Exams, Marks, Rank)"]


def flow(module):
    if module == "Attendance":
        actions = ["Monthly", "Quarterly", "Half_Yearly", "Yearly"]
    elif module == 'Homework':
        actions = ["Tracking Report", "Show Homework"]
    elif module == 'Cafeteria':
        actions = ["Show Menu", "Order Food"]
    elif module == 'payment':
        actions = ["Payment process", "Payment Status"]
    elif module == 'Class Schedule':
        actions = ["Show Timetable", "Set Reminder"]
    elif module == 'Greetings':
        actions = ["Hi How can I help you?"]
    elif module == 'End of the conversation':
        actions = ["Have a nice day!"]
    else:
        actions = []
    return actions

def clean_module(name):
    module = name.split("_")[0]
    return module

def identify_module(query, classifier):
    result = classifier(query, Modules)
    print(result)
    Final_result = clean_module(result['labels'][0])
    return Final_result


@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            detected_module = identify_module(user_input, classifiers_loaded)
            # print(detected_module)
            possible_actions = flow(detected_module)
            return render_template('chat.html', user_input=user_input, detected_module=detected_module, possible_actions=possible_actions)
        else:
            return "No input provided."
    else:
        return render_template('chat.html', user_input=None, detected_module=None, possible_actions=None)

if __name__ == "__main__":
    Model_path = r'D:\Projects\Colan\FixedBid\Bobby\Demo\app\Moritz(DB variants)\Moritz(DBRT)_L'
    classifiers_loaded = classifier(Model_path,multi_labels=True)
    app.run(debug=True)
