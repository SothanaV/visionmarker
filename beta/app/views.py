from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Batch, Image, Label, MyUser
import app.models as md
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='wl_auth:signin')
def home(request):
	print "home"
	if 'username' in request.session:
		_username=request.session['username']
		print "username: %s"%_username
		u=User.objects.get(username=_username)
		mu=MyUser.objects.get(user=u)
		if mu.isreviewer:
			b=Batch.objects.filter(status=md.REVIEWING).first()
			if b:
				return render(request,'home.html',{'batch_id':b.id,'username':_username,'isreviewer':1})
			else:
				return render(request,'home.html',{'batch_id':'','username':_username,'isreviewer':1} )
		else:
			b=Batch.objects.filter(status=md.TAGGING,labeller=mu).first()
			if not b: #not found
				b=Batch.objects.filter(status=md.TODO).first()				
			if b:
				b.labeller=mu
				b.save()
				return render(request,'home.html',{'batch_id':b.id,'username':_username,'isreviewer':0})
			else:
				return render(request,'home.html',{'batch_id':'','username':_username,'isreviewer':0} )

#@csrf_exempt
@login_required(login_url='wl_auth:signin')
def batch(request, batch_id):
	if request.method == 'GET':
		_labels=[{"id":"rec0","x":290,"y":245,"width":650,"height":341,
			"brand":"b0","model": "m0", "color":"c0", "nn":"n0" },]
		_images=[ {"src":"static/dataset/_00.jpg", "labels":_labels},]

		#x=Batch.objects.get(pk=batch_id)
		BID=Batch.objects.get(pk=batch_id)
		IMGS=Image.objects.filter(batch=BID)
		data=[]
		for I in IMGS:
			labels=[]
			for L in Label.objects.filter(image=I):
				labels.append({
					#"id":"rec%d"%L.id,
					"x":L.x,
					"y":L.y,
					"width":L.width,
					"height":L.height,
					"brand":L.brand,
					"model": L.model,
					"color":L.color,
					"nn":L.nickname,
					})
			item={'src':I.src_path, 'labels': labels}	
			data.append(item)
		return JsonResponse(data, safe=False)
	if request.method=='POST':
		client_data = json.loads(request.POST.get('client_data'))
		print client_data
		images=client_data
		for i in images:
			print "i: %s"%i
			m=Image.objects.get(src_path=i['src'])
			Label.objects.filter(image=m).delete()
			for j in i['labels']:
				m=Image.objects.get(src_path=i['src'])
				q=Label(
					image = m,
					x = j['x'],
					y = j['y'],
					width = j['width'],
					height = j['height'],
					brand = j['brand'],
					model = j['model'],
					color = j['color'],
					nickname = j['nn']
					)
				q.save()
		if request.POST.get('rework'):
			b=Batch.objects.get(pk=batch_id)
			b.status=md.TAGGING
			b.save()
		else:
			if request.POST.get('submission'):
				if request.POST.get('submission')=='1':	#reviewer
					b=Batch.objects.get(pk=batch_id)
					b.status=md.DONE
					b.save()
					print "DONE:: batch: %s, status: %s, submission: %s"%(b, b.status, request.POST.get('submission'))
				else:									#labeller
					b=Batch.objects.get(pk=batch_id)
					b.status=md.REVIEWING
					b.save()
					print "TO REVIEWER:: batch: %s, status: %s, submission: %s"%(b, b.status, request.POST.get('submission'))
			elif 'username' in request.session:#debug view92
				_username=request.session['username']
				print "#debug view92:: username: %s"%_username
				u=User.objects.get(username=_username)
				mu=MyUser.objects.get(user=u)

				b=Batch.objects.get(pk=batch_id)
				b.status=md.TAGGING
				b.labeller=mu
				b.save()
				print "batch: %s, status: %s"%(b, b.status)
		return JsonResponse(images, safe=False)

