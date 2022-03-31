from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Rule
from api.serializers import RuleSerializer
from drf_spectacular.utils import extend_schema

class CartRuleList(APIView):
    @extend_schema(request=None, responses=RuleSerializer)
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data)

class CartRuleCreate(APIView):
    @extend_schema(request=RuleSerializer, responses=RuleSerializer)
    def post(self, request):
        serializer = RuleSerializer(data=request.data)
        if request.data["rule_type"] == "OL" or request.data["rule_type"] == "PD":
            try:
                Rule.objects.get(rule_type=request.data["rule_type"])
                return Response({
                    'error': 'Rule already exists'
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except:
                pass            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartRuleChange(APIView):
    @extend_schema(request=RuleSerializer, responses=RuleSerializer)
    def put(self, request, pk):
        try: 
            rule = Rule.objects.get(pk=pk)
            serializer = RuleSerializer(rule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'error': 'Rull does not exist'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=None, responses=RuleSerializer)
    def delete(self, request, pk):
        try:
            rule = Rule.objects.get(pk=pk)
            rule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'Rull does not exist'
            }, status=status.HTTP_404_NOT_FOUND)