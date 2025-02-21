from datetime import datetime


def dateTime_convert_to_ddMMyyyyHHMMssStr(dateTime):
    try:
        create_date_obj = datetime.strptime(str(dateTime), "%Y-%m-%d %H:%M:%S")

        return create_date_obj.strftime("%d/%m/%Y  %H:%M:%S")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


def dateTime_convert_to_ddMMyyyystr(dateTime):
    try:
        create_date_obj = datetime.strptime(str(dateTime), "%Y-%m-%d %H:%M:%S")

        return create_date_obj.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")


def date_convert_to_ddMMyyyystr(date):
    try:
        res = datetime.strptime(str(date), "%Y-%m-%d")
        return res.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")  

def date_convert_to_yyyyMMddstr(date):
    try:
        res = datetime.strptime(str(date), "%Y-%m-%d")
        return res.strftime("%Y/%m/%d")
    except Exception as e:
        print(f"Exception caught: {e.args[0]}")  