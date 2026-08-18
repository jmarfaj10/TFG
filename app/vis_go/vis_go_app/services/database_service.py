from vis_go_app.models import Mission, Log, User, Goal, Prompt


#USER
def login(username, password):
    try:
        user = User.objects.get(username= username)
    except User.DoesNotExist:
        return False
    return user.check_password(password)

def sing_in(username, password, v_password):
    if User.objects.filter(username= username).exists():
        if password == v_password:
            user = User()
            user.username = username
            user.set_password(password)

#LOGS
