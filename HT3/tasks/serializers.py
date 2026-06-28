from rest_framework import serializers, viewsets, permissions
from .models import Task, Plan, TaskPlan


class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()
    plan_names = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'parent', 'subtasks', 'plans', 'plan_names',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_subtasks(self, obj):
        subtasks = obj.subtasks.all()
        return TaskSerializer(subtasks, many=True, context=self.context).data

    def get_plan_names(self, obj):
        return [p.name for p in obj.plans.all()]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PlanSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'type', 'start_date', 'end_date', 'is_active', 'created_at', 'task_count']
        read_only_fields = ['user', 'created_at']

    def get_task_count(self, obj):
        return obj.task_plans.filter(is_active=True).count()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskPlanSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = TaskPlan
        fields = ['id', 'task', 'plan', 'task_title', 'plan_name', 'added_at', 'is_active']


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).select_related('user').prefetch_related('subtasks', 'plans')


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user).select_related('user')


class TaskPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TaskPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskPlan.objects.filter(
            task__user=self.request.user
        ).select_related('task', 'plan')
