from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        return Response({"message": f"Welcome, {user.username}!"})