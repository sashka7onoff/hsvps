from rest_framework import serializers
from .models import MealEntry

class MealEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = ['id','eaten_at','meal_type','is_planned','reasons','hunger_level','portion','junk_items','positive_items','rating','note','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

    def validate_reasons(self, value):
        if len(value) > 2:
            raise serializers.ValidationError('Можно выбрать до 2 причин')
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
