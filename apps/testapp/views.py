from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import viewsets, status
from .services import authenticate_or_create_google_user
from .permissions import IsTeacherOrReadOnly

class GoogleAuthView(APIView):
    def post(self, requests):
        code = requests.data.get("code")
        if not code:
            return Response({"error": "Поле 'code' обязательно."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            return Response(authenticate_or_create_google_user(code), 
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsTeacherOrReadOnly]

    def list(self, request):
        return Response({"message": "Список уроков (доступно всем авторизованным)"})
    def create(self, request):
        return Response({"message": "Урок успешно создан (доступно только преподавателям)"}, 
                        status=status.HTTP_201_CREATED)



