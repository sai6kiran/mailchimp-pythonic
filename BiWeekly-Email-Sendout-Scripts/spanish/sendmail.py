from mailchimp3 import MailChimp
import json
import time
import os



def delete(mcc, cid,tid):
	if(mcc.campaigns.get(campaign_id = cid)['status']=='sent'):
		mcc.campaigns.delete(campaign_id = cid)
		mcc.templates.delete(template_id = tid)
	else:
		now = time.time()

		ftr = now + 100
		if(time.time() < ftr):
			delete(mcc, cid,tid)

		else:
			print("No se puede borrar la campaña")

client = MailChimp(mc_api=os.getenv("mailchimp_api_key"), mc_user=os.getenv("mailchimp_admin_user"))

if((client.templates.all(get_all=True))['templates'] is not None):
	lot = json.loads(json.dumps(client.templates.all(get_all=True)))['templates']
	mrtt = 0
	for i in range(0, len(lot)):
		ct = lot[i]['date_created']

		date_time = ct.split('T')[0] + ' ' + ct.split('T')[1].split('+')[0]
		pattern = '%Y-%m-%d %H:%M:%S'
		epoch = int(time.mktime(time.strptime(date_time, pattern)))

		
		if(epoch>mrtt):
			mrti = lot[i]['id']
			mrtt = epoch
else:
	print("No templates are existing")

data = {
	"recipients": {
		"list_id": os.getenv("mailchimp_list_id"),
		"list_is_active":True,
		"list_name":"Paracelsus Members",
		"segment_opts":{"saved_segment_id":int(os.getenv("mailchimp_spanish_segmentid"))}
	},
	"settings": {
		"subject_line": "¡Nuevos artículos de Paracelso!",
		"title":"¡Nuevos artículos de Paracelso!", 
		"from_name": "Paracelsus \"Health & Healing\"",
		"reply_to": "info@paracelsus-magazin.ch",
		"authenticate": True,
		"template_id": mrti
	},
	"tracking":{ 
		"opens":True,
		"html_clicks":True,
		"text_clicks":False,
		"goal_tracking":False,
		"ecomm360":False,
		"google_analytics":"",
	},
	"type": "regular"
}
client.campaigns.create(data)

if((client.campaigns.all(get_all=True))['campaigns'] is not None):
	loc = json.loads(json.dumps(client.campaigns.all(get_all=True)))['campaigns']
	mrct = 0
	for i in range(0, len(loc)):
		ct = loc[i]['create_time']
		date_time = ct.split('T')[0] + ' ' + ct.split('T')[1].split('+')[0]
		pattern = '%Y-%m-%d %H:%M:%S'
		epoch = int(time.mktime(time.strptime(date_time, pattern)))
		if(epoch>mrct):
			mrci = loc[i]['id']
			mrct = epoch
else:
	print("No existen campañas")

client.campaigns.actions.send(campaign_id = mrci)
delete(client, mrci,mrti)
print("************El correo electrónico se ha enviado correctamente!*****************")
