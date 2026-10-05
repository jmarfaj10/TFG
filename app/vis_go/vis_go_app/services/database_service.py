from vis_go_app.models import Mission, Log, User, Goal, Prompt
from django.db import transaction
import base64
from django.core.files.base import ContentFile


#LOGS

@transaction.atomic
def create_log(data):
    log_data, goal_data, mission_data, prompt_data = data.values()
    try:
        user = User.objects.get(pk=log_data['user_id'])
    except User.DoesNotExist:
        user = None
    if user:
        log = Log.objects.create(user=user, ip=log_data['ip'])
        if mission_data:
            mission = Mission.objects.create(log=log,
                                            state=mission_data.get("state", None),
                                            distance=mission_data.get("distance", None),
                                            time=mission_data.get("time", None),
                                            x=mission_data.get("x"),
                                            y=mission_data.get("y"),
                                            z=mission_data.get("z"))
            if prompt_data:
                b64 = prompt_data.get("bbox", None)
                if b64:
                    try:
                        b64 = ContentFile(base64.b64decode(b64), name=f"{log.date:%Y%m%d-%H%M%S}-{log.id}.jpg")
                    except Exception:
                        b64 = None
                if prompt_data.get("prompt", None):
                     prompt_text = prompt_data.get("prompt") 
                else:
                     prompt_text = ""
                Prompt.objects.create(mission=mission, 
                                    prompt= prompt_text,
                                    object=prompt_data.get("object") or "",
                                    bbox=b64)
            if goal_data:
                Goal.objects.create(mission=mission,
                                        x=goal_data.get("x", None),
                                        y=goal_data.get("y", None),
                                        z=goal_data.get("z", None))
        return log
    else:
        return None
