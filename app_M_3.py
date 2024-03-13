# This File is about Trials of M2 followed by the success of M1

from flask import Flask, render_template, request
import time
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from flask import jsonify

app = Flask(__name__)

# Global variable to store chat history
chat_history = []


Modules_description = {
    "Greetings": {
        "keywords": [],
        "description": "It's a warm intro at the starting of conversation"
    },

    "End of the conversation": {
        "keywords": [],
        "description": ""
    },

    "Out of Scopes": {
        "keywords": [],
        "description": "Questions to gain knowledge not related to Schools info"
    },

    "Attendance": {
        "keywords": [],
        "description": "Information about individuals' presence, absence, leave records, and a list of names."
    },

    "Homework": {
        "keywords": [],
        "description": "Homework refers to tasks assigned by schools for students."
    },

    "Class Schedule": {
        "keywords": [],
        
        "description": "It pertains to all class periods, which constitute a predetermined timetable outlining the timing of each class."
    },

    "Fees_module": {
        "keywords": [], 
        "description": "It refers about Money or payment especially relavant in schools related to the monetary payments like fees required from students or their parents/guardians for various Purposes which is related to all Academic things"
    },
    "Performance_Modules": {
        "keywords": [],
        "description": "It's all related about marks, academic performance, grade levels"
    },
}



def classifier(Model_path,multi_labels=False):
    ML2_1 = AutoModelForSequenceClassification.from_pretrained(Model_path)
    tokenizer2_1 = AutoTokenizer.from_pretrained(Model_path)
    ML_classifier2 = pipeline("zero-shot-classification", model=ML2_1, tokenizer=tokenizer2_1,multi_label = multi_labels)
    return ML_classifier2


def flow(module):
    if module == "Attendance":
        actions = {
            "Attendance report":{
                        "keywords": [],
                        "description": "It revolves around providing or is associated with attendance records. Based on user's preference It has many options to show the report for showing specific usecase."
                        },
            "Condition Based":
                        {
                             "keywords": [],
                             "description": "Conditionally, it extracts details from the attendance records, based on user's conditional clause."
                             }}

        
    elif module == 'Homework':
        actions = {
            "Homework Report": {
                "keywords": [],
                "description": "It involves extracting details from the Homework Report, highlighting tasks they have previously completed. Incorporating tasks that have been finished or are still pending, along with their respective comments."
                },
            "Show Homework":{
                    "keywords": [],
                    "description": "It pertains to displaying or retrieving details about assigned homework for individuals or specific categories of individuals."
                    }
        }


    elif module == 'Fees':
        actions = {
            "Payment Report": {
                "Related_column": [],
                "keywords": [],
                "description": "It related to displays existing concerning completed payments reports, particularly focusing on fees that students or their representatives are required to pay for certain classes."
                },
            "Pending Payment":{
                    'Related_column':['status'],
                    "keywords": [],
                    "description": "It provides information regarding outstanding payments, specifically focusing on balance payments, particularly in relation to fees."
                    },
            "Completed Payment":{
                    'Related_column':['status'],
                    "keywords": [],
                    "description": "It furnishes details concerning payment completed lists, particularly in connection with fees without any pending payments."
                    }
        }

    
        
    elif module == 'Class Schedule':
        actions = {
            "Show Timetable": {
                "keywords": [],
                "description": "It involves retrieving the timetable and displaying it exclusively in specific level as per user's request."
                },
            "Set Reminder":{
                    "keywords": [],
                    "description": "It involves retrieving the timetable data and setting a reminder or notify the user prior the class schedule as per the notification time set by the user or else intimate immediately."
                    }
        }
    elif module == 'Greetings':
        actions = {
            "Welcome": {
                "keywords": [],
                "description": ""
                }}
        
    elif module == 'End of the conversation':
            actions = {
                "Sent off": {
                "keywords": [],
                "description": ""
                },
            }
    
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

def identify_module(query, classifier, Modules_List):
    result = classifier(query, Modules_List)
    Labels = [clean_module(i) for i in result['labels']]
    makeup_result = result.copy()
    makeup_result['labels'] = Labels
    print(makeup_result)
    Final_result = clean_module(result['labels'][0])
    return Final_result

