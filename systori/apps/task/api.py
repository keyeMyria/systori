from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from rest_framework import views, viewsets, mixins
from rest_framework import response, renderers
from systori.lib.templatetags.customformatting import ubrdecimal
from .models import Job, Group, Task
from .serializers import JobSerializer
from ..user.permissions import HasStaffAccess


class EditorAPI(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (HasStaffAccess,)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)


class SearchAPI(views.APIView):

    permission_classes = (HasStaffAccess,)

    def post(self, request, *args, **kwargs):
        model_type = request.data["model_type"]
        terms = request.data["terms"]
        if model_type == "group":
            remaining_depth = int(request.data["remaining_depth"])
            return response.Response(
                list(
                    Group.objects.groups_with_remaining_depth(remaining_depth)
                    .search(terms)
                    .distinct("name", "rank")
                    .values(
                        "id", "job__name", "match_name", "match_description", "rank"
                    )[:30]
                )
            )
        elif model_type == "task":
            qs = Task.objects.raw(
                """
                    SELECT
                    task_task.id,
                    COUNT(task_lineitem.id) AS lineItemCount,
                    ts_headline('german', task_task.description, plainto_tsquery('german'::regconfig, '{terms}')) AS match_description,
                    ts_headline('german', task_task.name, plainto_tsquery('german'::regconfig, '{terms}')) AS match_name
                    FROM task_task
                    JOIN (
                    SELECT DISTINCT ON (task_task.search) * FROM task_task
                    ) distinctifier
                    ON task_task.id = distinctifier.id
                    LEFT JOIN task_lineitem ON (task_task.id = task_lineitem.task_id)
                    WHERE task_task.search @@ (plainto_tsquery('german'::regconfig, '{terms}')) = true 
                    GROUP BY task_task.id
                    ORDER BY lineItemCount DESC
                """.format(
                    terms=terms
                )
            )[:30]
            return response.Response(
                [
                    {
                        "id": task.id,
                        "match_name": task.match_name,
                        "match_description": task.match_description,
                    }
                    for task in qs
                ]
            )


class InfoAPI(views.APIView):

    permission_classes = (HasStaffAccess,)

    def get(self, request, *args, **kwargs):
        model_type = kwargs["model_type"]
        model_pk = int(kwargs["pk"])
        if model_type == "group":
            group = Group.objects.get(pk=model_pk)
            return response.Response(
                {
                    "name": group.name,
                    "description": group.description,
                    "total": ubrdecimal(group.estimate),
                }
            )
        elif model_type == "task":
            task = Task.objects.get(pk=model_pk)
            return response.Response(
                {
                    "name": task.name,
                    "description": task.description,
                    "project_string": _("Project"),
                    "project_id": task.group.job.project.id,
                    "qty": ubrdecimal(task.qty, min_significant=0),
                    "unit": task.unit,
                    "price": ubrdecimal(task.price),
                    "total": ubrdecimal(task.total),
                    "lineitems": [
                        {
                            "name": li["name"],
                            "qty": ubrdecimal(li["qty"], min_significant=0),
                            "unit": li["unit"],
                            "price": ubrdecimal(li["price"]),
                            "total": ubrdecimal(li["total"]),
                        }
                        for li in task.lineitems.values(
                            "name", "qty", "unit", "price", "total"
                        )
                    ],
                }
            )


class CloneAPI(views.APIView):

    renderer_classes = (renderers.TemplateHTMLRenderer,)
    permission_classes = (HasStaffAccess,)

    def post(self, request, *args, **kwargs):
        source_type = request.data["source_type"]
        position = request.data["position"]
        source_class = {"group": Group, "task": Task}[source_type]
        source = source_class.objects.get(pk=int(request.data["source_pk"]))
        target = Group.objects.get(pk=int(request.data["target_pk"]))
        source.clone_to(target, position)
        source = source_class.objects.get(pk=source.pk)
        return response.Response(
            {source_type: source},
            template_name="task/editor/{}_loop.html".format(source_type),
        )


urlpatterns = [
    url(
        r"^job/(?P<pk>\d+)/editor/save$",
        EditorAPI.as_view({"post": "update"}),
        name="api.editor.save",
    ),
    url(r"^editor/search$", SearchAPI.as_view(), name="api.editor.search"),
    url(
        r"^editor/info/(?P<model_type>(group|task))/(?P<pk>\d+)$",
        InfoAPI.as_view(),
        name="api.editor.info",
    ),
    url(r"^editor/clone$", CloneAPI.as_view(), name="api.editor.clone"),
]
