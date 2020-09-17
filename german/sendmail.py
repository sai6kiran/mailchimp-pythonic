from mailchimp3 import MailChimp
import json
import time




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
			print("Kann die Kampagne nicht löschen")

client = MailChimp(mc_api='7c2e1725d93298c0dcd73f7a54d76430-us3', mc_user='sai06ks')

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
	print("Es sind keine Vorlagen vorhanden")

data = {
	"recipients": {


		"list_id": "f76e696629",
		"list_is_active":True,
		"list_name":"Paracelsus",
	},
	"settings": {
		"subject_line": "Neue Paracelsus-Artikel",
		"title":"wöchentliche Paracelsus-Artikel", 
		"from_name": "Saikiran Yerraguntla",
		"reply_to": "syerrag1@hawk.iit.edu",
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
	print("No campaigns are existing")

client.campaigns.actions.send(campaign_id = mrci)
delete(client, mrci,mrti)
print("************E-Mail wurde erfolgreich gesendet!*****************")
