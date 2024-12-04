from kavenegar import *
import json


def send_login_code(phone, code):
    try:
        api_key = '5A3744443068464371454B30473039694C796C5175316C596B6F696A73684572576B5947304D4A534F47303D'
        api = KavenegarAPI(api_key)

        message = f"""بایت مارکت\n کد تایید شما برای ورود {code} می باشد. """

        params = {'sender': '1000689696', 'receptor': phone, 'message': message}
        api.sms_send(params)

    except APIException as e:
        print(e)

    except HTTPException as e:
        print(e)
