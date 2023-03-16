from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_project_quota'

router = NetBoxRouter()
router.register('project', views.ProjectViewSet)
router.register('quotatemplate', views.QuotaTemplateViewSet)

urlpatterns = router.urls