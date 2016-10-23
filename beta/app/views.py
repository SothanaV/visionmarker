# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Batch, Image, Label, MyUser, Comment
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

@login_required(login_url='wl_auth:signin')
def chat(request, batch_id):
	_log=""
	if request.method=='POST':
		if 'username' in request.session:
			_username=request.session['username']
			print "#debug view92:: username: %s"%_username
			u=User.objects.get(username=_username)
			mu=MyUser.objects.get(user=u)

			_message = request.POST.get('message')
			c=Comment(user=mu, message=_message, batch=Batch.objects.get(pk=batch_id))
			c.save()

	q=Comment.objects.filter(batch=Batch.objects.get(pk=batch_id)).order_by('created_time')
	for i in q:
		_log=_log+"%s: %s\n"%(i.user.user.username[:6], i.message)

	return JsonResponse({"log":_log}, safe=False)

@login_required(login_url='wl_auth:signin')
def typeahead(request, mode):
	if mode=="brands":
		return JsonResponse(["Toyota","Honda","Hyundai","Nissan","Tata","T1","T2","T3","T4","X1"], safe=False)
	if mode=="models":
		return JsonResponse(["Vios","Camry","Altis"], safe=False)
	if mode=="colors":
		return JsonResponse(["White","Black","Red","Blue","Gold"], safe=False)
	if mode=="nicknames":
		return JsonResponse(["Toyota","honda",u"ปลาวาฬ"], safe=False)
