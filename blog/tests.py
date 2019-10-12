from django.test import TestCase
import json
# Create your tests here.

s = '{"changeType":"OFFLINE","dataType":"PRODUCT","dataList":[{"uniqueCode":"900915","roomAndRates":[{"ratePlanIds":[31],"dateExpression":null,"class":"com.oyo.ota.platform.direct.dto.RoomAndRateDTO","roomTypeId":20}],"ratePlanId":null,"class":"com.oyo.ota.platform.direct.dto.NotifyDataChangeInfoDTO"}],"class":"com.oyo.ota.platform.direct.dto.NotifyDataChangeParamDTO"}'

a = json.loads(s)
print(a)
print(type(a))
