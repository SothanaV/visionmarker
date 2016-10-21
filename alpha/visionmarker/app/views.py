from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Batch, Image, Label
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='wl_auth:signin')
def home(request):
	if request.method == 'GET':
		return render(request,'home.html',{'batch_id': Batch.objects.filter(status='1').first().id})
	if request.method == 'POST':
		return render(request,'home.html',{'batch_id': 1})

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
		return JsonResponse(images, safe=False)

