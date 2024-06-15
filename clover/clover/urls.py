from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from users import views as u_views
from forums import views as f_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('trailer', views.trailer, name="trailer"),
    #LEADERBOARDS
    path('leaderboards', views.hcf_view, name="leaderboards"),
    path('practice', views.practice, name="practice"),
    path('kitmap', views.kitmap, name="kitmap"),
    path('practice/<ladder>/<page>', views.practice_more, name="practice_more"),
    #HCF URLS
    # path('armadas', views.hcf_view, name="hcf"),
    # path('armadas/<stat>/<page>', views.hcf_more, name="hcf_more"),
    # path('armadas/faction/<faction>', views.hcf_faction, name="hcf_faction"),
    # path('hcf/faction/<faction>', views.hcf_faction),
    # path('hcf', views.hcf_view),
    # path('hcf/<stat>/<page>', views.hcf_more),

    # path('kitmap/<stat>/<page>', views.kitmap_more, name="kitmap_more"),
    #USER STUFF
    path('u/<user>', u_views.user, name="user"),
    path('user/<user>', u_views.user),
    path('staff', views.staff, name="staff"),
    # path('famous', views.famous, name="famous"),
    # path('media', views.famous, name="famous"),
    path('register', u_views.register, name="register"),
    path('api/players/name', views.api, name="api"),
    path('login', u_views.login_page, name="login"),
    path('logout', u_views.logout_page, name="logout"),
    path('register/confirm', u_views.register_confirm, name="register_confirm"),
    path('register/request', u_views.register_request, name="register_request"),
    #USER API
    path('api/player/<uuid>', u_views.api_get_player),
    path('api/get/player/trending', u_views.api_get_trending_players),
    #Forums stuff
    path('thread/<id>/<title>', f_views.thread, name="thread"),
    path('forums', f_views.forums, name="forums"),
    path('forums/<forum>', f_views.forum, name="forum"),
    path('thread/create', f_views.create_thread, name="create_thread"),

    #FORUMS API
    path('thread/api/reply/create/<reply_type>', f_views.api_reply),
    path('thread/api/reply/get/<reply>', f_views.api_reply_get),
    path('thread/api/reply/edit/<reply>', f_views.api_reply_edit),
    path('thread/api/reply/delete/<reply>', f_views.api_reply_delete),
    path('thread/api/thread/edit/<thread>', f_views.api_thread_edit),

    path('thread/api/partial/subreply-create/<reply>', f_views.api_sub_reply_create_partial),
    #Admin stuff
    #path('admin/ranks', views.ranks, name="ranks"),
    # path('graphs', views.graphs, name="graphs"),
    # path('api/graphs/<ip>', views.get_graph, name="graph_api"),
]
