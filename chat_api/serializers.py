from rest_framework import serializers
from account.models import Message, Chatter


class MessageSerializer(serializers.ModelSerializer):
	sender = serializers.StringRelatedField()
	receiver = serializers.StringRelatedField()
	class Meta:
		model = Message
		fields = "__all__"
		
		