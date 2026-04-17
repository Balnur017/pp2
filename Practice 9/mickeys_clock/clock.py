from datetime import datetime

def get_time_angles():
    now = datetime.now()

   
    minutes = now.minute
    hours = now.hour % 12


    

    minute_angle = -(minutes * 6)
    

    hour_angle   = -(hours * 30 + minutes * 0.5)

    return hour_angle, minute_angle