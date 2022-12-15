from rest_framework import serializers
from account.models import Message, Chatter


class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()
	receiver = serializers.StringRelatedField()
	class Meta:
		model = Message
		fields = "__all__"
		

class ChatterSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	friends = serializers.StringRelatedField(many=True)
	class Meta:
		model = Chatter
		fields = "__all__"