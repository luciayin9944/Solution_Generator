from math_project import app
from math_project.views.AuthPublic import auth_public
from math_project.views.ParentViewRewardRecord import parent_reward_record

'''
Blueprint
'''
from math_project.views.Auth import auth
from math_project.views.StudentViewRecords import records
from math_project.views.ParentViewStudent import parent_student
from math_project.views.ParentViewPayment import payment
from math_project.views.ParentView import parentView
from math_project.views.ParentViewRewardPlan import parent_reward
# from math_project.views.ParentViewRewardRecord import parent_reward_record
from math_project.views.Subscribe import subscribe
from math_project.views.StudentViewTestRecord import test_record
from math_project.views.StudentView import studentView
from math_project.views.StudentViewTest import studentViewTest
from math_project.views.StudentViewPractice import studentViewPractice
from math_project.views.StudentViewQuestionList import studentViewQuestionList
from math_project.views.StudentViewQuestionListQuestion import studentViewQuestionListQuestion
from math_project.views.StudentViewHistory import studentViewHistory



app.register_blueprint(auth)
app.register_blueprint(auth_public)
app.register_blueprint(records)
app.register_blueprint(parent_student)
app.register_blueprint(parentView)
app.register_blueprint(subscribe)
app.register_blueprint(test_record)
app.register_blueprint(studentView)
app.register_blueprint(studentViewTest)
app.register_blueprint(studentViewPractice)
app.register_blueprint(studentViewQuestionList)
app.register_blueprint(studentViewQuestionListQuestion)
app.register_blueprint(studentViewHistory)
app.register_blueprint(payment)
app.register_blueprint(parent_reward)
app.register_blueprint(parent_reward_record)

if __name__ == '__main__':
    # print(app.url_map)
    app.debug = True
    app.run(ssl_context='adhoc')