def sequence(user_input, Modules_description):
    Modules_List = Modules(Modules_description)
    detected_module = identify_module(user_input, classifiers_loaded, Modules_List)
    possible_actions = flow(detected_module)
    return detected_module, possible_actions


def data_perform(user_input, Modules_description):
    function = Modules(Modules_description)
    detected_module = identify_module(user_input, classifiers_loaded, function)
    return detected_module


def data_query(user_input,agg_fns,data_fetch):
    data_fetch_fn = data_perform(user_input,data_fetch)
    agg_fn = data_perform(user_input,agg_fns)
    return data_fetch_fn,agg_fn



Choices = {

    'Payment Report': {
        'Term_wise':['termName'],

        'Overall':[],
        
        'Class_wise':{
            "column": ['className'],
            'options':{
                'division': ["division"],
                'overall' : []
            }
            }
    },
    'Pending Payment': {
        'Term_wise':['termName'],
        'Overall':[],
        'Class_wise':['className']
    },
    'Completed Payment': {
        'Term_wise':['termName'],
        'Overall':[],
        'Class_wise':['className']
    }
}


@app.route('/', methods=['GET', 'POST'])
def chat():
    global chat_history
    detected_module = None
    possible_actions = None
    user_input = None

    if request.method == 'POST':
        user_input = request.form['user_input']
        ST = time.time()

        if str(user_input).lower() == 'clear':
                chat_history.clear()
                return jsonify({'type':'clear_chat','messages':'chat cleared'})

        elif user_input:

            # First run
            detected_module, possible_actions = sequence(user_input, Modules_description)

            if possible_actions and len(possible_actions) > 0:
                possible_actions, _ = sequence(user_input, possible_actions)

            try:
                options1 = Choices[possible_actions].keys()
                Options = list(options1)
                print(Options, 'options data')
                if Options:
                    suggestions_data = {'type':'suggestions','suggestions': Options, 'user': user_input, 'bot_module': detected_module, 'bot_actions': possible_actions}
                    return jsonify(suggestions_data)
            except:
                pass

            chat_entry = {'type':'detections', 'user': user_input, 'bot_module': detected_module, 'bot_actions': possible_actions}
            chat_history.append(chat_entry)
            print(chat_entry, "chat entry data")

        ET = time.time()
        print(f'Time = {ET - ST}_secs')

        # Return the chat entry data as JSON
        return jsonify(chat_entry)
    else:
    # Render the template with chat history
        return render_template('chat.html', user_input=user_input, chat_history=chat_history)
    
@app.route('/new-chat', methods=['POST'])
def new_chat():
        user_input = request.form['user_input']
        print(user_input,'jjjjjjj')
        chat_entry = {'type':'new_chat', "user":user_input}
        return jsonify(chat_entry)


if __name__ == "__main__":
    Model_path = r'D:\Projects\Colan\FixedBid\Bobby\AvatarBot Project\Trials\Avatar Bot\M1 Model\Moritz(DB variants)\Moritz(DBRT)_L'
    classifiers_loaded = classifier(Model_path,multi_labels=True)
    app.run(debug=True)




# @app.route('/', methods=['GET', 'POST'])
# def chat():
#     global chat_history
#     detected_module = None
#     possible_actions = None
#     user_input = None

#     if request.method == 'POST':
#         user_input = request.form['user_input']
#         ST = time.time()

#         if user_input == 'clear':
#                 chat_history.clear()

#         elif user_input:

#             # First run
#             detected_module, possible_actions = sequence(user_input, Modules_description)

#             if possible_actions and len(possible_actions) > 0:
#                 possible_actions, _ = sequence(user_input, possible_actions)

#             try:
#                 Options = Choices[possible_actions]
#                 print(Options, 'options data')
#                 if Options:
#                     pass
#                     # option_info = request.form['user_input']
#                     # print(option_info)
#                     # Option_details = options_query(Options)
#                     # print(Option_details)
#             except:
#                 pass

#             chat_history.append({'user': user_input, 'bot_module': detected_module, 'bot_actions': possible_actions, })
#             print(chat_history, "chat history data")
#         ET = time.time()
#         print(f'Time = {ET - ST}_secs')

#     # Render the template with chat history
#     return render_template('chat.html', user_input=user_input, chat_history=chat_history)
