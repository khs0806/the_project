
from django.shortcuts import render, get_object_or_404
import pandas as pd
import folium
import json
from folium.features import DivIcon
from folium.plugins import MarkerCluster
from blog.models import Post
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm 


# Create your views here.
def post_list(request):

    crime_seoul = pd.read_csv("static/seoul_crime_data.csv")
    
    #c_list=[]
    #for i in range(len(crime_seoul.columns))
    #   if i[-2:]=='_p':
    #       c_list.append(i)
    #sc_clist = [i for i in c_list]
    sc_clist = [i for i in crime_seoul.columns]
    clist=[]
    for i in sc_clist:
        if i[-2:] == '_p':
            clist.append(i.strip('_p'))
    sc_ylist = [int(i) for i in crime_seoul['year'].unique()]
    print(clist,sc_ylist)

    return render(request, 'htmltest/post_list.html', {'sc_ylist':sc_ylist,'sc_clist':clist,'l_year':sc_ylist[0],'l_rate':clist[0]})

def make_map(request,year_r,rate_r,poli_loc):#, year, columns,poli_loc
    
    #year=2018
    year=int(year_r)
    rate=rate_r+'_p'
    poli_loc = int(poli_loc)
    crime_seoul = pd.read_csv("static/seoul_crime_data.csv")
    year_data=crime_seoul[crime_seoul.year==year]
    year_data=year_data.set_index('state')
    geo_path = 'static/seoul_state_map.json'
    geo_str = json.load(open(geo_path, encoding='utf-8'))
    f = folium.Figure (width = 600, height = 530)
    map = folium.Map(location=[37.5592, 126.982], zoom_start=11,
                    tiles='Stamen Toner').add_to (f)

    
    map.choropleth(geo_data=geo_str,
                  data=year_data[rate],
                  columns=[year_data.index, year_data[rate]],
                  fill_color='YlOrRd',   #Reds,YlOrRd,PuRd,Oranges
                  key_on='feature.id',
                  legend_name=rate[:-2]
                  )
    gps_data = pd.read_csv('static/seoul_state_gps.csv',encoding = 'utf-8')
    for i in gps_data.index:
        x=gps_data.loc[i,'state_x']
        y=gps_data.loc[i,'state_y']-0.015
        kor_s=gps_data.loc[i,'state_kor']
        folium.map.Marker(
        [x,y],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 12pt">'+gps_data.loc[i,'state_kor']+'</div>',
            )
        ).add_to(map)

    
    data=pd.read_excel('static/seoul_marker.xlsx')
    if poli_loc == 1:
        icon_create_function = """\
        function(cluster) {
            return L.divIcon({
            html: '<b style="font-size:18px">&nbsp' + cluster.getChildCount() + '</b>',
            className: 'marker-cluster marker-cluster-large',
            iconSize: new L.Point(30, 30)
            });
        }"""
        y = data.geo_y.values
        x = data.geo_x.values
        locations = list(zip(y,x))
        popups = list(data.title.values)
        marker_cluster = MarkerCluster(
            locations=locations, popups=popups,
            name='seoul',
            overlay=True,
            control=True,
            icon_create_function=icon_create_function
        )
        marker_cluster.add_to(map)


    # c_list=[]
    # for i in range(len(crime_seoul.columns)):
    #     if i[-2:]=='_p':
    #         c_list.append(i)
    #sc_clist = [i for i in c_list]
    sc_clist = [i for i in crime_seoul.columns]
    clist=[]
    for i in sc_clist:
        if i[-2:] == '_p':
            clist.append(i.strip('_p'))
    sc_ylist = [int(i) for i in crime_seoul['year'].unique()]
    #dic_m={'year':sc_ylist,'columns':sc_clist}

    map.save('htmltest/templates/htmltest/s_map.html')


    return render(request, 'htmltest/post_list.html', {'sc_ylist':sc_ylist,'sc_clist':clist,'l_year':year,'l_rate':rate.strip('_p')})
# def s_map(request):
#     return render(request, 'htmltest/s_map.html', {})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'htmltest/post_list.html',{'post':post})

def test_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'htmltest/list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'htmltest/post_edit.html', {'form': form})

def index(request):
    return render(request, 'htmltest/index.html')

def indextwo(request):
    return render(request, 'htmltest/indextwo.html')

def tozi(request):
    return render(request, 'htmltest/200122.html')

def gutozi(request):
    return render(request, 'htmltest/gutozi.html')

def piechart(request):
    return render(request, 'htmltest/piechart.html')

def satis(request):
    return render(request, 'htmltest/satis.html')

def lat(request):
    return render(request, 'htmltest/lat.html')

def marker(request):
    return render(request, 'htmltest/marker.html')

def center(request):
    return render(request, 'htmltest/center.html')