import sys
import csv
from datetime import datetime, timedelta
import random

review_time = [1, 2, 5, 8, 15, 30, 60]
header = ['id', 'name', 'link', 'review date',
          'next review date', 'created date', 'tags']
date_format = '%Y-%m-%d'
today = datetime.today().date()


filename = ""
problem_list = []
todays_list = []


# file reader/writer
def read_csv():
    with open(filename+'.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            review_date = get_date_obj(row['next review date'])
            if review_date <= today:
                todays_list.append(row)
            problem_list.append(row)


def create_csv():
    with open(filename+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)


def write_new_problem(row):
    with open(filename+'.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow(row)


def update_problem_list():
    with open(filename+'.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(problem_list)


# date helper
def get_date_obj(date):
    return datetime.strptime(date, date_format).date()


def get_next_date(days):
    next_date = today + timedelta(days)
    return next_date.strftime(date_format)


def get_next_review_date(review_date, next_review_date):
    next_review_day_diff = {
        1: 2,
        2: 5,
        5: 8,
        8: 15,
        15: 30,
        30: 60,
        60: 9999
    }

    r_date = get_date_obj(review_date)
    n_date = get_date_obj(next_review_date)
    return get_next_date(next_review_day_diff[(n_date - r_date).days])


# problem related
def print_by_line(l):
    print(*l, sep='\n')


def list_all_problems():
    print("")
    print(f"Total has {len(problem_list)} problems:")
    print_by_line(problem_list)
    resume_operation()


def list_review_problems_for_today():
    print("")
    print(f"Total has {len(todays_list)} problems:")
    print_by_line(todays_list)
    resume_operation()


def add_new_problem():
    new_problem = {}
    new_problem['id'] = input("Problem Id: ").strip()
    new_problem['name'] = input("Problem name: ").strip()
    new_problem['link'] = input("Problem link: ").strip()
    new_problem['review date'] = today.strftime(date_format)
    new_problem['created date'] = today.strftime(date_format)
    new_problem['next review date'] = get_next_date(1)
    new_problem['tags'] = input("Problem tags, please provide in comma separated format: ").strip()

    problem_list.append(new_problem)
    write_new_problem(new_problem)
    resume_operation()


def review_questions():
    print(f"Tere are {len(todays_list)} problems need to be reviewed.")

    while todays_list:
        curr = todays_list.pop()

        print(curr)
        print(
            'Do you need to add the problem back to the top of review list? Press y or n.')
        curr['next review date'] = get_next_date(1) if input().lower(
        ) == 'y' else get_next_review_date(curr['review date'], curr['next review date'])
        curr['review date'] = today.isoformat()
        update_problem_list()

    resume_operation()


def review_random_question():
    print('Randomly pick a problem to review')
    random_int = random.randint(0, len(problem_list) - 1)
    review_question = problem_list[random_int]

    print(review_question)
    print('Do you need to add the problem back to the top of review list? Press y or n.')
    review_question['next review date'] = get_next_date(1) if input().lower(
    ) == 'y' else get_next_review_date(review_question['review date'], review_question['next review date'])
    review_question['review date'] = today.isoformat()

    update_problem_list()

    resume_operation()


def get_questions_by_tag():
    tag_name = input('Please provide tag name: ')
    tag_questions = [d for d in problem_list if tag_name in d['tags']]

    print(f"There are {len(tag_questions)} match with tag name: {tag_name}")
    print_by_line(tag_questions)

    resume_operation()


# get user inputs & operate based on input
def resume_operation():
    input("\nPress any key to continue...\n")
    prompt_operation()


def prompt_operation():
    print("""
          
    ==========================================
    1. Print all the problems
    2. List problems need to be reviewed today
    3. Add a new problem
    4. Review problems
    5. Review a random problem
    6. List questions by tag
    
    Press "q" to quit
    ==========================================
          
    """)
    while True:
        user_input = input("Enter your input: ")
        if user_input == '1':
            list_all_problems()
        elif user_input == '2':
            list_review_problems_for_today()
        elif user_input == '3':
            add_new_problem()
        elif user_input == '4':
            review_questions()
        elif user_input == '5':
            review_random_question()
        elif user_input == '6':
            get_questions_by_tag()
        elif user_input.lower() == 'q':
            print("Bye")
            sys.exit()


# entry point
def operate_file():
    operations = sys.argv[1].split('=')
    operation = operations[0]
    global filename
    filename = operations[1]
    if operation == '-c':
        create_csv()
    elif operation == '-r':
        read_csv()

    prompt_operation()


operate_file()
