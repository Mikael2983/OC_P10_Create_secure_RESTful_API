from rest_framework import serializers

from .models import Comment, Issue, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'date_created', 'name', 'author', 'type', ]

    def validate_name(self, value):
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError('Project already exists')
        return value

    def validation(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('name must be in description')
        return data


class ProjectDetailSerializer(serializers.ModelSerializer):
    Issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'date_created', 'name', 'author', 'type',
                  'description', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'status', 'priority', 'nature',
                  'project']


class CommentSerializer(serializers.ModelSerializer):
    issue_link = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'description', 'issue', 'issue_link']

    def get_issue_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/issues/{obj.issue.id}/')
        return None
